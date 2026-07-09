package platform

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/enolalabs/dotagen/v2/internal/agent"
	"github.com/enolalabs/dotagen/v2/internal/config"
	"github.com/enolalabs/dotagen/v2/internal/skill"
)

type CursorAdapter struct{}

func NewCursorAdapter() *CursorAdapter {
	return &CursorAdapter{}
}

func (a *CursorAdapter) Name() string {
	return "cursor"
}

func (a *CursorAdapter) Render(ag agent.Agent) (string, error) {
	var sb strings.Builder
	sb.WriteString("---\n")
	sb.WriteString(fmt.Sprintf("description: %s\n", agent.ExtractDescription(ag)))
	if globs, ok := ag.Frontmatter["globs"]; ok && globs != "" {
		sb.WriteString(fmt.Sprintf("globs: %s\n", globs))
	}
	sb.WriteString("alwaysApply: false\n")
	sb.WriteString("---\n\n")
	sb.WriteString(ag.Content)
	return sb.String(), nil
}

func (a *CursorAdapter) OutputPath(agentName string) string {
	return filepath.Join("cursor", agentName+".mdc")
}

func (a *CursorAdapter) SymlinkPath(agentName string) string {
	return filepath.Join(config.CursorRootPath, agentName+".mdc")
}

func (a *CursorAdapter) EnsureDirectories(projectDir string) error {
	return os.MkdirAll(filepath.Join(projectDir, config.CursorRootPath), 0o755)
}

func (a *CursorAdapter) RenderSkill(sk skill.Skill) (string, error) {
	desc := skill.ExtractDescription(sk)
	var sb strings.Builder
	sb.WriteString("---\n")
	sb.WriteString(fmt.Sprintf("name: %s\n", sk.Name))
	if desc != "" {
		sb.WriteString(fmt.Sprintf("description: %s\n", desc))
	}
	sb.WriteString("---\n\n")
	sb.WriteString(sk.Content)
	return sb.String(), nil
}

func (a *CursorAdapter) SkillOutputDir(skillName string) string {
	return filepath.Join("cursor", "skills", skillName)
}

func (a *CursorAdapter) SkillSymlinkDir(skillName string) string {
	return filepath.Join(config.CursorSkillPath, skillName)
}

func (a *CursorAdapter) EnsureSkillDirectories(projectDir string) error {
	return os.MkdirAll(filepath.Join(projectDir, config.CursorSkillPath), 0o755)
}
