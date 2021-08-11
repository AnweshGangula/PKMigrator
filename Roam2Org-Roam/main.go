// Install Exporter package: go get github.com/fabioberger/roam-migration
// Run following command in terminal: go run main.go -p "C:\Users\AnweshG\Desktop\Roam-Export-1628326421838 - MD"

package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path"
	"regexp"
	"strings"
	"time"
)

const TITLE_PREFIX = "#+TITLE:"
const MAX_BULLET_NESTING = 20 // The max number of indents we will properly convert

func main() {
	ROAM_DIR_PTR := flag.String("p", "", "Path to directory containing your Roam Research export")
	flag.Parse()
	ROAM_DIR := *ROAM_DIR_PTR
	if ROAM_DIR == "" {
		log.Fatalf("Please make sure you use the -p flag to specify the path to the directory containing your Roam Research exported files")
	}
	err := recursivelyConvertFiles(ROAM_DIR)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Conversion complete!")
}

func recursivelyConvertFiles(directory string) error {
	files, err := ioutil.ReadDir(directory)
	if err != nil {
		return err
	}
	for _, f := range files {
		fileName := f.Name()
		filePath := path.Join(directory, fileName)
		if f.IsDir() {
			if err := recursivelyConvertFiles(filePath); err != nil {
				return err
			}
		}
		if !strings.HasSuffix(fileName, ".md") && !strings.HasSuffix(fileName, ".org") {
			continue // Ignore it
		}
		record, err := NewRecord(filePath)
		if err != nil {
			return err
		}
		if !record.HasTitle() {
			title := fmt.Sprintf("%s %s\n", TITLE_PREFIX, fileName[:len(fileName)-3])
			record.Prepend(title)
			if err != nil {
				return err
			}
		}
		record.FixBidirectionalLinks()
		names := record.FindAllBidirectionalLinkNames()
		record.FormatDates(names)
		record.FixTaskKeywords()
		record.FormatBullets()
		record.RemoveRoamStyling()
		record.UnderscoreLinkedFileNames(names)
		record.ConvertHashTagsToBidirectionalLinks()
		record.ConvertHyperLinks()
		err = record.Save()
		if err != nil {
			return err
		}

		// Rename file to underscore version and change suffix to .org
		dir, file := path.Split(filePath)
		oldPath := filePath
		newFile := strings.ReplaceAll(strings.Replace(file, ".md", ".org", 1), " ", "_")
		newPath := path.Join(dir, newFile)
		err = os.Rename(oldPath, newPath)
		if err != nil {
			return err
		}
		fmt.Println("Processed: ", fileName)
	}
	return nil
}

type Record struct {
	Path     string
	Contents string
}

func NewRecord(path string) (*Record, error) {
	content, err := ioutil.ReadFile(path)
	if err != nil {
		return nil, err
	}
	return &Record{
		Path:     path,
		Contents: string(content),
	}, nil
}

func (r *Record) ConvertHashTagsToBidirectionalLinks() {
	// Replace hash tags with links
	regex := `\s#([^[+[][^\s]+)`
	replacement := ` [[file:$1.org][$1]]`
	re := regexp.MustCompile(regex)
	r.Contents = re.ReplaceAllString(r.Contents, replacement)

	// Remove hash tag in front of links
	regex = `#(\[\[file:)`
	replacement = `$1`
	re = regexp.MustCompile(regex)
	r.Contents = re.ReplaceAllString(r.Contents, replacement)

}

func (r *Record) ConvertHyperLinks() {
	// https://orgmode.org/guide/Hyperlinks.html

	// Format Hyperlinks as per org-mode
	// Reference: https://regex101.com/r/iaTu7H/1
	regexL := `\[\s*(.+?)\s*\]\(\s*(.+?)\s*\)`
	replacementL := `[[$2][$1]]`
	reL := regexp.MustCompile(regexL)
	r.Contents = reL.ReplaceAllString(r.Contents, replacementL)

}

func (r *Record) FormatDates(names []string) {
	for _, n := range names {
		// Remove th, rd, st, nd,
		possibleDateStr := removeDaySuffixes(n)
		t, err := time.Parse("January 2 2006", possibleDateStr)
		if err != nil {
			continue // Skip any non-dates
		}
		regex := fmt.Sprintf(`\[\[file:%s.org\]\[%s\]\]`, n, n)
		replacement := t.Format("<2006-01-02 Mon>")
		var re = regexp.MustCompile(regex)
		r.Contents = re.ReplaceAllString(r.Contents, replacement)
	}
}

