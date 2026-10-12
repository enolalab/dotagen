# Motion-Graphics Built-in Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Vendor two MIT-licensed Remotion motion-graphics skills (haidrrrry + fernandokaraka) as pinned, hash-verified built-in skills (issue #8).

**Architecture:** No runtime code changes. Add `skillsrc/data/dotagent-haidrrrry-remotion-motion-graphics/` (4 upstream files + `SOURCE.md`) and `skillsrc/data/dotagent-fernandokaraka-remotion-motion-graphics/` (5 upstream files + `SOURCE.md`); the existing `go:embed` + `runInit` copy + `RenderAllSkills` symlink flow picks them up. Mirror the answer-me-with-html snapshot tests, init tests, docs-count updates, and add one sync test covering both skills on two platforms.

**Tech Stack:** Go 1.26+, testify, `go test ./...`, git.

## Global Constraints

- Pinned upstream commits: haidrrrry `1dcbe5e3fc6cf970bd10d3cc05f0a8a5d19d0383` (`main`, 2026-08-12, source dir `remotion-motion-graphics`); fernandokaraka `1fc286924c68260b7945f1f29e474b986446b70d` (`main`, 2026-07-17, source dir `skills/remotion-motion-graphics`). All downloads use these SHAs in the raw URL, never `main`.
- Skill directories: `skillsrc/data/dotagent-haidrrrry-remotion-motion-graphics/` and `skillsrc/data/dotagent-fernandokaraka-remotion-motion-graphics/`; frontmatter `name: "dotagent:<vendor>:remotion-motion-graphics"`, `vendor: "<vendor>"`, `category: "Documents & Content"`, `license: MIT`.
- Upstream single-line `description` kept verbatim on one line; no `argument-hint` (neither upstream uses `$ARGUMENTS`); bodies kept verbatim; the only intentional edits are the frontmatter normalizations.
- Snapshot manifests: haidrrrry 4 files, 23240 bytes; fernandokaraka 5 files, 33243 bytes. No network dependency added to builds, installs, or runtime.
- Both skills stay disabled by default (`targets: []`).
- CI is billing-blocked: verify with full local runs (`go test ./...`, manual `init`+`sync` smoke test).

---

### Task 1: Vendor the haidrrrry snapshot

**Files:**
- Create: `skillsrc/data/dotagent-haidrrrry-remotion-motion-graphics/SKILL.md`
- Create: `skillsrc/data/dotagent-haidrrrry-remotion-motion-graphics/references/design-rules.md`
- Create: `skillsrc/data/dotagent-haidrrrry-remotion-motion-graphics/references/motion-patterns.md`
- Create: `skillsrc/data/dotagent-haidrrrry-remotion-motion-graphics/assets/theme.ts`
- Create: `skillsrc/data/dotagent-haidrrrry-remotion-motion-graphics/SOURCE.md`

**Interfaces:**
- Consumes: upstream raw files at pinned commit (URLs below).
- Produces: 4 snapshot files with exact bytes/hashes below + `SOURCE.md` manifest consumed by Task 3 tests.

Expected final bytes and SHA-256 (post-normalization):

| Path | Bytes | SHA-256 |
|---|---|---|
| `SKILL.md` | 7995 | `f5547417e7cdb0b65a075e48107639a24253276877babebbb5f1cbb8e7991255` |
| `references/design-rules.md` | 4332 | `cd101a35bb81c4ab58871a7514216a508d355ea65332d682214012952c1489f9` |
| `references/motion-patterns.md` | 9763 | `3499916cdf80226fe3ed53a367dcb072088d08b40494314eb7c38c2f8aaca939` |
| `assets/theme.ts` | 1150 | `690a8ce4440be897781df3baeba1e89b8c30797cb05354d279e7eb69a5b6da58` |

- [ ] **Step 1: Create directories and download the 4 pinned files**

Run:

```bash
D=skillsrc/data/dotagent-haidrrrry-remotion-motion-graphics
mkdir -p $D/references $D/assets
B=https://raw.githubusercontent.com/haidrrrry/claude-remotion-skill/1dcbe5e3fc6cf970bd10d3cc05f0a8a5d19d0383/remotion-motion-graphics
curl -sL -o /tmp/mgh-SKILL.md "$B/SKILL.md"
curl -sL -o $D/references/design-rules.md "$B/references/design-rules.md"
curl -sL -o $D/references/motion-patterns.md "$B/references/motion-patterns.md"
curl -sL -o $D/assets/theme.ts "$B/assets/theme.ts"
```

Expected: 4 files downloaded, no curl errors.

- [ ] **Step 2: Verify the 3 verbatim files match their known hashes**

Run:

```bash
D=skillsrc/data/dotagent-haidrrrry-remotion-motion-graphics
sha256sum $D/references/design-rules.md $D/references/motion-patterns.md $D/assets/theme.ts
```

Expected output:

