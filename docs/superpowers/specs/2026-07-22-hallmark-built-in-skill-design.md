# Hallmark built-in skill design

## Goal

Package the MIT-licensed Hallmark design skill from `Nutlope/hallmark` as a
Dotagent built-in skill. It must be available after `dotagen init` but remain
disabled until the user assigns targets in `.dotagen/config.yaml`.

## Scope

- Add a point-in-time snapshot of the Hallmark skill and its required
  `references/` files under `skillsrc/data/dotagent-nutlope-hallmark/`.
- Rename the skill frontmatter name to `dotagent:nutlope:hallmark` while
  retaining the upstream instructions and relative reference links.
- Keep the snapshot manual: do not alter `scripts/fetch-official-skills.py` or
  introduce a network dependency for builds, installs, or runtime use.
- Update public catalog documentation and built-in-skill counts to include the
  Nutlope vendor and Hallmark in the Frontend & UI category.
- Add focused tests covering embedded discovery, copied reference files, and
  default disabled configuration.

## Non-goals

- Automatically checking, downloading, or updating the upstream Hallmark
  repository.
- Bundling Hallmark's website, demos, or other development-only repository
  content.
- Enabling Hallmark automatically for any platform.

## Architecture and data flow

`skillsrc.DefaultSkills` embeds all contents of `skillsrc/data`. The new
`dotagent-nutlope-hallmark` directory therefore becomes discoverable through
`skillsrc.ListSkills()` without a runtime code change. During `dotagen init`,
`runInit` copies every embedded file from the skill directory into
`~/.dotagen/skills/dotagent-nutlope-hallmark/` and writes a matching config
entry with `targets: []`.

The snapshot preserves the layout expected by Hallmark:

```text
skillsrc/data/dotagent-nutlope-hallmark/
├── SKILL.md
└── references/
    └── ... upstream reference files ...
```

This layout keeps relative links from `SKILL.md` valid after initialization and
allows all supported platform renderers to consume the same source material.

## Snapshot rules

Import only `skills/hallmark/SKILL.md` and files it requires below
`skills/hallmark/references/` from the upstream `main` branch at integration
time. The upstream source is MIT-licensed. The only intentional content change
is the frontmatter `name`, which follows Dotagent's public namespace
convention: `dotagent:nutlope:hallmark`.

If a required source file is binary, too large for the repository's embedded
skill convention, or contains an absolute path that prevents use after init,
stop and surface it for a follow-up decision. Do not silently omit required
references or rewrite Hallmark's operational guidance.

## Documentation

Update `README.md` to reflect the new total built-in skill and vendor counts,
the Frontend & UI category count, and a Nutlope vendor entry. Update
`docs/CATALOG.vi.md` with an entry for `dotagent:nutlope:hallmark` that
describes its anti-AI-slop UI/design workflow and appropriate use cases.

## Validation

Add or extend Go tests to verify that:

1. `skillsrc.ListSkills()` returns `dotagent-nutlope-hallmark`.
2. The embedded skill exposes `SKILL.md` and the expected reference files.
3. The frontmatter identifies the skill as `dotagent:nutlope:hallmark`.
4. `runInit` copies the skill layout and emits the skill's config entry with
   `targets: []`.

Run the affected package tests and the full Go test suite. Keep unrelated
working-tree changes untouched.
