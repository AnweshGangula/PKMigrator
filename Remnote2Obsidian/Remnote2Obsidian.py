# terminal code: "cd Remnote2Obsidian && python Remnote2Obsidian.py"

import sys
import os
import json

# user-input variables: ----------------------------------------
jsonPath = "rem.json"
homepageID = "pAbgiAqZ45tLDzSpS"
folderName = "Rem2Obs"
# ---------------------------------------------------------------

dir_path = os.path.dirname(os.path.realpath(__file__))
# jsonPath = sys.argv[1]

Rem2ObsPath = os.path.join(dir_path, folderName)
os.makedirs(Rem2ObsPath, exist_ok=True)


j = json.load(open(jsonPath, mode="rt", encoding="utf-8", errors="ignore"))

RemnoteDocs = j["docs"]

mainPages = [x["subBlocks"] for x in RemnoteDocs if x["_id"] == homepageID][0]
filteredPages = [x for x in RemnoteDocs if x["_id"] in mainPages]
mainFiles = [x for x in filteredPages if not "contains:" in x["key"]]  # Rem with "contains:" in key are auto-generated

for file in mainFiles:
    # print(file["key"][0])
    filename = os.path.join(Rem2ObsPath, file["key"][0] + ".md")
    with open(filename, mode="wt", encoding="utf-8") as f:
        f.write("# " + file["key"][0])

print(str(len(mainFiles)) + " files generated")