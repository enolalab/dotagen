# answer-me-with-html Built-in Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Vendor the MIT-licensed answer-me-with-html skill as a pinned, hash-verified built-in skill (issue #6).

**Architecture:** No runtime code changes. Add `skillsrc/data/dotagent-qingyuna-answer-me-with-html/` (4 upstream files + `SOURCE.md` manifest); the existing `go:embed` + `runInit` copy + `RenderAllSkills` symlink flow picks it up. Mirror the Hallmark snapshot tests, init test, docs-count updates, and add one sync test.

**Tech Stack:** Go 1.26+, testify, `go test ./...`, git.

## Global Constraints

- Pinned upstream commit: `4cb97d606a25a00ad73a3bedf633d292b395d040` (`main`, 2026-10-12). All downloads use this SHA in the raw URL, never `main`.
- Skill directory: `skillsrc/data/dotagent-qingyuna-answer-me-with-html/`; frontmatter `name: "dotagent:qingyuna:answer-me-with-html"`, `vendor: "qingyuna"`, `category: "Frontend & UI"`, `license: MIT`.
- Upstream `description` and `argument-hint` kept verbatim; body kept verbatim; only intentional edits are the frontmatter normalization and one appended sentence in `references/settings.md`.
- Snapshot manifest: 4 files, 822095 bytes total. No network dependency added to builds, installs, or runtime.
- Skill stays disabled by default (`targets: []`).
- CI is billing-blocked: verify with full local runs (`go test ./...`, manual `init`+`sync` smoke test).

---

### Task 1: Vendor the pinned snapshot

**Files:**
- Create: `skillsrc/data/dotagent-qingyuna-answer-me-with-html/SKILL.md`
- Create: `skillsrc/data/dotagent-qingyuna-answer-me-with-html/references/settings.md`
- Create: `skillsrc/data/dotagent-qingyuna-answer-me-with-html/references/video.md`
- Create: `skillsrc/data/dotagent-qingyuna-answer-me-with-html/scripts/am.mjs`
- Create: `skillsrc/data/dotagent-qingyuna-answer-me-with-html/SOURCE.md`

**Interfaces:**
- Consumes: upstream raw files at pinned commit (URLs below).
- Produces: 4 snapshot files with exact bytes/hashes below + `SOURCE.md` manifest consumed by Task 2 tests.

Expected final bytes and SHA-256 (post-normalization):

| Path | Bytes | SHA-256 |
|---|---|---|
| `SKILL.md` | 17647 | `154e42a0a8122880d94f27456c6a39ab69e2b1e8267a0d12297a6bc0ef3cdf23` |
| `references/settings.md` | 1970 | `078f9061afa6dcb9535bb3ade704a71c358821dfd6597757cd7ed5cf8d3c0c98` |
| `references/video.md` | 3603 | `011468549673cf2553e600a6d87eecb71d18eea75b4ab96375c9e3fef781b9c5` |
| `scripts/am.mjs` | 798875 | `098c5d3373a89e88d757ad80ed57f3dfe9773537739d9a8c4425c57455da8045` |

- [ ] **Step 1: Create directories and download the 4 pinned files**

Run:

```bash
D=skillsrc/data/dotagent-qingyuna-answer-me-with-html
mkdir -p $D/references $D/scripts
B=https://raw.githubusercontent.com/QingYunA/answer-me-with-html/4cb97d606a25a00ad73a3bedf633d292b395d040/skills/answer-me-with-html
curl -sL -o /tmp/amh-SKILL.md "$B/SKILL.md"
curl -sL -o /tmp/amh-settings.md "$B/references/settings.md"
curl -sL -o $D/references/video.md "$B/references/video.md"
curl -sL -o $D/scripts/am.mjs "$B/scripts/am.mjs"
```

Expected: 4 files downloaded, no curl errors.

- [ ] **Step 2: Verify the two verbatim files match their known hashes**