```
cd101a35bb81c4ab58871a7514216a508d355ea65332d682214012952c1489f9  skillsrc/data/dotagent-haidrrrry-remotion-motion-graphics/references/design-rules.md
3499916cdf80226fe3ed53a367dcb072088d08b40494314eb7c38c2f8aaca939  skillsrc/data/dotagent-haidrrrry-remotion-motion-graphics/references/motion-patterns.md
690a8ce4440be897781df3baeba1e89b8c30797cb05354d279e7eb69a5b6da58  skillsrc/data/dotagent-haidrrrry-remotion-motion-graphics/assets/theme.ts
```

If any hash differs, STOP: the pinned commit moved or the download is corrupt. Do not proceed.

- [ ] **Step 3: Normalize SKILL.md frontmatter**

Run this exact script (it copies the single-line description from upstream byte-for-byte, so no text is retyped):

```bash
D=skillsrc/data/dotagent-haidrrrry-remotion-motion-graphics
python3 - "$D" <<'EOF'
import sys
d = sys.argv[1]
raw = open('/tmp/mgh-SKILL.md', encoding='utf-8').read()
assert raw.startswith('---\n'), "upstream SKILL.md lost its frontmatter"
_, fm, body = raw.split('---\n', 2)
assert 'name: remotion-motion-graphics' in fm, "upstream skill renamed"
desc = [ln for ln in fm.split('\n') if ln.startswith('description:')]
assert len(desc) == 1, f"expected 1 description line, got {len(desc)}"
assert 'argument-hint' not in fm, "upstream added argument-hint"
assert '$ARGUMENTS' not in raw, "upstream added $ARGUMENTS dispatch"
new_fm = ('---\n'
    'name: "dotagent:haidrrrry:remotion-motion-graphics"\n'
    + desc[0] + '\n'
    'category: "Documents & Content"\n'
    'vendor: "haidrrrry"\n'
    'license: MIT\n'
    '---\n')
open(f'{d}/SKILL.md', 'w', encoding='utf-8').write(new_fm + body)
print("staged OK")
EOF
```

Expected: prints `staged OK`.

- [ ] **Step 4: Hygiene scan (fail-closed import gate)**

Run:

```bash
D=skillsrc/data/dotagent-haidrrrry-remotion-motion-graphics
test -z "$(find $D -type l)" && echo "no symlinks"
grep -rEn '/home/|/Users/|/tmp/|C:\\|$ARGUMENTS|skill-dir|SKILL_DIR' $D && echo "HYGIENE DIRTY" || echo "hygiene clean"
```

Expected: `no symlinks` and `hygiene clean`. Any match is a STOP: inspect the path before proceeding (per spec, the import must fail and report the path and reason).

- [ ] **Step 5: Verify all 4 snapshot hashes and byte counts**

Run:

```bash
D=skillsrc/data/dotagent-haidrrrry-remotion-motion-graphics
sha256sum $D/SKILL.md $D/references/design-rules.md $D/references/motion-patterns.md $D/assets/theme.ts
wc -c $D/SKILL.md $D/references/design-rules.md $D/references/motion-patterns.md $D/assets/theme.ts
```

Expected: hashes and byte counts match the table at the top of this task exactly (total 23240).

- [ ] **Step 6: Write SOURCE.md**

Create `skillsrc/data/dotagent-haidrrrry-remotion-motion-graphics/SOURCE.md` with exactly this content:

```markdown
---
source_repository: "https://github.com/haidrrrry/claude-remotion-skill"
source_path: "remotion-motion-graphics"
source_commit: "1dcbe5e3fc6cf970bd10d3cc05f0a8a5d19d0383"
snapshot_date: "2026-10-12"
license: "MIT"
copyright: "Copyright (c) 2025 haidrrrry"
upstream_files: 4
upstream_bytes: 23240
files:
  - path: "SKILL.md"
    sha256: "f5547417e7cdb0b65a075e48107639a24253276877babebbb5f1cbb8e7991255"
  - path: "references/design-rules.md"
    sha256: "cd101a35bb81c4ab58871a7514216a508d355ea65332d682214012952c1489f9"
  - path: "references/motion-patterns.md"
    sha256: "3499916cdf80226fe3ed53a367dcb072088d08b40494314eb7c38c2f8aaca939"
  - path: "assets/theme.ts"
    sha256: "690a8ce4440be897781df3baeba1e89b8c30797cb05354d279e7eb69a5b6da58"
---

# remotion-motion-graphics (haidrrrry) source provenance

Manual update: checkout the pinned commit; review the full file set and license; reject symlinks, non-Markdown files outside assets/, unsafe instructions, and absolute filesystem references; regenerate this ledger; update README; run the required Go tests.

The reviewer examined the complete 4-file set at pinned commit `1dcbe5e3fc6cf970bd10d3cc05f0a8a5d19d0383`. Frontmatter was normalized to name `dotagent:haidrrrry:remotion-motion-graphics`, vendor `haidrrrry`, category `Documents & Content`, license `MIT`; the single-line description was kept verbatim and no argument-hint was added (no $ARGUMENTS dispatch). No body adaptations were made. `assets/theme.ts` (1.2 KB theme template, required at runtime — every workflow copies it into `src/theme.ts` as the single source of truth for colors, easings, and springs) is plain TypeScript with no network or credential use. The skill shells out only to local commands (`npm install`, `npx remotion render`/`still`, `which`/`ls` browser probes, `ffmpeg`/`ffprobe` frame extraction), with no network URLs (only an SVG-data-URI XML namespace), no credentials, and no self-update behavior. No remote prompt loading, credential collection/exfiltration, or unsafe command instructions were found. The MIT license notice reads `Copyright (c) 2025 haidrrrry`.
```

