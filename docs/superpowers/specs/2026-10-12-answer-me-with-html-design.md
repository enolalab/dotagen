# answer-me-with-html built-in skill design

## Goal

Package the MIT-licensed answer-me-with-html skill from
`QingYunA/answer-me-with-html` as a Dotagent built-in skill. It must be
available after `dotagen init` but remain disabled until the user assigns
targets in `.dotagen/config.yaml`. Tracks issue #6.

## Scope

- Add a point-in-time snapshot of the answer-me-with-html skill under
  `skillsrc/data/dotagent-qingyuna-answer-me-with-html/`: upstream
  `SKILL.md`, `references/settings.md`, `references/video.md`, and the
  required `scripts/am.mjs` CLI (single file, ~799 KB, Node.js 20+, zero
  dependencies). The skill cannot function without `am.mjs` — every
  workflow invokes `node scripts/am.mjs` — so the snapshot must include
  it despite its size.
- Normalize the skill frontmatter for Dotagent discovery: `name` is
  `dotagent:qingyuna:answer-me-with-html`, `vendor` is `qingyuna`,
  `category` is `Frontend & UI`, `license` is `MIT`. Keep the upstream
  `description` (trigger behavior) and `argument-hint` (`config | clean |
  update` dispatch via `$ARGUMENTS`) verbatim.
- Keep the upstream operational instructions verbatim, including
  `${CLAUDE_SKILL_DIR}` references: the upstream text already tells
  non-Claude agents to substitute the absolute path of the directory
  containing `SKILL.md`, and Dotagent deploys the whole skill directory
  (SKILL.md plus references, relative paths preserved) on all 8
  platforms, so that fallback works everywhere without edits.
- Add one line to `references/settings.md` documenting the Dotagent
  update path (wait for a new pinned snapshot; do not run the
  npx/plugin/git-clone update commands). Record this adaptation in
  `SOURCE.md`.
- Keep the snapshot manual: do not alter `scripts/fetch-official-skills.py`
  or introduce a network dependency for builds, installs, or runtime use.
- Update public catalog documentation and built-in-skill counts to include
  the QingYunA vendor and the skill in the Frontend & UI category.
- Add focused tests covering embedded discovery, copied reference files,
  default disabled configuration, metadata, snapshot integrity, and size.

## Non-goals

- Automatically checking, downloading, or updating the upstream
  answer-me-with-html repository.
- Bundling the upstream website, demos, benchmarks, `bin/`, `commands/`,
  or other development-only repository content (only the 4 files under
  `skills/answer-me-with-html/` are imported).
- Enabling the skill automatically for any platform.
- Rewriting `${CLAUDE_SKILL_DIR}` per platform or adding engine-side
  variable substitution.

## Architecture and data flow

`skillsrc.DefaultSkills` embeds all contents of `skillsrc/data`. The new
`dotagent-qingyuna-answer-me-with-html` directory therefore becomes
discoverable through `skillsrc.ListSkills()` without a runtime code change.
During `dotagen init`, `runInit` copies every embedded file from the skill
directory into `~/.dotagen/skills/dotagent-qingyuna-answer-me-with-html/`
and writes a matching config entry with `targets: []`.

The snapshot preserves the layout expected by the skill:

```text
skillsrc/data/dotagent-qingyuna-answer-me-with-html/
├── SKILL.md
├── SOURCE.md
├── references/
│   ├── settings.md
│   └── video.md
└── scripts/
    └── am.mjs
```

On `dotagen sync`, the engine renders `SKILL.md` per platform and copies
every reference file (including `scripts/am.mjs` and `SOURCE.md`) into
`.generated/<platform>/skills/<name>/`, preserving relative paths, then
symlinks that directory into the platform skill path. The `node
"<skill-dir>/scripts/am.mjs"` invocation therefore resolves on all 8
platforms. All current platform adapters are directory-based; no adapter
uses the single-file `Skill.ContentWithReferences` fallback today.

No engine, parser, or adapter code changes are required: `collectReferences`
already collects all files except the top-level `SKILL.md`, and
`langFromExt` falls back to an unlabeled fence for `.mjs`.

## Snapshot rules

Import only the 4 files under `skills/answer-me-with-html/` from immutable
commit `4cb97d606a25a00ad73a3bedf633d292b395d040` on the upstream
`https://github.com/QingYunA/answer-me-with-html` repository (`main`,
2026-10-12). Add a committed `SOURCE.md` alongside the snapshot that
records the repository URL, source directory, commit SHA, snapshot date,
MIT license/copyright notice, exact intentional frontmatter normalization
and the one-line `settings.md` adaptation, complete imported path list,
and SHA-256 digest of each imported file. The manifest is the source of
truth for the snapshot's file count and total byte size; tests must enforce
those recorded values.

Before merging a new snapshot, a maintainer must fetch the pinned revision,
review the changed file set and manifest, confirm the MIT license and
attribution, and inspect imported content for remote prompt loading,
credential collection/exfiltration instructions, and unsafe command
execution. They then update the manifest and catalog counts, run the named
Go tests, and review the resulting diff. This is the complete manual update
procedure; no updater or network dependency is added to Dotagent.

Review notes for this snapshot (pinned commit above): `am.mjs` spawns only
local commands (`which`/`where` probes, `say`/`espeak-ng` voice lists,
browser open, headless Chrome screenshots, `ffmpeg` video export, and a
detached self update-check). Its only network use is a throttled
(7-day, 5s timeout) version check against the upstream `package.json`
that prints a hint (the skill instructs the agent never to update without
user consent), ElevenLabs text-to-speech only when the user configures a
voice key for videos, and localhost `am serve`. No remote prompt loading,
credential harvesting, or exfiltration was found.

If a required source file is binary, exceeds the snapshot's reviewed
manifest size, or contains an absolute path that prevents use after init,
the import or PR validation must fail before merge and report the path and
reason. Do not silently omit required references or rewrite the skill's
operational guidance.

## Documentation

Update `README.md` to reflect the new total built-in skill (842 -> 843)
and vendor (59 -> 60) counts, the Frontend & UI category count (24 -> 25),
a QingYunA vendor-table entry, and the pinned-snapshot sentence so it
covers both Hallmark and answer-me-with-html. Update the scope-note counts
in `docs/CATALOG.md` and `docs/CATALOG.vi.md` (842 -> 843, 59 -> 60),
which defer the full list to the README. Check `website/` for hardcoded
skill/vendor counts and update them if present.

## Validation

Add `skillsrc/answer_me_with_html_snapshot_test.go`, mirroring the Hallmark
snapshot tests, to verify that:

1. `skillsrc.ListSkills()` returns `dotagent-qingyuna-answer-me-with-html`.
2. The embedded skill and the `runInit` output each expose every path listed
   in `SOURCE.md`; their SHA-256 digests, file count, and total bytes match
   the manifest. Unlike the Hallmark test, the allowed non-Markdown path is
   `scripts/am.mjs` (allowed roots: `SKILL.md`, `references/`, `scripts/`).
3. The frontmatter identifies the skill as
   `dotagent:qingyuna:answer-me-with-html`, with the normalized QingYunA,
   Frontend & UI, description, argument-hint, and MIT license metadata.
4. `runInit` copies the skill layout and emits the skill's config entry with
   `targets: []`.
5. `dotagen sync` output for at least one platform contains the rendered
   `SKILL.md` plus `references/` and `scripts/am.mjs` with identical bytes.

Run `go test ./skillsrc/... ./internal/...` and `go test ./...`; keep
unrelated working-tree changes untouched. CI is billing-blocked, so verify
with full local test runs instead.
