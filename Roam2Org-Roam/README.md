# Roam .md to .org convertor 

This is a forked repository from [fabioberger/roam-migration](https://github.com/fabioberger/roam-migration) with few more **additional features**:

* Convert Markdown hyperlinks to match the syntax in org-mode i.e., `[Desc](URL)` to `[[URL][Desc]]`

___

A command-line tool to convert [Roam Research](https://roamresearch.com/) exported markdown files to [Org-roam](https://github.com/org-roam/org-roam) compatible markdown.

## Installation 

### Use a pre-built binary

Under the [Releases](https://github.com/fabioberger/roam-migration/releases) page we have pre-built binaries of the CLI available for most popular operating systems.

Download the relevant one for your system (e.g., darwin_amd64 for most MacOS users, etc...) and you're ready to go!

### Build from source

Building from source requires you to have [Golang](https://golang.org/) installed on your OS.

```
$ go get github.com/fabioberger/roam-migration
```

You should now have a CLI tool available called `roam-migration`

## Usage

First, go to Roam Research and click the three dots (`...`) in the top right corner and click "Export All". This will download a zip to your computer. Unzip this file by double clicking it. This will create a folder containing your Roam notes.

Then run the following:

```
$ roam-migration -p /path/to/roam-research-export
```

Replace the `/path/to/roam-research-export` with the path to where the Roam export directory was saved on your machine.

If you downloaded a pre-built binary, you additionally need to replace `roam-migration`, with to path the the downloaded binary. 

For example, if you downloaded the pre-built binary on a Mac, it might look something like this:

```
$ ~/Downloads/roam-migration_darwin_amd64 -p ~/Downloads/Roam-Export-1590095488816
```

Happy hacking! If you run into any unexpected errors, please open an [issue](https://github.com/fabioberger/roam-migration/issues/new). 

## CLI arguments

`-h string` -- See help menu 

`-p string` -- Path to directory containing your Roam Research export

## Limitations

There are currently a few known limitations of this conversion tool.

1. Block references

Since [Org-roam](https://github.com/org-roam/org-roam) doesn't have an equivalent concept to Roam's block references, if you use block references in your Roam notes, those references will simply duplicate the original content and insert them where the references were in your notes (within double quotes). This is done by the Roam exporter and this tool cannot convert them back into references.

2. Roam-specific Heading Styles

Roam Research allows you to style bullets as headers. This adds `#`, `##` or `###` depending on the header type into the exported markdown. Since these are nested within bullets however, they don't render properly as headers in org-roam. Additionally, org-mode already has default styling it applies to bullets based on nesting, so this tool strips out the hashes.

3. Notes with slashes (i.e., `/`) in their title are exported in nested folders

There seems to be a bug in the Roam exporter. If your note has a slash in it's title, Roam interprets it as a file path and exports this note into a nested folder along the file path encoded in the note's title. E.g., a note called `wine / beer` will create a file called ` beer.md` within a folder called `wine `. This tool does not currently try to fix this issue, but does convert nested files by traversing the export directory recurisively. If you wish to avoid this, remove the slashes in note titles before exporting your notes.