- [ ] **Step 7: Commit**

```bash
git add skillsrc/data/dotagent-haidrrrry-remotion-motion-graphics
git commit -m "feat: vendor haidrrrry remotion-motion-graphics snapshot (issue #8)"
```

---

### Task 2: Vendor the fernandokaraka snapshot

**Files:**
- Create: `skillsrc/data/dotagent-fernandokaraka-remotion-motion-graphics/SKILL.md`
- Create: `skillsrc/data/dotagent-fernandokaraka-remotion-motion-graphics/references/patterns.md`
- Create: `skillsrc/data/dotagent-fernandokaraka-remotion-motion-graphics/references/polish.md`
- Create: `skillsrc/data/dotagent-fernandokaraka-remotion-motion-graphics/references/scaffold.md`
- Create: `skillsrc/data/dotagent-fernandokaraka-remotion-motion-graphics/references/traps.md`
- Create: `skillsrc/data/dotagent-fernandokaraka-remotion-motion-graphics/SOURCE.md`

**Interfaces:**
- Consumes: upstream raw files at pinned commit (URLs below).
- Produces: 5 snapshot files with exact bytes/hashes below + `SOURCE.md` manifest consumed by Task 3 tests.

Expected final bytes and SHA-256 (post-normalization):

| Path | Bytes | SHA-256 |
|---|---|---|
| `SKILL.md` | 6747 | `44ba993517e6755f92e301e6acad8fba54a1c1e7887f6db59d3dc555c7b399ea` |
| `references/patterns.md` | 10933 | `362afb2a2b1527f765bee209f69c7b273739d2875c2c7f5cd1a583f4b75dc3d9` |
| `references/polish.md` | 4544 | `69771e83ed8b4aaa7b05da56982245dcc3dd0631c572020468d30bd455aaafd2` |
| `references/scaffold.md` | 5249 | `53fa5d76ce997cbb409e7b80d8039537b9d641aac9419601de05ff1aa93e4b41` |
| `references/traps.md` | 5770 | `125eaacaebf809f868f1a4c5dfa40716940246ad7f5f170ff1c6a8ce6eb36151` |

- [ ] **Step 1: Create directories and download the 5 pinned files**

Run:

```bash
D=skillsrc/data/dotagent-fernandokaraka-remotion-motion-graphics
mkdir -p $D/references
B=https://raw.githubusercontent.com/fernandokaraka/remotion-motion-graphics-skill/1fc286924c68260b7945f1f29e474b986446b70d/skills/remotion-motion-graphics
curl -sL -o /tmp/mgf-SKILL.md "$B/SKILL.md"
curl -sL -o $D/references/patterns.md "$B/references/patterns.md"
curl -sL -o $D/references/polish.md "$B/references/polish.md"
curl -sL -o $D/references/scaffold.md "$B/references/scaffold.md"
curl -sL -o $D/references/traps.md "$B/references/traps.md"
```

Expected: 5 files downloaded, no curl errors.

- [ ] **Step 2: Verify the 4 verbatim files match their known hashes**

Run:

```bash
D=skillsrc/data/dotagent-fernandokaraka-remotion-motion-graphics
sha256sum $D/references/patterns.md $D/references/polish.md $D/references/scaffold.md $D/references/traps.md
```

Expected output:

```
362afb2a2b1527f765bee209f69c7b273739d2875c2c7f5cd1a583f4b75dc3d9  skillsrc/data/dotagent-fernandokaraka-remotion-motion-graphics/references/patterns.md
69771e83ed8b4aaa7b05da56982245dcc3dd0631c572020468d30bd455aaafd2  skillsrc/data/dotagent-fernandokaraka-remotion-motion-graphics/references/polish.md
53fa5d76ce997cbb409e7b80d8039537b9d641aac9419601de05ff1aa93e4b41  skillsrc/data/dotagent-fernandokaraka-remotion-motion-graphics/references/scaffold.md
125eaacaebf809f868f1a4c5dfa40716940246ad7f5f170ff1c6a8ce6eb36151  skillsrc/data/dotagent-fernandokaraka-remotion-motion-graphics/references/traps.md
```

If any hash differs, STOP: the pinned commit moved or the download is corrupt. Do not proceed.

- [ ] **Step 3: Normalize SKILL.md frontmatter**

Run this exact script (it copies the single-line description from upstream byte-for-byte, so no text is retyped):

