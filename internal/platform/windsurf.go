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

type WindsurfAdapter struct{}

func NewWindsurfAdapter() *WindsurfAdapter {
	return &WindsurfAdapter{}
}

func (a *WindsurfAdapter) Name() string {
	return "windsurf"
}

func (a *WindsurfAdapter) Render(ag agent.Agent) (string, error) {
	var sb strings.Builder
	sb.WriteString("---\n")
	sb.WriteString(fmt.Sprintf("name: %s\n", ag.Name))
	if desc, ok := ag.Frontmatter["description"]; ok && desc != "" {
		sb.WriteString(fmt.Sprintf("description: %s\n", desc))
	}
	sb.WriteString("---\n\n")
	sb.WriteString(ag.Content)
	return sb.String(), nil
}

func (a *WindsurfAdapter) OutputPath(agentName string) string {
	return filepath.Join("windsurf", agentName+".md")
}

func (a *WindsurfAdapter) SymlinkPath(agentName string) string {
	return filepath.Join(config.WindsurfRootPath, agentName+".md")
}

func (a *WindsurfAdapter) EnsureDirectories(projectDir string) error {
	return os.MkdirAll(filepath.Join(projectDir, config.WindsurfRootPath), 0o755)
}

func (a *WindsurfAdapter) RenderSkill(sk skill.Skill) (string, error) {
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

func (a *WindsurfAdapter) SkillOutputDir(skillName string) string {
	return filepath.Join("windsurf", "skills", skillName)
}

func (a *WindsurfAdapter) SkillSymlinkDir(skillName string) string {
	return filepath.Join(config.WindsurfSkillPath, skillName)
}

func (a *WindsurfAdapter) EnsureSkillDirectories(projectDir string) error {
	return os.MkdirAll(filepath.Join(projectDir, config.WindsurfSkillPath), 0o755)
}
