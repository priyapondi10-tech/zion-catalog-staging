"""Materialize a faithful, pinned public homepage copy with isolated staging additions."""
import argparse, hashlib, json, pathlib, re, urllib.request
SOURCE_COMMIT = '074dee49c7709bb61920fd45d4ec39693bde1fb0'
SOURCE_BLOB = '97c56dd327d0bb3d2921046367100e3c16a51ea1'
SOURCE_URL = f'https://raw.githubusercontent.com/Zion-support/zion-support.github.io/{SOURCE_COMMIT}/index.html'
ROOT = pathlib.Path(__file__).resolve().parent

def build(raw):
    blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    if blob != SOURCE_BLOB:
        raise ValueError('The pinned homepage content does not match the reviewed Git blob.')
    html = raw.decode('utf-8')
    html = re.sub(r'''(\b(?:href|src|action)=["'])/(?!/)''', lambda m: m.group(1) + 'https://ziontechgroup.com/', html)
    html = re.sub(r'<meta\b[^>]*name=["\']robots["\'][^>]*>', '', html, flags=re.I)
    html = html.replace('<title>', '<title>STAGING — ', 1)
    structured_data = {'@context': 'https://schema.org', '@type': 'WebPage', '@id': 'https://priyapondi10-tech.github.io/zion-catalog-staging/#webpage', 'url': 'https://priyapondi10-tech.github.io/zion-catalog-staging/', 'name': 'STAGING — Zion Tech Group | Advanced AI Services & IT Solutions', 'description': 'Noindex staging copy of the Zion Tech Group homepage with links to four working browser-based utilities. This is not the production site.', 'isBasedOn': 'https://ziontechgroup.com/', 'inLanguage': 'en'}
    schema_script = '<script id="staging-structured-data" type="application/ld+json">' + json.dumps(structured_data, ensure_ascii=False) + '</script>\n'
    styles = (ROOT / 'staging.css').read_text(encoding='utf-8')
    html = html.replace('</head>', '<meta name="robots" content="noindex,nofollow,nosnippet">\n' + schema_script + '<style id="staging-styles">' + styles + '</style>\n</head>', 1)
    banner = '<div class="stage-banner" role="note">STAGING COPY · Hosted by priyapondi10-tech · Production is unchanged · <a href="#staging-apps">Open the four new utilities</a></div>'
    html, body_count = re.subn(r'(<body\b[^>]*>)', lambda m: m.group(1) + banner, html, count=1, flags=re.I)
    feature = (ROOT / 'features.html').read_text(encoding='utf-8')
    html, main_count = re.subn(r'(<main\b[^>]*>)', lambda m: m.group(1) + feature, html, count=1, flags=re.I)
    if body_count != 1 or main_count != 1:
        raise ValueError('The reviewed homepage structure changed unexpectedly.')
    out = ROOT / 'dist'
    out.mkdir(exist_ok=True)
    (out / 'index.html').write_text(html, encoding='utf-8')
    (out / 'robots.txt').write_text('User-agent: *\nDisallow: /\n', encoding='utf-8')
    (out / '.nojekyll').touch()
    metadata = {'source_url': SOURCE_URL, 'source_commit': SOURCE_COMMIT, 'source_git_blob': blob, 'source_sha256': hashlib.sha256(raw).hexdigest(), 'staging_sha256': hashlib.sha256(html.encode()).hexdigest(), 'owner': 'priyapondi10-tech', 'production_modified': False, 'custom_domains_bound': False, 'cloudflare_zone_at_setup': 'pending'}
    (out / 'SOURCE.json').write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')
    return out

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-file', type=pathlib.Path, help='Use the exact reviewed snapshot for an offline build.')
    args = parser.parse_args()
    if args.source_file:
        raw = args.source_file.read_bytes()
    else:
        with urllib.request.urlopen(SOURCE_URL, timeout=30) as response:
            raw = response.read(1048577)
        if len(raw) > 1048576:
            raise ValueError('Source unexpectedly exceeds 1 MiB.')
    print('Built staging snapshot:', build(raw))
