---
name: "dotagent:enolalabs:plan-review"
description: "Review an implementation plan from multiple software development perspectives using specialized subagents. Use after writing-plans produces a plan, before executing it."
category: "Developer Tools"
vendor: "enolalabs"
---

# Plan Review

Multi-perspective plan review using specialized subagents. Each reviewer examines the implementation plan from their domain expertise, then findings are consolidated into a verdict with actionable fixes.

## When to Use

After `superpowers:writing-plans` produces a plan file, before executing it (either inline or via `superpowers:subagent-driven-development`).

**Typical flow:**
```
brainstorming → spec-review → writing-plans → plan-review → implementation
```

## Process

### Step 1: Locate the Plan

- Auto-scan `docs/superpowers/plans/` for `*.md` files
- If exactly one plan found → use it
- If multiple found → ask user which one (multiple-choice with file dates)
- If none found → ask user for the path

Read the plan content. Also read the original spec if referenced in the plan header.

### Step 2: Detect Tech Stack

Follow the detection rules in [subagent-mapping.md](subagent-mapping.md).

Scan the project root for config files and scan the plan content for technology keywords. The plan header usually contains a `**Tech Stack:**` field — use that as a starting point.

Present the detected tech stack to the user for confirmation:

```
Detected tech stack (from plan + project):
  Language:  Go (go.mod found)
  Frontend:  React (package.json)
  Database:  PostgreSQL (plan header)
  Infra:     Kubernetes (plan mentions helm charts)

Is this correct?
A) ⭐ Yes, proceed with these (recommended)
B) No, let me adjust
```

### Step 3: Ask User Which Review Groups

Present the 5 review groups as a multiple-choice question:

```
Which review groups to run?

A) ⭐ All 5 groups (recommended)
   Example: Technical + Performance + Security + Process + Product — comprehensive review

B) Technical + Security only
   Example: Focus on task structure and vulnerability coverage

C) Technical only (spec coverage + task quality)
   Example: Focus on plan completeness and code quality

D) Let me pick individually
   Example: I'll select specific groups from the full list

Subagents that will be dispatched (auto-selected for your Go + React project):
  Technical:   golang-pro, react-specialist
  Performance: performance-engineer
  Security:    security-auditor
  Process:     devops-engineer
  Product:     product-manager
```

If the user picks D, show all 5 groups individually.

### Step 4: Dispatch Reviewer Subagents

For each selected review group, dispatch a subagent:

1. Read the reviewer prompt template from `reviewers/<group>.md`
2. Fill in the plan content, spec content (if available), and tech stack context
3. Dispatch using the subagent type determined in Step 2
4. If the specialized subagent is not available, use `general-purpose`

Each subagent receives:
- Its role description from the reviewer template
- The full plan content
- The original spec content (for spec coverage checks)
- The detected tech stack
- Instructions to output findings by severity (Critical / Important / Minor)

### Step 5: Consolidate Report

Merge all subagent findings into a single review report. See Output Format below.

Calculate the overall verdict:

| Verdict | Condition |
|---------|-----------|
| **Approved** | 0 Critical, 0 Important |
| **Needs Changes** | Any Critical or Important findings |
| **Rejected** | Fundamental plan flaws (spec coverage gaps, impossible task ordering) |

### Step 6: Present Verdict and Report

Display the consolidated report to the user, then save it:

```
docs/superpowers/reviews/YYYY-MM-DD-<topic>-plan-review.md
```

### Step 7: Fix Flow (if Needs Changes or Rejected)

For each Critical and Important finding, in priority order:

**If the fix is clear and unambiguous:**
- Apply the fix directly to the plan file

**If there are multiple valid approaches:**
Ask the user with a multiple-choice question. Format:

```
Finding: [finding title]
[task/section reference in plan]

Which approach do you prefer?

A) ⭐ [Recommended option] (recommended)
   Example: [concrete example of this approach in plan context]
   Best for: [when to choose this]

B) [Alternative option]
   Example: [concrete example]
   Best for: [when to choose this]

C) [Another alternative]
   Example: [concrete example]
   Best for: [when to choose this]

D) Skip this finding
   Example: Leave the plan as-is, address during implementation
```

Rules for multiple-choice questions:
- Always mark the recommended option with a star icon
- Every option must have a concrete example in plan context (task steps, file paths, test code)
- Limit to 3-4 options (plus skip)
- If the user selects skip, note it and move on

**After all fixes are applied:**
- Commit the updated plan with message: `fix: apply plan review findings`
- Offer to re-run the review (user's choice)

### Step 8: Transition

If verdict is Approved:
- Suggest proceeding to execution (`superpowers:subagent-driven-development` or `superpowers:executing-plans`)

If verdict is Needs Changes and fixes were applied:
- Offer to re-review, or proceed if user is satisfied

## Output Format

```markdown
# Plan Review: [Feature Name]

**Date:** YYYY-MM-DD
**Plan:** `path/to/plan.md`
**Spec:** `path/to/spec.md` (if referenced)
**Tech Stack:** Go, React, PostgreSQL, Kubernetes
**Reviewers:** golang-pro, react-specialist, performance-engineer, security-auditor, devops-engineer, product-manager

---

## Verdict: [Approved / Needs Changes / Rejected]

**Summary:** [1-2 sentence overall assessment]

**Finding counts:** X Critical, Y Important, Z Minor

**Spec coverage:** X of Y requirements have corresponding tasks (Z gaps)

---

## Findings

### [Group Icon] Group Name (reviewer agents)

#### Critical (Must Fix)
1. **[Finding title]**
   - Task/Section: [plan reference]
   - Issue: [what's wrong]
   - Impact: [why it matters during implementation]
   - Recommended Fix: [how to fix]

#### Important (Should Fix)
2. **[Finding title]**
   ...

#### Minor (Nice to Have)
3. **[Finding title]**
   ...

---

## Spec Coverage Gaps
[List of spec requirements with no corresponding plan task, if any]

## Strengths
[What the plan does well — task structure, code quality, test coverage]

## Recommendations
[Improvements for plan execution quality]
```

## Key Principles

- **Never skip the user choice step** — always ask which groups to run
- **Never auto-apply ambiguous fixes** — always ask the user with multiple-choice
- **Every multiple-choice option needs a concrete example in plan context**
- **Mark recommended options clearly**
- **Commit only after all fixes are applied** — not after each individual fix
- **Be specific in findings** — reference task numbers and step numbers, not vague "improve the plan"
- **Check spec coverage** — every spec requirement must map to at least one task
- **Check for placeholders** — "TBD", "TODO", "implement later" are Critical findings
- **Check task interfaces** — types and function signatures must be consistent across tasks
- **Acknowledge strengths** before listing issues
