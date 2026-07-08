package skillsrc

import (
	"embed"
	"io/fs"
	"sort"
	"strings"
)

//go:embed all:data
var DefaultSkills embed.FS

func ListSkills() []string {
	entries, err := fs.ReadDir(DefaultSkills, "data")
	if err != nil {
		return nil
	}
	var names []string
	for _, entry := range entries {
		if !entry.IsDir() {
			continue
		}
		if _, err := fs.Stat(DefaultSkills, "data/"+entry.Name()+"/SKILL.md"); err == nil {
			names = append(names, entry.Name())
		}
	}
	sort.Strings(names)
	return names
}

func ReadSkillFile(path string) ([]byte, error) {
	return fs.ReadFile(DefaultSkills, "data/"+path)
}

func ListSkillFiles(skillName string) []string {
	var files []string
	dir := "data/" + skillName
	fs.WalkDir(DefaultSkills, dir, func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			return err
		}
		if d.IsDir() {
			return nil
		}
		rel, err := relPath(dir, path)
		if err != nil {
			return nil
		}
		files = append(files, rel)
		return nil
	})
	return files
}

func relPath(base, target string) (string, error) {
	if !strings.HasPrefix(target, base+"/") {
		return target, nil
	}
	return target[len(base)+1:], nil
}