func removeDaySuffixes(possibleDateStr string) string {
	firstRegex := `st,`
	replacement := ``
	re := regexp.MustCompile(firstRegex)
	modifiedDateStr := re.ReplaceAllString(possibleDateStr, replacement)

	secondRegex := `nd,`
	re = regexp.MustCompile(secondRegex)
	modifiedDateStr = re.ReplaceAllString(modifiedDateStr, replacement)

	thirdRegex := `rd,`
	re = regexp.MustCompile(thirdRegex)
	modifiedDateStr = re.ReplaceAllString(modifiedDateStr, replacement)

	fourthRegex := `th,`
	re = regexp.MustCompile(fourthRegex)
	modifiedDateStr = re.ReplaceAllString(modifiedDateStr, replacement)

	return modifiedDateStr
}

func (r *Record) FixTaskKeywords() {
	// Fix DONE tasks
	regex := `{{\[\[file:DONE.org\]\[DONE\]\]}}`
	replacement := `DONE`
	re := regexp.MustCompile(regex)
	r.Contents = re.ReplaceAllString(r.Contents, replacement)

	// Fix TODO tasks
	regex = `{{\[\[file:TODO.org\]\[TODO\]\]}}`
	replacement = `TODO`
	re = regexp.MustCompile(regex)
	r.Contents = re.ReplaceAllString(r.Contents, replacement)

	// Move scheduled timestamps to next line with SCHEDULED: keyword
	regex = `(.*)TODO(.*)<(.*)>(.*)`
	replacement = `$1 TODO$2 $4
$1 SCHEDULED: <$3>`
	re = regexp.MustCompile(regex)
	r.Contents = re.ReplaceAllString(r.Contents, replacement)

	// Get rid of leading `-` in front of SCHEDULED keyword
	regex = `(-  )SCHEDULED:`
	replacement = `   SCHEDULED:`
	re = regexp.MustCompile(regex)
	r.Contents = re.ReplaceAllString(r.Contents, replacement)
}

func (r *Record) FormatBullets() {
	for i := MAX_BULLET_NESTING; i >= 0; i-- {
		regex := fmt.Sprintf("%*s", i*4, "- ")
		replacement := bullets(i)
		var re = regexp.MustCompile(regex)
		r.Contents = re.ReplaceAllString(r.Contents, replacement)
	}
	regex := `  \*\*`
	replacement := `**`
	var re = regexp.MustCompile(regex)
	r.Contents = re.ReplaceAllString(r.Contents, replacement)
}

func bullets(num int) string {
	bullets := ""
	for i := 0; i <= num; i++ {
		bullets = bullets + "*"
	}
	return bullets + " "
}

func (r *Record) RemoveRoamStyling() {
	regex := `### `
	replacement := ``
	var re = regexp.MustCompile(regex)
	r.Contents = re.ReplaceAllString(r.Contents, replacement)

	regex = `## `
	replacement = ``
	re = regexp.MustCompile(regex)
	r.Contents = re.ReplaceAllString(r.Contents, replacement)
}

func (r *Record) FixBidirectionalLinks() {
	regex := `\[\[([^file:][a-zA-Z0-9 !&,-.()?':]*)\]\]`
	replacement := `[[file:$1.org][$1]]`
	var re = regexp.MustCompile(regex)
	r.Contents = re.ReplaceAllString(r.Contents, replacement)
}

func (r *Record) FindAllBidirectionalLinkNames() []string {
	regex := `\[\[file:([^\]]*)`
	var re = regexp.MustCompile(regex)
	matches := re.FindAllStringSubmatch(r.Contents, -1)
	names := []string{}
	for _, m := range matches {
		names = append(names, m[1][:len(m[1])-4])
	}
	return names
}

func (r *Record) UnderscoreLinkedFileNames(names []string) {
	for _, n := range names {
		underscoredName := strings.ReplaceAll(n, " ", "_")
		regex := fmt.Sprintf(`\[\[file:%s.org\]\[%s\]\]`, n, n)
		replacement := fmt.Sprintf(`[[file:%s.org][%s]]`, underscoredName, n)
		var re = regexp.MustCompile(regex)
		r.Contents = re.ReplaceAllString(r.Contents, replacement)
	}
}

func (r *Record) Save() error {
	pathToDir := path.Dir(r.Path)
	err := os.MkdirAll(pathToDir, os.ModePerm)
	if err != nil {
		return err
	}
	err = ioutil.WriteFile(r.Path, []byte(r.Contents), 0644)
	if err != nil {
		return err
	}
	return nil
}

func (r *Record) HasTitle() bool {
	return strings.Contains(r.Contents, TITLE_PREFIX)
}

func (r *Record) Prepend(content string) {
	r.Contents = content + r.Contents
}
