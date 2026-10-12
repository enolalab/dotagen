# Motion-graphics built-in skills design (haidrrrry + fernandokaraka)

## Goal

Package two MIT-licensed Remotion motion-graphics skills as Dotagent
built-in skills: `haidrrrry/claude-remotion-skill` (professional studio
workflow: easing, stagger, grading, captions, frame-verified renders) and
`fernandokaraka/remotion-motion-graphics-skill` (diagnose-first polish
plus transparent ProRes/PNG overlay export for editors). Both must be
available after `dotagen init` but remain disabled until the user assigns
targets in `.dotagen/config.yaml`. Tracks issue #8.

Both upstreams name their skill `remotion-motion-graphics`; Dotagent's
vendor namespacing (`dotagent:haidrrrry:remotion-motion-graphics` and
`dotagent:fernandokaraka:remotion-motion-graphics`) disambiguates them.

## Scope

- Add a point-in-time snapshot of the haidrrrry skill under
  `skillsrc/data/dotagent-haidrrrry-remotion-motion-graphics/`: upstream
  `SKILL.md`, `references/design-rules.md`,
  `references/motion-patterns.md`, and the required
  `assets/theme.ts` template (4 files, 23240 bytes post-normalization).
  The skill cannot function as designed without `theme.ts` — every
  workflow copies it into `src/theme.ts` as the project's single source
  of truth for colors, easings, and springs — so the snapshot must
  include it.
- Add a point-in-time snapshot of the fernandokaraka skill under
  `skillsrc/data/dotagent-fernandokaraka-remotion-motion-graphics/`:
  upstream `SKILL.md` plus all four files under `references/`
  (`patterns.md`, `polish.md`, `scaffold.md`, `traps.md`) (5 files,
  33243 bytes post-normalization).
- Normalize each skill's frontmatter for Dotagent discovery: `name` is
  `dotagent:<vendor>:remotion-motion-graphics`, `vendor` is `haidrrrry`
  or `fernandokaraka`, `category` is `Documents & Content` (matching the
  bundled `dotagent-remotion-dev-remotion` skill), `license` is `MIT`.
  Keep each upstream single-line `description` (trigger behavior)
  verbatim on one line. Neither upstream defines `argument-hint` (no
  `$ARGUMENTS` dispatch), so none is added.
- Keep both upstream bodies verbatim. No content adaptations are needed:
  neither skill contains self-update commands, absolute filesystem
  paths, or skill-directory variables — all file references
  (`references/…`, `assets/theme.ts`) are relative and Dotagent deploys
  the whole skill directory with relative paths preserved on all 8
  platforms.
- Keep both snapshots manual: do not alter
  `scripts/fetch-official-skills.py` or introduce a network dependency
  for builds, installs, or runtime use.
- Update public catalog documentation and built-in-skill counts to
  include the two new vendors and skills in the Documents & Content
  category.
- Add focused tests covering embedded discovery, copied reference
  files, default disabled configuration, metadata, snapshot integrity,
  and size for both skills.

## Non-goals

- Automatically checking, downloading, or updating either upstream
  repository.
- Bundling the haidrrrry `examples/` project, demo media (`demo.mp4`,
  `demo.gif`, `examples/videos/`), the `remotion-motion-graphics.skill`
  zip install artifact, `scripts/build-skill.sh`, or repo-only docs
  (`README.md`, `CONTRIBUTING.md`); or the fernandokaraka repo-level
  `README.md`. Only the 4 + 5 files under the upstream skill
  directories are imported.
- Merging the two skills into one: they cover distinct crafts (studio
  polish workflow vs diagnose-first rules plus alpha-channel export).
- Enabling either skill automatically for any platform.
- Rewriting skill content per platform or adding engine-side variable
  substitution.

## Architecture and data flow

`skillsrc.DefaultSkills` embeds all contents of `skillsrc/data`. The two
new directories therefore become discoverable through
`skillsrc.ListSkills()` without a runtime code change. During `dotagen
init`, `runInit` copies every embedded file from each skill directory
into `~/.dotagen/skills/<name>/` and writes matching config entries
with `targets: []`.

The snapshots preserve the layouts expected by the skills:

```text
skillsrc/data/dotagent-haidrrrry-remotion-motion-graphics/
├── SKILL.md
├── SOURCE.md
├── assets/
│   └── theme.ts
└── references/
    ├── design-rules.md
    └── motion-patterns.md

skillsrc/data/dotagent-fernandokaraka-remotion-motion-graphics/
├── SKILL.md
├── SOURCE.md
└── references/
    ├── patterns.md
    ├── polish.md
    ├── scaffold.md
    └── traps.md
```

