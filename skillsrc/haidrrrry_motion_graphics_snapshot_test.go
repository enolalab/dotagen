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
