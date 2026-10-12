---
source_repository: "https://github.com/QingYunA/answer-me-with-html"
source_path: "skills/answer-me-with-html"
source_commit: "4cb97d606a25a00ad73a3bedf633d292b395d040"
snapshot_date: "2026-10-12"
license: "MIT"
copyright: "Copyright (c) 2026 Answer me with HTML contributors"
upstream_files: 4
upstream_bytes: 822095
files:
  - path: "SKILL.md"
    sha256: "154e42a0a8122880d94f27456c6a39ab69e2b1e8267a0d12297a6bc0ef3cdf23"
  - path: "references/settings.md"
    sha256: "078f9061afa6dcb9535bb3ade704a71c358821dfd6597757cd7ed5cf8d3c0c98"
  - path: "references/video.md"
    sha256: "011468549673cf2553e600a6d87eecb71d18eea75b4ab96375c9e3fef781b9c5"
  - path: "scripts/am.mjs"
    sha256: "098c5d3373a89e88d757ad80ed57f3dfe9773537739d9a8c4425c57455da8045"
---

# answer-me-with-html source provenance

Manual update: checkout the pinned commit; review the full file set and license; reject symlinks, non-Markdown files outside scripts/, unsafe instructions, and absolute filesystem references; regenerate this ledger; update README; run the required Go tests.

The reviewer examined the complete 4-file set at pinned commit `4cb97d606a25a00ad73a3bedf633d292b395d040`. Frontmatter was normalized to name `dotagent:qingyuna:answer-me-with-html`, vendor `qingyuna`, category `Frontend & UI`, license `MIT`; description and argument-hint were kept verbatim. One sentence was appended to the update paragraph of `references/settings.md` documenting the dotagen pinned-snapshot update path. `scripts/am.mjs` (799 KB bundled CLI, required at runtime) spawns only local commands (which/where probes, say/espeak-ng voice lists, browser open, headless Chrome screenshots, ffmpeg video export, and a detached self update-check). Its only network use is a throttled (7-day, 5s timeout) version check against the upstream package.json that prints a hint (the skill instructs the agent never to update without user consent), ElevenLabs text-to-speech only when the user configures a voice key for videos, and localhost am serve. No remote prompt loading, credential collection/exfiltration, or unsafe command instructions were found. The MIT license notice reads `Copyright (c) 2026 Answer me with HTML contributors`.