Run:

```bash
sha256sum $D/references/video.md $D/scripts/am.mjs
```

Expected output:

```
011468549673cf2553e600a6d87eecb71d18eea75b4ab96375c9e3fef781b9c5  skillsrc/data/dotagent-qingyuna-answer-me-with-html/references/video.md
098c5d3373a89e88d757ad80ed57f3dfe9773537739d9a8c4425c57455da8045  skillsrc/data/dotagent-qingyuna-answer-me-with-html/scripts/am.mjs
```

If either hash differs, STOP: the pinned commit moved or the download is corrupt. Do not proceed.

- [ ] **Step 3: Normalize SKILL.md frontmatter and adapt settings.md**

Run this exact script (it copies the multi-line description from upstream byte-for-byte, so no CJK text is retyped):

```bash
D=skillsrc/data/dotagent-qingyuna-answer-me-with-html
python3 - "$D" <<'EOF'
import sys
d = sys.argv[1]
raw = open('/tmp/amh-SKILL.md', encoding='utf-8').read()
assert raw.startswith('---\n'), "upstream SKILL.md lost its frontmatter"
_, fm, body = raw.split('---\n', 2)
desc, cap = [], False
for ln in fm.split('\n'):
    if ln.startswith('description:'):
        cap = True
        continue
    if cap:
        if ln.startswith('  '):
            desc.append(ln)
        else:
            break
assert len(desc) == 11, f"expected 11 description lines, got {len(desc)}"
new_fm = ('---\n'
    'name: "dotagent:qingyuna:answer-me-with-html"\n'
    'description: >-\n' + '\n'.join(desc) + '\n'
    'argument-hint: "[config [key value] | clean | update]"\n'
    'category: "Frontend & UI"\n'
    'vendor: "qingyuna"\n'
    'license: MIT\n'
    '---\n')
open(f'{d}/SKILL.md', 'w', encoding='utf-8').write(new_fm + body)

s = open('/tmp/amh-settings.md', encoding='utf-8').read()
anchor = 'Installed with git clone: run `git pull && npm install` in the repository directory.'
assert anchor in s, "settings.md update paragraph changed upstream"
adapt = (' Installed via dotagen: this skill is a pinned snapshot - tell the user'
         ' to wait for a new dotagen release instead of running any update command.')
open(f'{d}/references/settings.md', 'w', encoding='utf-8').write(s.replace(anchor, anchor + adapt))
print("staged OK")
EOF
```

Expected: prints `staged OK`.

- [ ] **Step 4: Verify all 4 snapshot hashes and byte counts**

Run:

```bash
D=skillsrc/data/dotagent-qingyuna-answer-me-with-html
sha256sum $D/SKILL.md $D/references/settings.md $D/references/video.md $D/scripts/am.mjs
wc -c $D/SKILL.md $D/references/settings.md $D/references/video.md $D/scripts/am.mjs
```

Expected: hashes and byte counts match the table at the top of this task exactly (total 822095).

- [ ] **Step 5: Write SOURCE.md**

Create `skillsrc/data/dotagent-qingyuna-answer-me-with-html/SOURCE.md` with exactly this content:

```markdown
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
```

- [ ] **Step 6: Commit**

```bash
git add skillsrc/data/dotagent-qingyuna-answer-me-with-html
git commit -m "feat: vendor answer-me-with-html skill snapshot (issue #6)"
```

---

### Task 2: Snapshot and metadata tests

**Files:**
- Create: `skillsrc/answer_me_with_html_snapshot_test.go`

**Interfaces:**
- Consumes: Task 1 snapshot files + `SOURCE.md`; existing helpers `skillsrc.ListSkills`, `ReadSkillFile`, `ListSkillFiles`, and `manifestInt`/`manifestMap` from `skillsrc/hallmark_snapshot_test.go` (same package — reuse, do not redefine).
- Produces: `TestAnswerMeWithHtmlSnapshotIsCompleteAndPinned`, `TestAnswerMeWithHtmlSkillMetadata`.

