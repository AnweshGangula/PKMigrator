# terminal code: "cd Remnote2Obsidian && python Remnote2Obsidian.py"

import sys
import os
import json

# user-input variables: ----------------------------------------
jsonPath = "rem.json"
# jsonPath = sys.argv[1]
# homepageName = "Personal"
homepageID = "pAbgiAqZ45tLDzSpS" # you can find this in the URL (eg: https://www.remnote.io/document/HrxrQbMC3fXbBpWPB)
folderName = "Rem2Obs"
# ---------------------------------------------------------------

dir_path = os.path.dirname(os.path.realpath(__file__))
Rem2ObsPath = os.path.join(dir_path, folderName)
os.makedirs(Rem2ObsPath, exist_ok=True)

j = json.load(open(jsonPath, mode="rt", encoding="utf-8", errors="ignore"))
RemnoteDocs = j["docs"]

mainPagesID = [x["subBlocks"] for x in RemnoteDocs if x["_id"] == homepageID][0]
# print([[x["key"], x["_id"]] for x in RemnoteDocs if x["key"] == [homepageName]])
mainPages = [x for x in RemnoteDocs if x["_id"] in mainPagesID]

def filterChildren(pages):
    filteredChildren = [x for x in pages if not "contains:" in x["key"]]

    return filteredChildren


filteredPages = filterChildren(mainPages) # Rem with "contains:" in key are auto-generated

for file in filteredPages:
    # print(file["key"][0])
    filename = os.path.join(Rem2ObsPath, file["key"][0] + ".md")
    with open(filename, mode="wt", encoding="utf-8") as f:
        f.write("# " + file["key"][0])

print(str(len(filteredPages)) + " files generated")
