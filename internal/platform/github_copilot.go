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

type CopilotAdapter struct{}

func NewCopilotAdapter() *CopilotAdapter {
	return &CopilotAdapter{}
}

func (a *CopilotAdapter) Name() string {
	return "github-copilot"
}

func (a *CopilotAdapter) Render(ag agent.Agent) (string, error) {
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

func (a *CopilotAdapter) OutputPath(agentName string) string {
	return filepath.Join("github-copilot", agentName+".md")
}

func (a *CopilotAdapter) SymlinkPath(agentName string) string {
	return filepath.Join(config.CopilotRootPath, agentName+".md")
}

func (a *CopilotAdapter) EnsureDirectories(projectDir string) error {
	return os.MkdirAll(filepath.Join(projectDir, config.CopilotRootPath), 0o755)
}

func (a *CopilotAdapter) RenderSkill(sk skill.Skill) (string, error) {
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

func (a *CopilotAdapter) SkillOutputDir(skillName string) string {
	return filepath.Join("github-copilot", "skills", skillName)
}

func (a *CopilotAdapter) SkillSymlinkDir(skillName string) string {
	return filepath.Join(config.CopilotSkillPath, skillName)
}

func (a *CopilotAdapter) EnsureSkillDirectories(projectDir string) error {
	return os.MkdirAll(filepath.Join(projectDir, config.CopilotSkillPath), 0o755)
}
