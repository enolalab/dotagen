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