```bash
D=skillsrc/data/dotagent-fernandokaraka-remotion-motion-graphics
python3 - "$D" <<'EOF'
import sys
d = sys.argv[1]
raw = open('/tmp/mgf-SKILL.md', encoding='utf-8').read()
assert raw.startswith('---\n'), "upstream SKILL.md lost its frontmatter"
_, fm, body = raw.split('---\n', 2)
assert 'name: remotion-motion-graphics' in fm, "upstream skill renamed"
desc = [ln for ln in fm.split('\n') if ln.startswith('description:')]
assert len(desc) == 1, f"expected 1 description line, got {len(desc)}"
assert 'argument-hint' not in fm, "upstream added argument-hint"
assert '$ARGUMENTS' not in raw, "upstream added $ARGUMENTS dispatch"
new_fm = ('---\n'
    'name: "dotagent:fernandokaraka:remotion-motion-graphics"\n'
    + desc[0] + '\n'
    'category: "Documents & Content"\n'
    'vendor: "fernandokaraka"\n'
    'license: MIT\n'
    '---\n')
open(f'{d}/SKILL.md', 'w', encoding='utf-8').write(new_fm + body)
print("staged OK")
EOF
```

Expected: prints `staged OK`.

- [ ] **Step 4: Hygiene scan (fail-closed import gate)**

Run:

```bash
D=skillsrc/data/dotagent-fernandokaraka-remotion-motion-graphics
test -z "$(find $D -type l)" && echo "no symlinks"
grep -rEn '/home/|/Users/|/tmp/|C:\\|$ARGUMENTS|skill-dir|SKILL_DIR' $D && echo "HYGIENE DIRTY" || echo "hygiene clean"
```

Expected: `no symlinks` and `hygiene clean`. Any match is a STOP: inspect the path before proceeding (per spec, the import must fail and report the path and reason).

- [ ] **Step 5: Verify all 5 snapshot hashes and byte counts**

Run:

```bash
D=skillsrc/data/dotagent-fernandokaraka-remotion-motion-graphics
sha256sum $D/SKILL.md $D/references/patterns.md $D/references/polish.md $D/references/scaffold.md $D/references/traps.md
wc -c $D/SKILL.md $D/references/patterns.md $D/references/polish.md $D/references/scaffold.md $D/references/traps.md
```

Expected: hashes and byte counts match the table at the top of this task exactly (total 33243).

- [ ] **Step 6: Write SOURCE.md**

Create `skillsrc/data/dotagent-fernandokaraka-remotion-motion-graphics/SOURCE.md` with exactly this content:

```markdown
---
source_repository: "https://github.com/fernandokaraka/remotion-motion-graphics-skill"
source_path: "skills/remotion-motion-graphics"
source_commit: "1fc286924c68260b7945f1f29e474b986446b70d"
snapshot_date: "2026-10-12"
license: "MIT"
copyright: "Copyright (c) 2026 Fernando Karakanian Melo"
upstream_files: 5
upstream_bytes: 33243
files:
  - path: "SKILL.md"
    sha256: "44ba993517e6755f92e301e6acad8fba54a1c1e7887f6db59d3dc555c7b399ea"
  - path: "references/patterns.md"
    sha256: "362afb2a2b1527f765bee209f69c7b273739d2875c2c7f5cd1a583f4b75dc3d9"
  - path: "references/polish.md"
    sha256: "69771e83ed8b4aaa7b05da56982245dcc3dd0631c572020468d30bd455aaafd2"
  - path: "references/scaffold.md"
    sha256: "53fa5d76ce997cbb409e7b80d8039537b9d641aac9419601de05ff1aa93e4b41"
  - path: "references/traps.md"
    sha256: "125eaacaebf809f868f1a4c5dfa40716940246ad7f5f170ff1c6a8ce6eb36151"
---

# remotion-motion-graphics (fernandokaraka) source provenance

Manual update: checkout the pinned commit; review the full file set and license; reject symlinks, non-Markdown files, unsafe instructions, and absolute filesystem references; regenerate this ledger; update README; run the required Go tests.

The reviewer examined the complete 5-file set at pinned commit `1fc286924c68260b7945f1f29e474b986446b70d`. Frontmatter was normalized to name `dotagent:fernandokaraka:remotion-motion-graphics`, vendor `fernandokaraka`, category `Documents & Content`, license `MIT`; the single-line description was kept verbatim and no argument-hint was added (no $ARGUMENTS dispatch). No body adaptations were made. The skill shells out only to `npx remotion render`/`still` and `npm run studio`, with no network use and no credential handling. No remote prompt loading, credential collection/exfiltration, or unsafe command instructions were found. The MIT license notice reads `Copyright (c) 2026 Fernando Karakanian Melo`.
```

- [ ] **Step 7: Commit**

```bash
git add skillsrc/data/dotagent-fernandokaraka-remotion-motion-graphics
git commit -m "feat: vendor fernandokaraka remotion-motion-graphics snapshot (issue #8)"
```

---

### Task 3: Snapshot and metadata tests

**Files:**
- Create: `skillsrc/haidrrrry_motion_graphics_snapshot_test.go`
- Create: `skillsrc/fernandokaraka_motion_graphics_snapshot_test.go`