- [ ] **Step 1: Write the test file**

Create `skillsrc/answer_me_with_html_snapshot_test.go` with exactly this content:

```go
package skillsrc

import (
	"crypto/sha256"
	"fmt"
	"reflect"
	"sort"
	"strings"
	"testing"

	"github.com/adrg/frontmatter"
)

const answerMeWithHTMLSkillName = "dotagent-qingyuna-answer-me-with-html"

func TestAnswerMeWithHtmlSnapshotIsCompleteAndPinned(t *testing.T) {
	skills := ListSkills()
	listed := false
	for _, s := range skills {
		if s == answerMeWithHTMLSkillName {
			listed = true
			break
		}
	}
	if !listed {
		t.Fatalf("ListSkills() does not contain %q", answerMeWithHTMLSkillName)
	}

	raw, err := ReadSkillFile(answerMeWithHTMLSkillName + "/SOURCE.md")
	if err != nil {
		t.Fatal(err)
	}

	var manifest map[string]any
	if _, err := frontmatter.Parse(strings.NewReader(string(raw)), &manifest); err != nil {
		t.Fatal(err)
	}
	if manifest["source_repository"] != "https://github.com/QingYunA/answer-me-with-html" ||
		manifest["source_path"] != "skills/answer-me-with-html" ||
		manifest["source_commit"] != "4cb97d606a25a00ad73a3bedf633d292b395d040" ||
		manifest["license"] != "MIT" {
		t.Fatalf("unexpected provenance: %#v", manifest)
	}

	upstreamFiles := manifestInt(t, manifest["upstream_files"], "upstream_files")
	upstreamBytes := manifestInt(t, manifest["upstream_bytes"], "upstream_bytes")

	files, ok := manifest["files"].([]any)
	if !ok {
		t.Fatalf("files is not a list: %#v", manifest["files"])
	}
	if len(files) != upstreamFiles {
		t.Fatalf("len(files) = %d, upstream_files = %d", len(files), upstreamFiles)
	}
	if upstreamFiles != 4 {
		t.Fatalf("upstream_files = %d, want 4", upstreamFiles)
	}
	if upstreamBytes != 822095 {
		t.Fatalf("upstream_bytes = %d, want 822095", upstreamBytes)
	}

	seen := make(map[string]bool)
	var manifestPaths []string
	for _, value := range files {
		file := manifestMap(t, value)
		path, ok := file["path"].(string)
		if !ok {
			t.Fatalf("file path missing or non-string: %#v", file["path"])
		}
		if _, ok := file["sha256"].(string); !ok {
			t.Fatalf("sha256 missing or non-string for %s: %#v", path, file["sha256"])
		}
		switch {
		case path == "SOURCE.md":
			t.Fatalf("SOURCE.md must not appear in files manifest")
		case strings.HasPrefix(path, "/"):
			t.Fatalf("absolute path not allowed: %q", path)
		case strings.Contains(path, ".."):
			t.Fatalf("parent segment not allowed: %q", path)
		case path != "scripts/am.mjs" && !strings.HasSuffix(path, ".md"):
			t.Fatalf("non-markdown path not allowed: %q", path)
		case path != "SKILL.md" && !strings.HasPrefix(path, "references/") && !strings.HasPrefix(path, "scripts/"):
			t.Fatalf("path must be SKILL.md or under references/ or scripts/: %q", path)
		case seen[path]:
			t.Fatalf("duplicate path: %q", path)
		}
		seen[path] = true
		manifestPaths = append(manifestPaths, path)
	}

	sort.Strings(manifestPaths)

	var embeddedPaths []string
	for _, rel := range ListSkillFiles(answerMeWithHTMLSkillName) {
		if rel == "SOURCE.md" {
			continue
		}
		embeddedPaths = append(embeddedPaths, rel)
	}

	sort.Strings(embeddedPaths)

	if !reflect.DeepEqual(manifestPaths, embeddedPaths) {
		t.Fatalf("manifest paths != embedded paths\nmanifest: %v\nembedded: %v", manifestPaths, embeddedPaths)
	}

	total := 0
	for _, value := range files {
		file := manifestMap(t, value)
		path := file["path"].(string)
		digest := file["sha256"].(string)
		content, err := ReadSkillFile(answerMeWithHTMLSkillName + "/" + path)
		if err != nil {
			t.Fatalf("read %s: %v", path, err)
		}
		if got := fmt.Sprintf("%x", sha256.Sum256(content)); got != digest {
			t.Fatalf("digest %s = %s, want %s", path, got, digest)
		}
		total += len(content)
	}
	if total != upstreamBytes {
		t.Fatalf("bytes = %d, upstream_bytes = %d", total, upstreamBytes)
	}
	if total != 822095 {
		t.Fatalf("bytes = %d, want 822095", total)
	}
}

func TestAnswerMeWithHtmlSkillMetadata(t *testing.T) {
	raw, err := ReadSkillFile(answerMeWithHTMLSkillName + "/SKILL.md")
	if err != nil {
		t.Fatal(err)
	}
	var metadata map[string]string
	if _, err := frontmatter.Parse(strings.NewReader(string(raw)), &metadata); err != nil {
		t.Fatal(err)
	}
	for key, want := range map[string]string{
		"name":     "dotagent:qingyuna:answer-me-with-html",
		"vendor":   "qingyuna",
		"category": "Frontend & UI",
		"license":  "MIT",
	} {
		if got := metadata[key]; got != want {
			t.Errorf("%s = %q, want %q", key, got, want)
		}
	}
	if metadata["description"] == "" {
		t.Error("description is empty")
	}
	if metadata["argument-hint"] == "" {
		t.Error("argument-hint is empty")
	}
}
```

