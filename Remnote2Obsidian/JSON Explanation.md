If your rem.json file is too large, VS Code may not be able to prettify it. You can [use python](https://stackoverflow.com/questions/19875218/best-way-to-format-large-json-file-30-mb) instead to prettify it: `type rem.json | python -mjson.tool > pretty.json`

# Pages that can be ignored

* Personal folder is my main starting Rem with ID: `pAbgiAqZ45tLDzSpS`
    * Use `subBlocks` property in this object to get list of child Documents (not Rem - my home page only has documents)
* pages with contains in key is Auto-generated. Ignore these
    ```JSON
                "key": [
                    "contains:",
    ```
* pages with ID `tEhuuggyZDow3LAvz` & `KYJAcN5YzpL9MZX6k` are automatic page in Personal folder

# General Observations

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
* Any object containing `"rcre":` can be ignored - they are [Power-up Rems](https://www.redgregory.com/remnote-content/2020/11/1/a-list-of-remnotes-power-up-rems-and-what-they-do).
    * RegEx to find them: `\{((.|\n)*?"rcre")((.|\n)*?\})`
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
