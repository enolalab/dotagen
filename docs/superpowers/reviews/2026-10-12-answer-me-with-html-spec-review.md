# Spec Review: answer-me-with-html built-in skill

**Mode:** Focused
**Scope:** Full spec (single-phase, no phased sections)
**Spec:** `docs/superpowers/specs/2026-10-12-answer-me-with-html-design.md`
**Base:** branch `feat/answer-me-with-html-skill`, pre-plan
**Reviewers:** Technical + Security (direct bounded review, no subagents — spec is small and all referenced code was already inspected)

## Verdict: Approved with Follow-ups

The spec follows the merged Hallmark precedent exactly (pinned snapshot + `SOURCE.md` manifest + mirror tests), requires no runtime code changes, and makes its one intentional content adaptation explicit. Security review of the 799 KB `am.mjs` CLI is recorded in the spec with bounded local-only process spawning and throttled/opt-in network use. Two non-blocking follow-ups below; the spec is ready for planning.

Strengths: (1) Snapshot rules pin an immutable commit with hash-enforced manifest, mirroring a proven pattern. (2) The `${CLAUDE_SKILL_DIR}` decision is evidence-backed — all 8 adapters are directory-based and upstream already documents the fallback. (3) Non-goals explicitly exclude updater machinery and non-skill repo content.

## Blocking Findings

None.

## Follow-ups

1. **Name the sync-test platform(s) in the plan** — Minor — Blocking: no
   - Evidence: Validation §5 says "at least one platform".
   - Impact: none on acceptance minimum; naming concrete platforms (suggested: `claude-code` where `${CLAUDE_SKILL_DIR}` resolves natively, plus one other to prove the directory fallback) makes the plan's test step unambiguous.
   - Minimal fix: plan picks the platform(s); no spec change required.

2. **Fix the exact `settings.md` adaptation wording in the plan** — Minor — Blocking: no
   - Evidence: Scope says "add one line" for the Dotagent update path without fixing the sentence.
   - Impact: plan author writes one sentence; must stay one line and be recorded in `SOURCE.md`.
   - Minimal fix: plan includes the literal line; no spec change required.

## Coverage and Resolution

- Goal/boundary (snapshot 4 files, pinned commit, MIT) → Scope, Snapshot rules → covered
- `${CLAUDE_SKILL_DIR}` multi-platform behavior → Scope, Architecture → covered (verbatim + fallback rationale)
- `scripts/am.mjs` size/executability justification → Scope, Snapshot rules review notes → covered
- Trust boundary (disabled by default, opt-in enable, no auto-update) → Goal, Non-goals → covered
- Docs/count updates (README 843/60, Frontend & UI 25, CATALOG EN+VI, website check) → Documentation → covered
- Acceptance contract (discovery, digests, metadata, init, sync) → Validation → covered
