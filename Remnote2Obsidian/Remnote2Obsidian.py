# terminal code: "cd Remnote2Obsidian && python Remnote2Obsidian.py"

import sys
import os
import json

jsonPath = "rem.json"
# jsonPath = sys.argv[1]

j = json.load(open(jsonPath, mode="rt", encoding="utf-8", errors="ignore"))

RemnoteDocs = j["docs"]

print([x["key"] for x in RemnoteDocs if x["_id"] == "pAbgiAqZ45tLDzSpS"])