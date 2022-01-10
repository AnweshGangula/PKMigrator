# RemNote JSON to Org converter
If your rem.json file is too large, VS Code may not be able to prettify it. You can [use python](https://stackoverflow.com/questions/19875218/best-way-to-format-large-json-file-30-mb) instead to prettify it:\
```
type rem.json | python -mjson.tool > prettyRem.json
```
`rem.json` is the relative file path of the json input file and `prettyRem.json` is the output file path
___

## _TODO
* [ ] Block ref's or File ref's from parent folders need to be relative (E.g: ../../folder/file.org)
    * need to understand if ref is from same folder or different folder - incorrect logic in `Test File 2.1.org`
    * this is partially DONE - references in same parent folder are still added with full path
* ~~[x] Block Ref's for a bullet which has a link need to be formatted properly~~
    * > Org-Roam doesn't need links to be expanded with reference
    * E.g: `[[../folder/file::*text\\[\\[url_within_ref\\]\\[url desc\\]\\]][actual block ref Desc.]]`
    * `[[file:Test Folder (Level 1)/Test File 1.1.org::*Sample Rem with Tag \\[\\[file:SampleTag1.org\\]\\[SampleTag1\\]\\]][Sample Rem with Tag SampleTag1]]`
* [x] Block Ref's for a bullet which has a link need to be formatted as plain text
    * E.g: Sample Rem with Tag `Sample Rem with Tag [[id:KdhgZRqGZThRY2a3a][SampleTag1]]` with `ID: FCceZrymThCCYGP72` can be referenced as `[[id:FCceZrymThCCYGP72][Sample Rem with Tag SampleTag1]]`
    * > Note: This probably doesn't work without org-roam
* [ ] convert block-ref's to org-transclutions:
    * Org-Tansclution: https://org-roam.discourse.group/t/alpha-org-transclusion/830
* [ ] Org-Roam: Create properties for bullets that are references (`org-id-get-create`)
* [ ] Create a function to add metadata to files or nodes
* [ ] Update [./orgLanguages.json](orgLanguages.json) as per OrgMode languages
    * E.g: json is not a supported language in orgmode - so JSON syntax highlighting is probably Javascript(js)

## How to use

This tool ([Remnote2OrgMode](./Remnote2OrgMode.py) or [Remnote2OrgRoam](./Remnote2OrgRoam.py)) is still work in progress