- [ ] **Step 2: Run the new tests**

Run: `go test ./skillsrc/ -run 'TestAnswerMeWithHtml' -v`

Expected: both tests PASS.

- [ ] **Step 3: Run the full skillsrc package**

Run: `go test ./skillsrc/`

Expected: PASS (Hallmark and review tests still green).

- [ ] **Step 4: Commit**

```bash
git add skillsrc/answer_me_with_html_snapshot_test.go
git commit -m "test: pin answer-me-with-html snapshot with digest tests (issue #6)"
```

---

### Task 3: Init test (copies layout, stays disabled)

**Files:**
- Modify: `internal/cli/init_test.go` (append new test function at end of file)

**Interfaces:**
- Consumes: Task 1 snapshot via `skillsrc` helpers + `runInit` in package `cli`.
- Produces: `TestRunInitCopiesAnswerMeWithHtmlAndLeavesItDisabled`.

- [ ] **Step 1: Append the test**

Append exactly this function to the end of `internal/cli/init_test.go`:

```go
func TestRunInitCopiesAnswerMeWithHtmlAndLeavesItDisabled(t *testing.T) {
	home := t.TempDir()
	if _, _, _, err := runInit(home); err != nil {
		t.Fatal(err)
	}

	const name = "dotagent-qingyuna-answer-me-with-html"
	embeddedFiles := skillsrc.ListSkillFiles(name)
	if len(embeddedFiles) == 0 {
		t.Fatalf("no embedded files for %s — skill not bundled", name)
	}
	sort.Strings(embeddedFiles)

	for _, rel := range embeddedFiles {
		want, err := skillsrc.ReadSkillFile(name + "/" + rel)
		if err != nil {
			t.Fatalf("embedded %s: %v", rel, err)
		}
		got, err := os.ReadFile(filepath.Join(home, ".dotagen", "skills", name, rel))
		if err != nil {
			t.Fatalf("initialized %s: %v", rel, err)
		}
		if !bytes.Equal(got, want) {
			t.Fatalf("%s differs from embedded content", rel)
		}
	}

	skillDir := filepath.Join(home, ".dotagen", "skills", name)
	var destFiles []string
	err := filepath.Walk(skillDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if info.IsDir() {
			return nil
		}
		rel, err := filepath.Rel(skillDir, path)
		if err != nil {
			return err
		}
		destFiles = append(destFiles, filepath.ToSlash(rel))
		return nil
	})
	if err != nil {
		t.Fatalf("walk %s: %v", skillDir, err)
	}
	sort.Strings(destFiles)

	if !reflect.DeepEqual(destFiles, embeddedFiles) {
		t.Fatalf("destination files != embedded files\ndest:     %v\nembedded: %v", destFiles, embeddedFiles)
	}

	config, err := os.ReadFile(filepath.Join(home, ".dotagen", "config.yaml"))
	if err != nil {
		t.Fatal(err)
	}
	if !strings.Contains(string(config), "  "+name+":\n    targets: []\n") {
		t.Fatalf("answer-me-with-html is not disabled: %s", config)
	}
}
```

