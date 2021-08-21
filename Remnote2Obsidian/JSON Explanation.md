# rem.json Observations

If your rem.json file is too large, VS Code may not be able to prettify it. You can [use python](https://stackoverflow.com/questions/19875218/best-way-to-format-large-json-file-30-mb) instead to prettify it: `type rem.json | python -mjson.tool > pretty.json`
___

> ## TODO
> * [ ] Automatically look for folders with `"forceIsFolder": true` and `"parent": null` properties
>   * [ ] differentiate between bullet and file inside a folder REM (blocks vs children!!)
> * [ ] Exclude unnecessary Power-Up Rem's
> * [x] Indent newlines in code-block and remove bullets
> * [x] Add Block-ref's and page ref's

## Pages that can be ignored

* Personal folder is my main starting Rem with ID: `pAbgiAqZ45tLDzSpS`
    * Use `subBlocks` property in this object to get list of child Documents (not Rem - my home page only has documents)
* pages with contains in key is Auto-generated. Ignore these
    ```JSON
                "key": [
                    "contains:",
    ```
* pages with ID `tEhuuggyZDow3LAvz` & `KYJAcN5YzpL9MZX6k` are automatic page in Personal folder

## General Observations

* If Rem's are created separately for each Block Ref, they follow this pattern!! - `"i": "q"` or `"rcrp":`
    ```JSON
    "key": [
        {
            "i": "q",
            "_id": "p3xgRaGLQ3jEHJE98"
        }
    ```
    * Find them using below search (includes the necessary whitespaces if JSON is prettified)
        ```JSON
                    "key": [
                        {
                            "_id":
        ```
        * or `"key":[{"_id":"` in un-prettified version <br>
        * or [RegEx match](https://regex101.com/r/tL9OZ7/5/) 
            * `\{"key":\[\{"_id":".*?","i":"q"\},""\].*?\}` in un-prettified version or 
            * `(\{\s*"key":\s*\[\s*\{\s*"_id":\s*".*?",\s*"i":\s*"q"\s*\},\s*""\s*\])((.|\n)*?\})` in both versions
    * but these are valid Rem's
        ```JSON
            "key": [
                "Sed is similar to ",
                {
                    "_id": "d6EBzKXA5Rh5kyPDN",
                    "i": "q"
                },
                " , but it is mostly used by  Linux users"
            ]
        ```

* Objects with blank array of key property can be ignored - `"key":[]`
* Any object containing `"rcre":` or `"rcrt": ` or `"rcrs": ` can be ignored - they are [Power-up Rems](https://www.redgregory.com/remnote-content/2020/11/1/a-list-of-remnotes-power-up-rems-and-what-they-do).
    * RegEx to find them: `\{((.|\n)*?"rcre")((.|\n)*?\})`
    * Object with `"rcrt": "c"` is **Custom CSS**
    * Object with `"rcrt": "t"` is **TODO**
    * Object with `"rcrt": "d"` is **Daily Documents**

    * [x] Note: Check for all `"rcrt"` is done
* Any object containing `"rcrp":` can be ignored
    * these are actually metadata of Rem (Heading Level, color, status etc...) - These can be ignored**
    * Understand of values:
        * `r.s`: Rem Size (Heading level)
        * `h.c`: highlight color
        * `o.s`: original status
        * `t.s`: Status: Unfinished
        * `l.a`: Aliases
* Objects with `"type": 2,` as a property are rems' with spaced repitition feature
* Objects with `"type": 6` as property are either blank (`"key":[]`) or additional Block Ref Rem - Can be ignored
* Objects with `"i": "o"` arer code blocks. They follow the below pattern:
    ```
                "key": [
                    {
                        "i": "o",
                        "language": "
    ```
* Object with `"n": 1` as a property are Top-level Rem's
* Object with `"forceIsFolder": true` as a property are folders. 
    * objects with `"parent": null` and `"forceIsFolder": true` can be used for initiation loop.
* Object with `"i": "i"` as a property in `key` are images
* Object with `"i": "m"` and `"b": true` as a property in `key` are bold text
* Object with `"i": "m"` and `"x": true` as a property in `key` are LaTeX text
* Object with `"i": "m"` and `"q": true` as a property in `key` are inline code
* Object with `"i": "m"` and `"u": true` as a property in `key` are emptry text (typically appear before underscore(_))
* Object with `"i": "m"` and `"url": ` as a property in `key` are URL links
* Object with `"i": "m"` and `"h": ` as a property in `key` are Highlighted Text
* Object with `"references": [\n` has been referenced in other blocks

* `typeParents: ` property is a list of Tags added to the REM

# Power Query function to extract Text-From-Key
```js
let
    Source = (keyColumn as any) => let
        #"Expanded Text" = if Value.Type(keyColumn) = type text or keyColumn is null then keyColumn 
            else if keyColumn[i]="q" and Record.HasFields(keyColumn, "_id") then "((" & keyColumn[_id] & "))" 
            else if keyColumn[i]="o" then "```"& keyColumn[language] & "#(lf)" & keyColumn[text] & "#(lf)" & "```"
            else if Record.HasFields(keyColumn, "q") and keyColumn[q] then "`" & keyColumn[text] & "`"
            else if keyColumn[i]="m" and Record.HasFields(keyColumn, "url") then "[" & keyColumn[text] & "](" & keyColumn[url] & ")" 
            else if keyColumn[i]="i" and Record.HasFields(keyColumn, "url") then "![" & keyColumn[url] & "]" 
            else if Record.HasFields(keyColumn, "text") then keyColumn[text] 
            else keyColumn[_id]
    in
        #"Expanded Text"
in
    Source
```
