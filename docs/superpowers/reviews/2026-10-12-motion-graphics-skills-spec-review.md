# Spec Review: motion-graphics built-in skills (haidrrrry + fernandokaraka)

**Mode:** Focused
**Scope:** Full spec (single-phase, no phased sections)
**Spec:** `docs/superpowers/specs/2026-10-12-motion-graphics-skills-design.md`
**Base:** branch `feat/remotion-motion-graphics-skills`, commit `97c21f4`, pre-plan
**Reviewers:** Technical + Security (direct bounded review, no subagents — spec is small, mirrors merged issue-#6 precedent, and all referenced code was inspected)

## Verdict: Approved with Follow-ups

The spec mirrors the merged answer-me-with-html precedent exactly (pinned snapshot + `SOURCE.md` manifest + mirror tests, no runtime code changes) and resolves the one new risk — both upstreams naming their skill `remotion-motion-graphics` — via vendor namespacing. Every load-bearing technical claim was verified against the tree: category match, base counts, `collectReferences`/`langFromExt` behavior, directory-only adapters, and `runInit` disabled-by-default entries. No spec edits were required. Two non-blocking follow-ups below; the spec is ready for planning.

Strengths: (1) The name-collision decision is explicit and structural — distinct directory names, frontmatter `name`s, and config keys leave no collision surface. (2) The `assets/theme.ts` inclusion is justified as a functional requirement with a size/enforcement contract, not bundled by default. (3) Snapshot rules reuse the proven hash-enforced manifest plus a complete manual update procedure with a fail-closed import gate.

## Blocking Findings

None. No spec text changes were needed.

## Follow-ups

1. **Name the sync-test platform(s) in the plan** — Minor — Blocking: no
   - Evidence: Validation §5 says "at least one platform" (same wording as the issue-#6 spec).
   - Impact: none on acceptance minimum; naming a concrete platform in the plan makes the test step unambiguous.
   - Minimal fix: plan picks the platform(s); no spec change required.

2. **Enumerate every README count location in the plan** — Minor — Blocking: no
   - Evidence: Documentation says "update `README.md`" generically, but counts live in at least five places: catalog intro (`843 skills` from `60 vendors`, pinned-snapshot sentence), category table (`Documents & Content | 18`), vendor table (`View all 60 vendors` + rows), init example (`all 843 built-in skills`), and command table (`with 843 built-in skills`); plus a second pinned-snapshot sentence in Acknowledgments.
   - Impact: plan author must touch all of them (843 -> 845, 60 -> 62, 18 -> 20, two new vendor rows, both pinned-snapshot sentences covering Hallmark, answer-me-with-html, and both motion-graphics skills); missing one breaks count-consistency tests.
   - Minimal fix: plan lists the locations; no spec change required.

## Coverage and Resolution

- Goal/boundary (snapshot 4 + 5 files, pinned commits, MIT, issue #8) → Goal, Scope, Snapshot rules → covered (commits/sizes rest on prior-child local-clone verification; manifest-enforcement tests re-verify at implementation)
- Upstream name collision (`remotion-motion-graphics` x2) → Goal, Scope → covered (vendor-namespaced names, directories, config keys)
- Category `Documents & Content` → Scope → covered (verified: `dotagent-remotion-dev-remotion` SKILL.md frontmatter)
- Verbatim bodies, no adaptations → Scope → covered (prior-child scan: relative refs only, no self-update/absolute-path/skill-dir vars; `assets/theme.ts` precedented by `scripts/am.mjs` non-Markdown reference)
- No engine changes (`collectReferences` any-subdir/any-ext, `.ts` → `typescript`, no adapter uses `ContentWithReferences`) → Architecture → covered (verified in `internal/skill/parser.go`, `internal/skill/types.go`; only test callers)
- Disabled by default (`targets: []`) → Goal, Non-goals, Validation → covered (verified in `internal/cli/init.go`)
- Docs/count updates (README 845/62, Documents & Content 20, CATALOG EN+VI, website check) → Documentation → covered (base 843/60/18 verified on this branch post-#6-merge; `website/` inspected: no hardcoded counts, only unrelated match in `website/docs/cli/manage-skills.md`)
- Trust boundary (no auto-update, manual snapshots, fail-closed import gate, recorded command/network review notes) → Snapshot rules, Non-goals → covered
- Acceptance contract (discovery, digests, metadata, init, sync) → Validation → covered (`SOURCE.md` + Hallmark/`answer_me_with_html` mirror-test precedent verified in `skillsrc/`)