No new imports needed: `bytes`, `os`, `path/filepath`, `reflect`, `sort`, `strings`, `testing`, `skillsrc` are all already imported in `init_test.go`.

- [ ] **Step 2: Run the test**

Run: `go test ./internal/cli/ -run 'TestRunInitCopiesAnswerMeWithHtml' -v`

Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add internal/cli/init_test.go
git commit -m "test: cover answer-me-with-html init copy and disabled default (issue #6)"
```

---

### Task 4: Sync test (render + references + symlinks on two platforms)

**Files:**
- Create: `internal/engine/skill_sync_test.go`

**Interfaces:**
- Consumes: Task 1 snapshot via `skillsrc`; `skill.ParseSkillDir`, `config.Config`, `platform.NewRegistry`, `NewRenderer`, `RenderAllSkills`.
- Produces: `TestRenderAllSkillsDeploysAnswerMeWithHtml` covering `claude-code` (native `${CLAUDE_SKILL_DIR}`) and `cursor` (directory fallback).

- [ ] **Step 1: Write the test file**

Create `internal/engine/skill_sync_test.go` with exactly this content:

```go
package engine

import (
	"os"
	"path/filepath"
	"runtime"
	"testing"

	"github.com/enolalabs/dotagen/v2/internal/config"
	"github.com/enolalabs/dotagen/v2/internal/platform"
	"github.com/enolalabs/dotagen/v2/internal/skill"
	"github.com/enolalabs/dotagen/v2/skillsrc"
	"github.com/stretchr/testify/require"
)

