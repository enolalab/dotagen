---
name: "dotagent:enolalabs:spec-review"
description: "Review a spec document from multiple software development perspectives using specialized subagents. Use after brainstorming produces a spec, before writing-plans."
category: "Developer Tools"
vendor: "enolalabs"
---

# Spec Review

Multi-perspective spec review using specialized subagents. Each reviewer examines the spec from their domain expertise, then findings are consolidated into a verdict with actionable fixes.

## When to Use

After `superpowers:brainstorming` produces a spec file, before invoking `superpowers:writing-plans`.

**Typical flow:**
```
brainstorming → spec-review → writing-plans → plan-review → implementation
```

## Process

### Step 1: Locate the Spec

- Auto-scan `docs/superpowers/specs/` for `*.md` files
- If exactly one spec found → use it
- If multiple found → ask user which one (multiple-choice with file dates)
- If none found → ask user for the path

Read the spec content. This is the document under review.

### Step 2: Detect Tech Stack

Follow the detection rules in [subagent-mapping.md](subagent-mapping.md).

Scan the project root for config files (`go.mod`, `package.json`, `requirements.txt`, `Cargo.toml`, `*.csproj`, `pom.xml`, `Gemfile`, etc.) and scan the spec content for technology keywords.

Present the detected tech stack to the user for confirmation:

```
Detected tech stack:
  Language:  Go (go.mod found)
  Frontend:  React (package.json, "React" in spec)
  Database:  PostgreSQL (mentioned in spec)
  Infra:     Kubernetes (mentioned in spec)

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
   Example: Focus on architecture soundness and vulnerability detection

C) Security + Performance only
   Example: Focus on bottlenecks and attack vectors

D) Let me pick individually
   Example: I'll select specific groups from the full list

Subagents that will be dispatched (auto-selected for your Go + React project):
  Technical:   golang-pro, react-specialist
  Performance: performance-engineer
  Security:    security-auditor
  Process:     devops-engineer
  Product:     product-manager
```

If the user picks D, show all 5 groups individually with checkboxes.

### Step 4: Dispatch Reviewer Subagents

For each selected review group, dispatch a subagent:

1. Read the reviewer prompt template from `reviewers/<group>.md`
2. Fill in the spec content and tech stack context
3. Dispatch using the subagent type determined in Step 2
4. If the specialized subagent is not available, use `general-purpose`

**Dispatch sequentially or in parallel** depending on platform capabilities. Collect all results before proceeding.

Each subagent receives:
- Its role description from the reviewer template
- The full spec content
- The detected tech stack
- Instructions to output findings by severity (Critical / Important / Minor)

### Step 5: Consolidate Report

Merge all subagent findings into a single review report. See Output Format below.

Calculate the overall verdict:

| Verdict | Condition |
|---------|-----------|
| **Approved** | 0 Critical, 0 Important |
| **Needs Changes** | Any Critical or Important findings |
| **Rejected** | Fundamental architecture or design flaws |

### Step 6: Present Verdict and Report

Display the consolidated report to the user, then save it:

```
docs/superpowers/reviews/YYYY-MM-DD-<topic>-spec-review.md
```

### Step 7: Fix Flow (if Needs Changes or Rejected)

For each Critical and Important finding, in priority order:

**If the fix is clear and unambiguous:**
- Apply the fix directly to the spec file

**If there are multiple valid approaches:**
Ask the user with a multiple-choice question. Format:

```
Finding: [finding title]
[section reference in spec]

Which approach do you prefer?

A) ⭐ [Recommended option] (recommended)
   Example: [concrete example of this approach]
   Best for: [when to choose this]

B) [Alternative option]
   Example: [concrete example]
   Best for: [when to choose this]

C) [Another alternative]
   Example: [concrete example]
   Best for: [when to choose this]

D) Skip this finding
   Example: Leave the spec as-is, address during implementation
```

Rules for multiple-choice questions:
- Always mark the recommended option with a star icon
- Every option must have a concrete example
- Limit to 3-4 options (plus skip)
- If the user selects skip, note it and move on

**After all fixes are applied:**
- Commit the updated spec with message: `fix: apply spec review findings`
- Offer to re-run the review (user's choice)

### Step 8: Transition

If verdict is Approved:
- Suggest proceeding to `superpowers:writing-plans`

If verdict is Needs Changes and fixes were applied:
- Offer to re-review, or proceed if user is satisfied

## Output Format

```markdown
# Spec Review: [Topic]

**Date:** YYYY-MM-DD
**Spec:** `path/to/spec.md`
**Tech Stack:** Go, React, PostgreSQL, Kubernetes
**Reviewers:** golang-pro, react-specialist, performance-engineer, security-auditor, devops-engineer, product-manager

---

## Verdict: [Approved / Needs Changes / Rejected]

**Summary:** [1-2 sentence overall assessment]

**Finding counts:** X Critical, Y Important, Z Minor

---

## Findings

### [Group Icon] Group Name (reviewer agents)

#### Critical (Must Fix)
1. **[Finding title]**
   - Section: [spec section reference]
   - Issue: [what's wrong]
   - Impact: [why it matters]
   - Recommended Fix: [how to fix]

#### Important (Should Fix)
2. **[Finding title]**
   ...

#### Minor (Nice to Have)
3. **[Finding title]**
   ...

---

## Strengths
[What the spec does well — be specific]

## Recommendations
[Improvements that go beyond fixing issues]
```

## Key Principles

- **Never skip the user choice step** — always ask which groups to run
- **Never auto-apply ambiguous fixes** — always ask the user with multiple-choice
- **Every multiple-choice option needs a concrete example**
- **Mark recommended options clearly**
- **Commit only after all fixes are applied** — not after each individual fix
- **Be specific in findings** — reference spec sections, not vague "improve X"
- **Acknowledge strengths** before listing issues — builds trust in the feedback