**Interfaces:**
- Consumes: Task 1 + Task 2 snapshot files + `SOURCE.md` manifests; existing helpers `skillsrc.ListSkills`, `ReadSkillFile`, `ListSkillFiles`, and `manifestInt`/`manifestMap` from `skillsrc/hallmark_snapshot_test.go` (same package — reuse, do not redefine).
- Produces: `TestHaidrrrryMotionGraphicsSnapshotIsCompleteAndPinned`, `TestHaidrrrryMotionGraphicsSkillMetadata`, `TestFernandokarakaMotionGraphicsSnapshotIsCompleteAndPinned`, `TestFernandokarakaMotionGraphicsSkillMetadata`.

- [ ] **Step 1: Write the haidrrrry test file**

Create `skillsrc/haidrrrry_motion_graphics_snapshot_test.go` with exactly this content:

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

const haidrrrryMotionGraphicsSkillName = "dotagent-haidrrrry-remotion-motion-graphics"

func TestHaidrrrryMotionGraphicsSnapshotIsCompleteAndPinned(t *testing.T) {
	skills := ListSkills()
	listed := false
	for _, s := range skills {
		if s == haidrrrryMotionGraphicsSkillName {
			listed = true
			break
		}
	}
	if !listed {
		t.Fatalf("ListSkills() does not contain %q", haidrrrryMotionGraphicsSkillName)
	}

	raw, err := ReadSkillFile(haidrrrryMotionGraphicsSkillName + "/SOURCE.md")
	if err != nil {
		t.Fatal(err)
	}

	var manifest map[string]any
	if _, err := frontmatter.Parse(strings.NewReader(string(raw)), &manifest); err != nil {
		t.Fatal(err)
	}
	if manifest["source_repository"] != "https://github.com/haidrrrry/claude-remotion-skill" ||
		manifest["source_path"] != "remotion-motion-graphics" ||
		manifest["source_commit"] != "1dcbe5e3fc6cf970bd10d3cc05f0a8a5d19d0383" ||
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
	if upstreamBytes != 23240 {
		t.Fatalf("upstream_bytes = %d, want 23240", upstreamBytes)
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
		case path != "assets/theme.ts" && !strings.HasSuffix(path, ".md"):
			t.Fatalf("non-markdown path not allowed: %q", path)
		case path != "SKILL.md" && !strings.HasPrefix(path, "references/") && !strings.HasPrefix(path, "assets/"):
			t.Fatalf("path must be SKILL.md or under references/ or assets/: %q", path)
		case seen[path]:
			t.Fatalf("duplicate path: %q", path)
		}
		seen[path] = true
		manifestPaths = append(manifestPaths, path)
	}

	sort.Strings(manifestPaths)

	var embeddedPaths []string
	for _, rel := range ListSkillFiles(haidrrrryMotionGraphicsSkillName) {
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
		content, err := ReadSkillFile(haidrrrryMotionGraphicsSkillName + "/" + path)
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
	if total != 23240 {
		t.Fatalf("bytes = %d, want 23240", total)
	}
}

func TestHaidrrrryMotionGraphicsSkillMetadata(t *testing.T) {
	raw, err := ReadSkillFile(haidrrrryMotionGraphicsSkillName + "/SKILL.md")
	if err != nil {
		t.Fatal(err)
	}
	var metadata map[string]string
	if _, err := frontmatter.Parse(strings.NewReader(string(raw)), &metadata); err != nil {
		t.Fatal(err)
	}
	for key, want := range map[string]string{
		"name":     "dotagent:haidrrrry:remotion-motion-graphics",
		"vendor":   "haidrrrry",
		"category": "Documents & Content",
		"license":  "MIT",
	} {
		if got := metadata[key]; got != want {
			t.Errorf("%s = %q, want %q", key, got, want)
		}
	}
	if metadata["description"] == "" {
		t.Error("description is empty")
	}
	if _, ok := metadata["argument-hint"]; ok {
		t.Error("argument-hint must not be set (no $ARGUMENTS dispatch upstream)")
	}
}
```

- [ ] **Step 2: Write the fernandokaraka test file**

Create `skillsrc/fernandokaraka_motion_graphics_snapshot_test.go` with exactly this content:

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

const fernandokarakaMotionGraphicsSkillName = "dotagent-fernandokaraka-remotion-motion-graphics"

func TestFernandokarakaMotionGraphicsSnapshotIsCompleteAndPinned(t *testing.T) {
	skills := ListSkills()
	listed := false
	for _, s := range skills {
		if s == fernandokarakaMotionGraphicsSkillName {
			listed = true
			break
		}
	}
	if !listed {
		t.Fatalf("ListSkills() does not contain %q", fernandokarakaMotionGraphicsSkillName)
	}

	raw, err := ReadSkillFile(fernandokarakaMotionGraphicsSkillName + "/SOURCE.md")
	if err != nil {
		t.Fatal(err)
	}

	var manifest map[string]any
	if _, err := frontmatter.Parse(strings.NewReader(string(raw)), &manifest); err != nil {
		t.Fatal(err)
	}
	if manifest["source_repository"] != "https://github.com/fernandokaraka/remotion-motion-graphics-skill" ||
		manifest["source_path"] != "skills/remotion-motion-graphics" ||
		manifest["source_commit"] != "1fc286924c68260b7945f1f29e474b986446b70d" ||
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
	if upstreamFiles != 5 {
		t.Fatalf("upstream_files = %d, want 5", upstreamFiles)
	}
	if upstreamBytes != 33243 {
		t.Fatalf("upstream_bytes = %d, want 33243", upstreamBytes)
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
		case !strings.HasSuffix(path, ".md"):
			t.Fatalf("non-markdown path not allowed: %q", path)
		case path != "SKILL.md" && !strings.HasPrefix(path, "references/"):
			t.Fatalf("path must be SKILL.md or under references/: %q", path)
		case seen[path]:
			t.Fatalf("duplicate path: %q", path)
		}
		seen[path] = true
		manifestPaths = append(manifestPaths, path)
	}

	sort.Strings(manifestPaths)

	var embeddedPaths []string
	for _, rel := range ListSkillFiles(fernandokarakaMotionGraphicsSkillName) {
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
		content, err := ReadSkillFile(fernandokarakaMotionGraphicsSkillName + "/" + path)
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
	if total != 33243 {
		t.Fatalf("bytes = %d, want 33243", total)
	}
}

func TestFernandokarakaMotionGraphicsSkillMetadata(t *testing.T) {
	raw, err := ReadSkillFile(fernandokarakaMotionGraphicsSkillName + "/SKILL.md")
	if err != nil {
		t.Fatal(err)
	}
	var metadata map[string]string
	if _, err := frontmatter.Parse(strings.NewReader(string(raw)), &metadata); err != nil {
		t.Fatal(err)
	}
	for key, want := range map[string]string{
		"name":     "dotagent:fernandokaraka:remotion-motion-graphics",
		"vendor":   "fernandokaraka",
		"category": "Documents & Content",
		"license":  "MIT",
	} {
		if got := metadata[key]; got != want {
			t.Errorf("%s = %q, want %q", key, got, want)
		}
	}
	if metadata["description"] == "" {
		t.Error("description is empty")
	}
	if _, ok := metadata["argument-hint"]; ok {
		t.Error("argument-hint must not be set (no $ARGUMENTS dispatch upstream)")
	}
}
```