On `dotagen sync`, the engine renders `SKILL.md` per platform and copies
every reference file (including `assets/theme.ts` and `SOURCE.md`) into
`.generated/<platform>/skills/<name>/`, preserving relative paths, then
symlinks that directory into the platform skill path. The relative
`references/…` and `assets/theme.ts` mentions therefore resolve on all
8 platforms. All current platform adapters are directory-based; no
adapter uses the single-file `Skill.ContentWithReferences` fallback
today.

No engine, parser, or adapter code changes are required:
`collectReferences` already collects all files except the top-level
`SKILL.md` (any subdirectory, any extension), and `langFromExt` maps
`.ts` to a `typescript` fence for the unused single-file fallback.

## Snapshot rules

Import the haidrrrry files from immutable commit
`1dcbe5e3fc6cf970bd10d3cc05f0a8a5d19d0383` on
`https://github.com/haidrrrry/claude-remotion-skill` (`main`,
2026-08-12, source directory `remotion-motion-graphics`), and the
fernandokaraka files from immutable commit
`1fc286924c68260b7945f1f29e474b986446b70d` on
`https://github.com/fernandokaraka/remotion-motion-graphics-skill`
(`main`, 2026-07-17, source directory
`skills/remotion-motion-graphics`). Add a committed `SOURCE.md`
alongside each snapshot that records the repository URL, source
directory, commit SHA, snapshot date, MIT license/copyright notice, the
exact intentional frontmatter normalization (no body adaptations),
complete imported path list, and SHA-256 digest of each imported file.
Each manifest is the source of truth for its snapshot's file count and
total byte size; tests must enforce those recorded values
(haidrrrry: 4 files, 23240 bytes; fernandokaraka: 5 files, 33243
bytes).

Before merging a new snapshot, a maintainer must fetch the pinned
revision, review the changed file set and manifest, confirm the MIT
license and attribution, and inspect imported content for remote prompt
loading, credential collection/exfiltration instructions, and unsafe
command execution. They then update the manifest and catalog counts, run
the named Go tests, and review the resulting diff. This is the complete
manual update procedure; no updater or network dependency is added to
Dotagent.

Review notes for these snapshots (pinned commits above): the haidrrrry
skill shells out only to local commands (`npm install`, `npx remotion
render`/`still`, `which`/`ls` browser probes, `ffmpeg`/`ffprobe` frame
extraction), with no network URLs (only an SVG-data-URI XML namespace),
no credentials, and no self-update behavior. The fernandokaraka skill
shells out only to `npx remotion render`/`still` and `npm run studio`,
with no network use and no credential handling. No remote prompt
loading, credential harvesting, or exfiltration was found in either
skill.

If a required source file is binary, exceeds the snapshot's reviewed
manifest size, or contains an absolute path that prevents use after
init, the import or PR validation must fail before merge and report the
path and reason. Do not silently omit required references or rewrite
the skills' operational guidance.

## Documentation

Update `README.md` to reflect the new total built-in skill (843 -> 845)
and vendor (60 -> 62) counts, the Documents & Content category count
(18 -> 20), haidrrrry and fernandokaraka vendor-table entries, and the
pinned-snapshot sentence so it covers Hallmark, answer-me-with-html,
and both motion-graphics skills. Update the scope-note counts in
`docs/CATALOG.md` and `docs/CATALOG.vi.md` (843 -> 845, 60 -> 62),
which defer the full list to the README. Check `website/` for hardcoded
skill/vendor counts and update them if present.

## Validation

Add `skillsrc/haidrrrry_motion_graphics_snapshot_test.go` and
`skillsrc/fernandokaraka_motion_graphics_snapshot_test.go`, mirroring
the Hallmark snapshot tests, to verify for each skill that:

1. `skillsrc.ListSkills()` returns the skill directory name.
2. The embedded skill and the `runInit` output each expose every path
   listed in its `SOURCE.md`; their SHA-256 digests, file count, and
   total bytes match the manifest. The haidrrrry test additionally
   allows the non-Markdown path `assets/theme.ts` (allowed roots:
   `SKILL.md`, `references/`, `assets/`); the fernandokaraka snapshot
   is Markdown-only (allowed roots: `SKILL.md`, `references/`).
3. The frontmatter identifies the skill as
   `dotagent:<vendor>:remotion-motion-graphics`, with the normalized
   vendor, Documents & Content category, verbatim description, and MIT
   license metadata.
4. `runInit` copies the skill layout and emits the skill's config entry
   with `targets: []`.
5. `dotagen sync` output for at least one platform contains the rendered
   `SKILL.md` plus `references/` (and `assets/theme.ts` for haidrrrry)
   with identical bytes.

Run `go test ./skillsrc/... ./internal/...` and `go test ./...`; keep
unrelated working-tree changes untouched. CI is billing-blocked, so
verify with full local test runs instead.
