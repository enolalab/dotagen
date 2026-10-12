# Plan Review: motion-graphics built-in skills (haidrrrry + fernandokaraka)

**Mode:** Focused
**Scope:** Full plan (7 tasks, single execution boundary)
**Plan:** `docs/superpowers/plans/2026-10-12-motion-graphics-skills.md`
**Spec:** `docs/superpowers/specs/2026-10-12-motion-graphics-skills-design.md` (Validation + Documentation sections)
**Base:** branch `feat/remotion-motion-graphics-skills`, commit `1a7b48b`, pre-execution
**Reviewers:** Technical (direct bounded review, no subagents — plan mirrors the merged issue-#6 precedent and every load-bearing claim was verified live, including fresh upstream downloads at the pinned SHAs)

## Verdict: Approved (P1 fixed during review, verified below)

The plan is executable and fully specified (exact bytes, hashes, file contents, commands). One blocking finding (P1, unescaped `&` in the Task 6 category-table sed) was fixed in the plan immediately and the fixed command verified on a README copy. One minor hardening fix (P2, verification grep missed singular `60 vendor`) was applied in the same pass. Everything else was ready as written.

## Differential verification of P1 + P2

- Fixed sed `s/| Documents & Content | 18 |/| Documents \& Content | 20 |/` on a README copy yields exactly `| Documents & Content | 20 |` at line 141 (previously mangled to `| Documents | Documents & Content | 18 | Content | 20 |`). Resolved.
- Widened final grep (`60 vendor` without the `s`) catches all stale spots on unmodified files, including the singular `60 vendor` in `docs/CATALOG.vi.md:5`. Resolved.
- No new blockers introduced by the two one-line fixes. No re-review of unchanged tasks needed.

Strengths: (1) Every hash/byte count reproduced exactly from live upstream downloads at the pinned SHAs, and download integrity is verified before normalization. (2) The sync test covers both skills on both a native (`claude-code`) and a fallback (`cursor`) platform, closing spec-review follow-up F1. (3) The Task 7 smoke test already carries the corrected `.dotagen/.generated` path that the issue-#6 review had to fix.

## Blocking Findings

1. **[P1] Category-table sed corrupts the README row** — Important — Blocking: yes
   - Evidence: Task 6 Step 1 runs `sed -i 's/| Documents & Content | 18 |/| Documents & Content | 20 |/'`; in sed, `&` in the replacement expands to the whole match. Dry-run on a README copy produced `| Documents | Documents & Content | 18 | Content | 20 |` at line 141 instead of `| Documents & Content | 20 |`.
   - Impact: executing the plan as written corrupts the category table; the final `counts clean` grep does not catch it.
   - Minimal fix: escape the `&` in the replacement (`\&`). Applied to the plan and re-verified (see above).

## Follow-ups

1. **[P2] Final count grep missed singular `60 vendor`** — Minor — Blocking: no
   - Evidence: Task 6 Step 1's gate grep looked for `60 vendors` (plural), but `docs/CATALOG.vi.md:5` uses singular `60 vendor`; a failed vi-sed would have passed the gate silently.
   - Impact: stale Vietnamese catalog count could slip through undetected.
   - Minimal fix: drop the trailing `s` (`60 vendor` matches both forms). Applied to the plan and re-verified (see above). No other `&` occurrences exist in the remaining sed replacements.

## Coverage and Resolution

- Spec Validation 1–2 (discovery, digests, file counts, byte totals) → Task 3 → covered (hashes/bytes re-verified live: H 7995/4332/9763/1150, F 6747/10933/4544/5249/5770; `manifestInt`/`manifestMap`/`ListSkills`/`ReadSkillFile`/`ListSkillFiles` all exist as named)
- Spec Validation 3 (metadata, no argument-hint) → Task 3 → covered (upstream verified: 1 description line each, no `argument-hint`, no `$ARGUMENTS`)
- Spec Validation 4 (init copy + disabled) → Task 4 → covered (`runInit(home)` 4-tuple and all 8 claimed imports verified in `internal/cli/init_test.go`)
- Spec Validation 5 (sync output, at least one platform) → Task 5 (claude-code + cursor) → covered (imports, `StringOrSlice{"all"}`, `RenderAllSkills` shape mirrored verbatim from the passing answer-me-with-html test; both markers verified in upstream bodies — line 9 and line 17, not frontmatter; `SOURCE.md` in refs matches precedent)
- Spec Documentation (README 845/62, Documents & Content 20, vendor rows, both pinned-snapshot sentences, CATALOG EN+VI, website check) → Task 6 → covered (all 9 README spots + both CATALOG scope notes dry-run green on copies, including both python `assert count == 1` blocks; `Testing & QA | 60 |` and `55 organizations` untouched; no Go test asserts hardcoded counts)
- Spec-review follow-up F1 (name platforms) → Task 5 → resolved
- Spec-review follow-up F2 (enumerate count locations) → Task 6 → resolved
- Task 7 smoke test paths → verified (`RenderAllSkills` writes `<dotgenDir>/.generated`, `GetProjectDir()` returns `$HOME`, `sync [target]` registered with `claude-code` in `ValidTargets`; `.claude/skills` symlink path matches the issue-#6 verified precedent)
- Upstream trust claims → spot-verified (MIT licenses `Copyright (c) 2025 haidrrrry` / `Copyright (c) 2026 Fernando Karakanian Melo`; hygiene scan clean on all 9 files; `go test ./...` green at review time)