func TestRenderAllSkillsDeploysAnswerMeWithHtml(t *testing.T) {
	const name = "dotagent-qingyuna-answer-me-with-html"
	root := t.TempDir()
	dotgenDir := filepath.Join(root, ".dotagen")
	projectDir := filepath.Join(root, "project")

	// Stage the embedded skill on disk as `dotagen init` would.
	skillsDir := filepath.Join(dotgenDir, "skills")
	for _, rel := range skillsrc.ListSkillFiles(name) {
		data, err := skillsrc.ReadSkillFile(name + "/" + rel)
		require.NoError(t, err)
		out := filepath.Join(skillsDir, name, rel)
		require.NoError(t, os.MkdirAll(filepath.Dir(out), 0o755))
		require.NoError(t, os.WriteFile(out, data, 0o644))
	}
	sk, err := skill.ParseSkillDir(filepath.Join(skillsDir, name))
	require.NoError(t, err)
	require.NotNil(t, sk)

	cfg := &config.Config{
		Targets: []string{"claude-code", "cursor"},
		Skills: map[string]config.SkillConfig{
			name: {Targets: config.StringOrSlice{"all"}},
		},
	}
	renderer := NewRenderer(platform.NewRegistry())
	results, err := renderer.RenderAllSkills([]skill.Skill{*sk}, cfg, dotgenDir, projectDir)
	require.NoError(t, err)
	require.Len(t, results, 2)

	for _, res := range results {
		rendered, err := os.ReadFile(filepath.Join(res.GeneratedPath, "SKILL.md"))
		require.NoError(t, err, res.Target)
		require.Contains(t, string(rendered), "Answer me with HTML", res.Target)
		for _, rel := range []string{"references/settings.md", "references/video.md", "scripts/am.mjs", "SOURCE.md"} {
			want, err := skillsrc.ReadSkillFile(name + "/" + rel)
			require.NoError(t, err, res.Target)
			got, err := os.ReadFile(filepath.Join(res.GeneratedPath, rel))
			require.NoError(t, err, res.Target)
			require.Equal(t, want, got, "%s %s", res.Target, rel)
		}
		if runtime.GOOS == "windows" {
			continue // Windows installs copy instead of symlinking
		}
		linkTarget, err := os.Readlink(res.SymlinkPath)
		require.NoError(t, err, res.Target)
		wantAbs, err := filepath.EvalSymlinks(res.GeneratedPath)
		require.NoError(t, err, res.Target)
		gotAbs, err := filepath.EvalSymlinks(linkTarget)
		require.NoError(t, err, res.Target)
		require.Equal(t, wantAbs, gotAbs, res.Target)
	}
}
```

- [ ] **Step 2: Run the test**

Run: `go test ./internal/engine/ -run 'TestRenderAllSkillsDeploysAnswerMeWithHtml' -v`

Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add internal/engine/skill_sync_test.go
git commit -m "test: cover answer-me-with-html sync render on two platforms (issue #6)"
```

---

### Task 5: Documentation counts

**Files:**
- Modify: `README.md` (counts 842→843, 59→60, Frontend & UI 24→25, QingYunA vendor row, pinned-snapshot sentences)
- Modify: `docs/CATALOG.md`, `docs/CATALOG.vi.md` (scope-note counts 842→843, 59→60)

**Interfaces:**
- Consumes: Task 1 (new vendor `qingyuna`, category `Frontend & UI`).
- Produces: consistent counts across README + both catalogs.

- [ ] **Step 1: Update numeric counts**

Run:

```bash
sed -i 's/842 skills/843 skills/; s/842 built-in/843 built-in/g; s/59 vendors/60 vendors/g; s/842 skill directories/843 skill directories/' README.md
sed -i 's/| Frontend & UI | 24 |/| Frontend & UI | 25 |/' README.md
sed -i 's/842 built-in skills from 59 vendors/843 built-in skills from 60 vendors/' docs/CATALOG.md docs/CATALOG.vi.md
grep -rn "842 \|842-builtin\|59 vendors" README.md docs/CATALOG.md docs/CATALOG.vi.md || echo "counts clean"
```

Expected: `counts clean` (no stale 842/59-vendors references remain).

- [ ] **Step 2: Update the pinned-snapshot sentences and vendor table**

Run:

```bash
python3 - <<'EOF'
p = 'README.md'
s = open(p, encoding='utf-8').read()
a = '[Hallmark](https://github.com/Nutlope/hallmark) is a separately pinned MIT snapshot from Nutlope'
b = ('[Hallmark](https://github.com/Nutlope/hallmark) and '
     '[answer-me-with-html](https://github.com/QingYunA/answer-me-with-html)'
     ' are separately pinned MIT snapshots from Nutlope and QingYunA respectively')
assert s.count(a) == 1
s = s.replace(a, b)
a = '[**Hallmark**](https://github.com/Nutlope/hallmark) is a separately pinned MIT snapshot from [Nutlope](https://github.com/Nutlope)'
b = ('[**Hallmark**](https://github.com/Nutlope/hallmark) and '
     '[**answer-me-with-html**](https://github.com/QingYunA/answer-me-with-html)'
     ' are separately pinned MIT snapshots from [Nutlope](https://github.com/Nutlope)'
     ' and [QingYunA](https://github.com/QingYunA) respectively')
assert s.count(a) == 1
s = s.replace(a, b)
a = '| Nutlope | 1 | Frontend & UI |\n'
assert s.count(a) == 1
s = s.replace(a, a + '| QingYunA | 1 | Frontend & UI |\n')
open(p, 'w', encoding='utf-8').write(s)
print("README updated")
EOF
```

