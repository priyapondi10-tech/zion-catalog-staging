# Zion homepage — isolated staging copy

Live: https://priyapondi10-tech.github.io/zion-catalog-staging/

This repository builds a **full copy of the reviewed public static homepage**, then adds prominent staging labeling, noindex metadata, four working utility summaries and bidirectional network navigation. The original hero, service sections, case studies, ROI calculator, navigation and footer are retained. Upstream root-relative links are rewritten to https://ziontechgroup.com/ so unmodified production destinations do not become broken staging paths. Upstream marketing claims are reproduced for review, not independently validated.

## Source / reproducibility

Pinned source commit: `Zion-support/zion-support.github.io@074dee49c7709bb61920fd45d4ec39693bde1fb0`, file `index.html`, Git blob `97c56dd327d0bb3d2921046367100e3c16a51ea1`. `build.py` refuses an unexpected source hash. The complete generated `index.html`, `SOURCE.json` and `robots.txt` are automatically committed to main by the workflow before publication; the same files are deployed as the Pages artifact. GitHub-token commits do not recursively trigger this workflow. No history is force-pushed.

```sh
python3 build.py
python3 -m unittest -v test_build.py
python3 -m http.server 8080 --directory dist
```

Python standard library only. For offline reproduction, use `python3 build.py --source-file /path/to/reviewed/index.html`. The build downloads only the pinned public source file; published visitors do not fetch GitHub source or depend on a runtime iframe, decompression library, backend or AI API. GitHub Pages build type is workflow. The generated page is ordinary self-contained HTML.

## Four working tools

- [MCP Trust Lab](https://priyapondi10-tech.github.io/zion-mcp-trust-lab/) — static capability-boundary review.
- [RAG Evidence Lab](https://priyapondi10-tech.github.io/zion-rag-evidence-lab/) — chunk comparison and BM25 evidence.
- [API Contract Lens](https://priyapondi10-tech.github.io/zion-api-contract-lens/) — directional OpenAPI migration risks.
- [Retry Lab](https://priyapondi10-tech.github.io/zion-retry-lab/) — seeded retry/circuit-breaker simulation.

All utilities link back here and to each other. Production is never edited. The new tools process inputs in memory, without analytics or network uploads.

## DNS preparation is not activation

Five DNS-only CNAMEs are prepared in the connected **pending** Cloudflare zone: mcp-trust, rag-evidence, contract-lens, retry-lab and catalog-preview under ziontechgroup.com, all targeting priyapondi10-tech.github.io with automatic TTL. They are not bound as Pages custom domains, so the working github.io HTTPS URLs do not redirect to inactive names. No CNAME file is committed. Nameservers, existing DNS and the production repository are unchanged.

Before future authoritative-zone activation, verify GitHub domain ownership, claim each hostname on the correct Pages repository and validate certificates. Unclaimed prepared custom-domain records can otherwise become a takeover risk. Zone activation/cutover is intentionally outside this deployment.
