import hashlib, json, pathlib, re, unittest
ROOT = pathlib.Path(__file__).resolve().parent
class StagingChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / 'dist/index.html').read_text(encoding='utf-8')
        cls.metadata = json.loads((ROOT / 'dist/SOURCE.json').read_text())
    def test_full_homepage_retained(self):
        self.assertGreater(len(self.html), 45000)
        for marker in ['main-content', 'peopleEl', 'AI ROI Snapshot', 'Real Results from Real Teams', 'site-footer']:
            self.assertIn(marker, self.html)
    def test_clear_staging_notice(self):
        self.assertIn('STAGING COPY', self.html)
        self.assertIn('Production is unchanged', self.html)
    def test_noindex(self):
        self.assertIn('noindex,nofollow,nosnippet', self.html)
        self.assertIn('Disallow: /', (ROOT / 'dist/robots.txt').read_text())
    def test_all_four_apps_linked(self):
        for repo in ['zion-mcp-trust-lab','zion-rag-evidence-lab','zion-api-contract-lens','zion-retry-lab']:
            self.assertGreaterEqual(self.html.count('https://priyapondi10-tech.github.io/' + repo + '/'), 2)
    def test_upstream_root_links_are_absolute(self):
        self.assertNotRegex(self.html, r'''(?:href|src|action)=["']/(?!/)''')
        self.assertIn('https://ziontechgroup.com/solutions/', self.html)
    def test_reproducible_source_and_output(self):
        self.assertEqual(self.metadata['source_git_blob'], '97c56dd327d0bb3d2921046367100e3c16a51ea1')
        self.assertEqual(self.metadata['staging_sha256'], hashlib.sha256(self.html.encode()).hexdigest())
        self.assertFalse(self.metadata['production_modified'])
    def test_no_custom_domain_binding(self):
        self.assertFalse((ROOT / 'dist/CNAME').exists())
        self.assertFalse(self.metadata['custom_domains_bound'])
    def test_webpage_structured_data(self):
        match = re.search(r'<script id="staging-structured-data" type="application/ld\+json">(.*?)</script>', self.html, re.S)
        self.assertIsNotNone(match)
        data = json.loads(match.group(1))
        self.assertEqual(data['@context'], 'https://schema.org')
        self.assertEqual(data['@type'], 'WebPage')
        self.assertEqual(data['url'], 'https://priyapondi10-tech.github.io/zion-catalog-staging/')
        self.assertEqual(data['isBasedOn'], 'https://ziontechgroup.com/')
    def test_existing_production_canonical_preserved(self):
        self.assertEqual(self.html.count('rel="canonical"'), 1)
        self.assertIn('<link rel="canonical" href="https://ziontechgroup.com/"', self.html)
if __name__ == '__main__':
    unittest.main()