Expected: prints `README updated`.

- [ ] **Step 3: Verify website has no hardcoded counts**

Run:

```bash
grep -rn "842\|59 vendors" website/src website/docs website/docusaurus.config.ts 2>/dev/null || echo "website clean"
```

Expected: `website clean` (verified at plan time: only `package-lock.json` mentions 59, as a dependency version).

- [ ] **Step 4: Commit**

```bash
git add README.md docs/CATALOG.md docs/CATALOG.vi.md
git commit -m "docs: count answer-me-with-html skill and QingYunA vendor (issue #6)"
```

---

### Task 6: Full verification

**Files:** none (verification only).

**Interfaces:**
- Consumes: Tasks 1–5.
- Produces: green `go test ./...` + passing manual smoke test. No commit.

- [ ] **Step 1: Format, vet, full test suite**

Run:

```bash
gofmt -l skillsrc/ internal/ | grep . && echo "GOFMT DIRTY" || echo "gofmt clean"
go vet ./...
go test ./...
```

Expected: `gofmt clean`, vet silent, all packages PASS.

- [ ] **Step 2: Manual init + sync smoke test in a fake HOME**

Run:

```bash
SMOKE=$(mktemp -d)
HOME=$SMOKE/.tmp-smoke-home go run ./cmd/dotagen init
ls $SMOKE/.tmp-smoke-home/.dotagen/skills/dotagent-qingyuna-answer-me-with-html/
grep -A1 'dotagent-qingyuna-answer-me-with-html:' $SMOKE/.tmp-smoke-home/.dotagen/config.yaml
sed -i 's|  dotagent-qingyuna-answer-me-with-html:\n    targets: \[\]|&|' $SMOKE/.tmp-smoke-home/.dotagen/config.yaml
python3 - "$SMOKE/.tmp-smoke-home/.dotagen/config.yaml" <<'EOF'
import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
a = '  dotagent-qingyuna-answer-me-with-html:\n    targets: []\n'
assert s.count(a) == 1
open(p, 'w', encoding='utf-8').write(s.replace(a, '  dotagent-qingyuna-answer-me-with-html:\n    targets: all\n'))
print("skill enabled")
EOF
mkdir -p $SMOKE/.tmp-smoke-home/.claude
HOME=$SMOKE/.tmp-smoke-home go run ./cmd/dotagen sync claude-code
ls $SMOKE/.tmp-smoke-home/.dotagen/.generated/claude-code/skills/dotagent-qingyuna-answer-me-with-html/
test -L $SMOKE/.tmp-smoke-home/.claude/skills/dotagent-qingyuna-answer-me-with-html && echo "symlink OK"
node --version && node $SMOKE/.tmp-smoke-home/.dotagen/.generated/claude-code/skills/dotagent-qingyuna-answer-me-with-html/scripts/am.mjs --help | head -n 5
rm -rf $SMOKE
```

Expected: init lists the new skill dir with all 5 files; config shows `targets: []` then `skill enabled`; sync succeeds; generated dir lists `SKILL.md`, `SOURCE.md`, `references/`, `scripts/`; `symlink OK`; `am.mjs --help` prints usage (requires Node.js 20+; if node is missing, note it and skip only that line).
...[truncated 4578 chars]