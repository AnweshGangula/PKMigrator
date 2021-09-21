# RemNote JSON to Org converter
If your rem.json file is too large, VS Code may not be able to prettify it. You can [use python](https://stackoverflow.com/questions/19875218/best-way-to-format-large-json-file-30-mb) instead to prettify it: `type rem.json | python -mjson.tool > prettyRem.json`
___

## _TODO
* [ ] Block ref's or File ref's from parent folders need to be relative (E.g: ../../folder/file.org)
    * need to understand if ref is from same folder or different folder - incorrect logic in `Test File 2.1.org`
    * this is partially DONE - references in same parent folder are still added with full path
* [ ] Block Ref's for a bullet which has a link need to be formatted properly
    * E.g: [[../folder/file::*text\\[\\[url_within_ref\\]\\[url desc\\]\\]][actual block ref Desc.]]
    * [[file:Test Folder (Level 1)/Test File 1.1.org::*Sample Rem with Tag \\[\\[file:SampleTag1.org\\]\\[SampleTag1\\]\\]][Sample Rem with Tag SampleTag1]]
* [ ] convert block-ref's to org-transclutions:
    * Org-Tansclution: https://org-roam.discourse.group/t/alpha-org-transclusion/830

## How to use

This tool(`Remnote2Org.py`) is still work in progress