- [ ] **Step 3: Run the new tests**

Run: `go test ./skillsrc/ -run 'TestHaidrrrryMotionGraphics|TestFernandokarakaMotionGraphics' -v`

Expected: all 4 tests PASS.

- [ ] **Step 4: Run the full skillsrc package**

Run: `go test ./skillsrc/`

Expected: PASS (Hallmark and answer-me-with-html tests still green).

- [ ] **Step 5: Commit**

```bash
git add skillsrc/haidrrrry_motion_graphics_snapshot_test.go skillsrc/fernandokaraka_motion_graphics_snapshot_test.go
git commit -m "test: pin motion-graphics snapshots with digest tests (issue #8)"
```

---

### Task 4: Init tests (copy layout, stay disabled)

**Files:**
- Modify: `internal/cli/init_test.go` (append two test functions at end of file)

**Interfaces:**
- Consumes: Task 1 + Task 2 snapshots via `skillsrc` helpers + `runInit` in package `cli`.
- Produces: `TestRunInitCopiesHaidrrrryMotionGraphicsAndLeavesItDisabled`, `TestRunInitCopiesFernandokarakaMotionGraphicsAndLeavesItDisabled`.

- [ ] **Step 1: Append the haidrrrry test**

Append exactly this function to the end of `internal/cli/init_test.go`:

```go
func TestRunInitCopiesHaidrrrryMotionGraphicsAndLeavesItDisabled(t *testing.T) {
	home := t.TempDir()
	if _, _, _, err := runInit(home); err != nil {
		t.Fatal(err)
	}

	const name = "dotagent-haidrrrry-remotion-motion-graphics"
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
		t.Fatalf("haidrrrry remotion-motion-graphics is not disabled: %s", config)
	}
}
```

No new imports needed: `bytes`, `os`, `path/filepath`, `reflect`, `sort`, `strings`, `testing`, `skillsrc` are all already imported in `init_test.go`.

- [ ] **Step 2: Append the fernandokaraka test**

Append exactly this function to the end of `internal/cli/init_test.go` (after the haidrrrry test):

```go
func TestRunInitCopiesFernandokarakaMotionGraphicsAndLeavesItDisabled(t *testing.T) {
	home := t.TempDir()
	if _, _, _, err := runInit(home); err != nil {
		t.Fatal(err)
	}

	const name = "dotagent-fernandokaraka-remotion-motion-graphics"
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
		t.Fatalf("fernandokaraka remotion-motion-graphics is not disabled: %s", config)
	}
}
```

- [ ] **Step 3: Run the tests**

Run: `go test ./internal/cli/ -run 'TestRunInitCopiesHaidrrrryMotionGraphics|TestRunInitCopiesFernandokarakaMotionGraphics' -v`

Expected: both PASS.

- [ ] **Step 4: Commit**

```bash
git add internal/cli/init_test.go
git commit -m "test: cover motion-graphics init copy and disabled default (issue #8)"
```

---

