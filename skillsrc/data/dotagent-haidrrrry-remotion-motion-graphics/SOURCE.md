---
source_repository: "https://github.com/haidrrrry/claude-remotion-skill"
source_path: "remotion-motion-graphics"
source_commit: "1dcbe5e3fc6cf970bd10d3cc05f0a8a5d19d0383"
snapshot_date: "2026-10-12"
license: "MIT"
copyright: "Copyright (c) 2025 haidrrrry"
upstream_files: 4
upstream_bytes: 23240
files:
  - path: "SKILL.md"
    sha256: "f5547417e7cdb0b65a075e48107639a24253276877babebbb5f1cbb8e7991255"
  - path: "references/design-rules.md"
    sha256: "cd101a35bb81c4ab58871a7514216a508d355ea65332d682214012952c1489f9"
  - path: "references/motion-patterns.md"
    sha256: "3499916cdf80226fe3ed53a367dcb072088d08b40494314eb7c38c2f8aaca939"
  - path: "assets/theme.ts"
    sha256: "690a8ce4440be897781df3baeba1e89b8c30797cb05354d279e7eb69a5b6da58"
---

# remotion-motion-graphics (haidrrrry) source provenance

Manual update: checkout the pinned commit; review the full file set and license; reject symlinks, non-Markdown files outside assets/, unsafe instructions, and absolute filesystem references; regenerate this ledger; update README; run the required Go tests.

The reviewer examined the complete 4-file set at pinned commit `1dcbe5e3fc6cf970bd10d3cc05f0a8a5d19d0383`. Frontmatter was normalized to name `dotagent:haidrrrry:remotion-motion-graphics`, vendor `haidrrrry`, category `Documents & Content`, license `MIT`; the single-line description was kept verbatim and no argument-hint was added (no $ARGUMENTS dispatch). No body adaptations were made. `assets/theme.ts` (1.2 KB theme template, required at runtime — every workflow copies it into `src/theme.ts` as the single source of truth for colors, easings, and springs) is plain TypeScript with no network or credential use. The skill shells out only to local commands (`npm install`, `npx remotion render`/`still`, `which`/`ls` browser probes, `ffmpeg`/`ffprobe` frame extraction), with no network URLs (only an SVG-data-URI XML namespace), no credentials, and no self-update behavior. No remote prompt loading, credential collection/exfiltration, or unsafe command instructions were found. The MIT license notice reads `Copyright (c) 2025 haidrrrry`.
