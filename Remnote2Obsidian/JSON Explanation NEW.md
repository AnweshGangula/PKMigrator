# Decoding the JSON Export

Revisiting the JSON export explanation to make it more readable

- Bold Text
    - `"i": "m"` & `"b": true`
- URL REM
    - Inline Link
        -  `"i": "m"` & `"qId": `
    - REM Reference
        - `"i": "q"` & `"_id": ` and 
        - `dict("_id")` should have `"crt": { "b":`
            - URL Link = `crt["b"]["u"]["s"]`
            - URL Title = URL = `crt["b"]["t"]["s"]`
        - `"content": false` can also be used to identify - but its not 100% accurate
- LaTeX
    - `"i": "m"` & `"x": true`