### Task 5: Sync test (render + references + symlinks, both skills, two platforms)

**Files:**
- Modify: `internal/engine/skill_sync_test.go` (append new test function at end of file)

**Interfaces:**
- Consumes: Task 1 + Task 2 snapshots via `skillsrc`; `skill.ParseSkillDir`, `config.Config`, `platform.NewRegistry`, `NewRenderer`, `RenderAllSkills`.
- Produces: `TestRenderAllSkillsDeploysMotionGraphics` covering both skills on `claude-code` (native `${CLAUDE_SKILL_DIR}`) and `cursor` (directory fallback). This resolves spec-review follow-up #1 (concrete platforms instead of "at least one platform").

- [ ] **Step 1: Append the test**

Append exactly this function to the end of `internal/engine/skill_sync_test.go`:

```go
func TestRenderAllSkillsDeploysMotionGraphics(t *testing.T) {
	cases := []struct {
		name   string
		marker string
		refs   []string
	}{
		{
			name:   "dotagent-haidrrrry-remotion-motion-graphics",
			marker: "motion design craft",
			refs:   []string{"references/design-rules.md", "references/motion-patterns.md", "assets/theme.ts", "SOURCE.md"},
		},
		{
			name:   "dotagent-fernandokaraka-remotion-motion-graphics",
			marker: "Diagnose before you decorate",
			refs:   []string{"references/patterns.md", "references/polish.md", "references/scaffold.md", "references/traps.md", "SOURCE.md"},
		},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			name := tc.name
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
				require.Contains(t, string(rendered), tc.marker, res.Target)
				for _, rel := range tc.refs {
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
		})
	}
}
```

No new imports needed: `os`, `path/filepath`, `runtime`, `testing`, `config`, `platform`, `skill`, `skillsrc`, `require` are all already imported in `skill_sync_test.go`.

- [ ] **Step 2: Run the test**

Run: `go test ./internal/engine/ -run 'TestRenderAllSkillsDeploysMotionGraphics' -v`

Expected: PASS (both subtests).

- [ ] **Step 3: Commit**

```bash
git add internal/engine/skill_sync_test.go
git commit -m "test: cover motion-graphics sync render on two platforms (issue #8)"
```

---

### Task 6: Documentation counts

**Files:**
- Modify: `README.md` (counts 843→845, 60→62, Documents & Content 18→20, haidrrrry + fernandokaraka vendor rows, both pinned-snapshot sentences)
- Modify: `docs/CATALOG.md`, `docs/CATALOG.vi.md` (scope-note counts 843→845, 60→62)

**Interfaces:**
- Consumes: Tasks 1–2 (new vendors `haidrrrry`, `fernandokaraka`, category `Documents & Content`).
- Produces: consistent counts across README + both catalogs. This resolves spec-review follow-up #2 (every count location enumerated — 9 README spots + 2 CATALOG scope notes).

Every location (line numbers at plan time; match by content, not by number):
1. Catalog intro: `**843 skills**`, `**60 vendors**`, pinned-snapshot sentence.
2. Category table: `| Documents & Content | 18 |`.
3. Vendor `<details>`: `View all 60 vendors`.
4. Vendor table: new `haidrrrry` + `fernandokaraka` rows after the QingYunA row.
5. Init example: `all 843 built-in skills`.
6. `skills/` tree comment: `843 built-in skill directories`.
7. Command table: `with 843 built-in skills`.
8. `data/` tree comment: `843 skill directories`.
9. Acknowledgments: pinned-snapshot sentence.

Do NOT touch `| Testing & QA | 60 |` (category count) or `55 organizations` (awesome-agent-skills registry count).

- [ ] **Step 1: Update numeric counts**

Run:

```bash
sed -i 's/843 skills/845 skills/; s/843 built-in/845 built-in/g; s/60 vendors/62 vendors/g; s/843 skill directories/845 skill directories/' README.md
sed -i 's/| Documents & Content | 18 |/| Documents \& Content | 20 |/' README.md
sed -i 's/843 built-in skills from 60 vendors/845 built-in skills from 62 vendors/' docs/CATALOG.md
sed -i 's/843 built-in skills từ 60 vendor/845 built-in skills từ 62 vendor/' docs/CATALOG.vi.md
grep -rn "843 \|843-builtin\|60 vendor" README.md docs/CATALOG.md docs/CATALOG.vi.md || echo "counts clean"
```

Expected: `counts clean` (no stale 843/60-vendors references remain).

- [ ] **Step 2: Update the pinned-snapshot sentences and vendor table**

Run:

