
* Rem's created separately for each Block Ref!! - `"i": "q"`
    ```JSON
    "key": [
        {
            "i": "q",
            "_id": "p3xgRaGLQ3jEHJE98"
        }
    ```
    * Find them using below search (includes the necessary namespaces if JSON is prettified)
        ```JSON
                    "key": [
                        {
                            "_id":
        ```
        or `"key":[{"_id":"` in un-prettified version <br>
        or RegEx match `\{"key":\[\{"_id":".*?","i":"q"\},""\]`
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