```bash
python3 - <<'EOF'
p = 'README.md'
s = open(p, encoding='utf-8').read()
a = ('[Hallmark](https://github.com/Nutlope/hallmark) and '
     '[answer-me-with-html](https://github.com/QingYunA/answer-me-with-html)'
     ' are separately pinned MIT snapshots from Nutlope and QingYunA respectively')
b = ('[Hallmark](https://github.com/Nutlope/hallmark), '
     '[answer-me-with-html](https://github.com/QingYunA/answer-me-with-html), '
     '[claude-remotion-skill](https://github.com/haidrrrry/claude-remotion-skill) and '
     '[remotion-motion-graphics-skill](https://github.com/fernandokaraka/remotion-motion-graphics-skill)'
     ' are separately pinned MIT snapshots from Nutlope, QingYunA, haidrrrry and fernandokaraka respectively')
assert s.count(a) == 1
s = s.replace(a, b)
a = ('[**Hallmark**](https://github.com/Nutlope/hallmark) and '
     '[**answer-me-with-html**](https://github.com/QingYunA/answer-me-with-html)'
     ' are separately pinned MIT snapshots from [Nutlope](https://github.com/Nutlope)'
     ' and [QingYunA](https://github.com/QingYunA) respectively')
b = ('[**Hallmark**](https://github.com/Nutlope/hallmark), '
     '[**answer-me-with-html**](https://github.com/QingYunA/answer-me-with-html), '
     '[**claude-remotion-skill**](https://github.com/haidrrrry/claude-remotion-skill) and '
     '[**remotion-motion-graphics-skill**](https://github.com/fernandokaraka/remotion-motion-graphics-skill)'
     ' are separately pinned MIT snapshots from [Nutlope](https://github.com/Nutlope),'
     ' [QingYunA](https://github.com/QingYunA), [haidrrrry](https://github.com/haidrrrry)'
     ' and [fernandokaraka](https://github.com/fernandokaraka) respectively')
assert s.count(a) == 1
s = s.replace(a, b)
a = '| QingYunA | 1 | Frontend & UI |\n'
assert s.count(a) == 1
s = s.replace(a, a + '| haidrrrry | 1 | Documents & Content |\n| fernandokaraka | 1 | Documents & Content |\n')
open(p, 'w', encoding='utf-8').write(s)
print("README updated")
EOF
```

Expected: prints `README updated`.

- [ ] **Step 3: Verify website has no hardcoded counts**

Run:

```bash
grep -rn "843\|60 vendors" website/ 2>/dev/null || echo "website clean"
```

Expected: `website clean` (verified at plan time: no matches under `website/`).

- [ ] **Step 4: Commit**

```bash
git add README.md docs/CATALOG.md docs/CATALOG.vi.md
git commit -m "docs: count motion-graphics skills and new vendors (issue #8)"
```

---

### Task 7: Full verification

**Files:** none (verification only).

**Interfaces:**
- Consumes: Tasks 1–6.
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
ls $SMOKE/.tmp-smoke-home/.dotagen/skills/dotagent-haidrrrry-remotion-motion-graphics/
ls $SMOKE/.tmp-smoke-home/.dotagen/skills/dotagent-fernandokaraka-remotion-motion-graphics/
grep -A1 'dotagent-haidrrrry-remotion-motion-graphics:' $SMOKE/.tmp-smoke-home/.dotagen/config.yaml
grep -A1 'dotagent-fernandokaraka-remotion-motion-graphics:' $SMOKE/.tmp-smoke-home/.dotagen/config.yaml
python3 - "$SMOKE/.tmp-smoke-home/.dotagen/config.yaml" <<'EOF'
import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
for name in ('dotagent-haidrrrry-remotion-motion-graphics',
             'dotagent-fernandokaraka-remotion-motion-graphics'):
    a = f'  {name}:\n    targets: []\n'
    assert s.count(a) == 1, name
    s = s.replace(a, f'  {name}:\n    targets: all\n')
open(p, 'w', encoding='utf-8').write(s)
print("skills enabled")
EOF
mkdir -p $SMOKE/.tmp-smoke-home/.claude
HOME=$SMOKE/.tmp-smoke-home go run ./cmd/dotagen sync claude-code
ls $SMOKE/.tmp-smoke-home/.dotagen/.generated/claude-code/skills/dotagent-haidrrrry-remotion-motion-graphics/
ls $SMOKE/.tmp-smoke-home/.dotagen/.generated/claude-code/skills/dotagent-fernandokaraka-remotion-motion-graphics/
test -L $SMOKE/.tmp-smoke-home/.claude/skills/dotagent-haidrrrry-remotion-motion-graphics && echo "haidrrrry symlink OK"
test -L $SMOKE/.tmp-smoke-home/.claude/skills/dotagent-fernandokaraka-remotion-motion-graphics && echo "fernandokaraka symlink OK"
head -c 200 $SMOKE/.tmp-smoke-home/.dotagen/.generated/claude-code/skills/dotagent-haidrrrry-remotion-motion-graphics/assets/theme.ts
rm -rf $SMOKE
```

Expected: init lists both new skill dirs with all files (5 + 6 incl. SOURCE.md); config shows `targets: []` then `skills enabled`; sync succeeds; haidrrrry generated dir lists `SKILL.md`, `SOURCE.md`, `references/`, `assets/`; fernandokaraka generated dir lists `SKILL.md`, `SOURCE.md`, `references/`; both `symlink OK`; `theme.ts` head prints TypeScript source. (`theme.ts` is a template the agent copies into projects, not an executed script, so there is no runtime check beyond byte-identical deploy, which Task 5 already asserts.)
