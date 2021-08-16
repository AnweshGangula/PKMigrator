# terminal code: "cd Remnote2Obsidian && python Remnote2Obsidian.py"

import sys, os, json

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
mainPageID = [x["children"] for x in RemnoteDocs if x["_id"] == homepageID][0]
# print([[x["key"], x["_id"]] for x in RemnoteDocs if x["key"] == [homepageName]])

def expandChildren(pages, ID):
    blockID = [x["children"] for x in pages if x["_id"] == ID][0]
    blockDict = [x for x in RemnoteDocs if x["_id"] in blockID]
    # Rem with "contains:" in key are auto-generated. So those will be removed
    filteredChildren = []
    for x in blockDict:
         if not x["key"] == [] and not "contains:" in x["key"] and not "rcrp" in x:
            if "type" in x and x["type"] == 6:
                 pass
            elif ID == homepageID:
                filteredChildren.append(x)
            else:
                text = ""
                for i in x["key"]:
                    if("_id" in i):
                        text += f'(({findByID(i["_id"])}))'
                    elif ("text" in i):
                        text += f'[{i["text"]}]({i["url"]})'
                    else:
                        text += i
                filteredChildren.append(text)

    return filteredChildren

def findByID(ID):
    key = [x["key"] for x in RemnoteDocs if x["_id"] in ID][0]
    text = ""
    for i in key:
        if("_id" in i):
            text += f'(({findByID(i["_id"])}))'
        elif ("text" in i):
            text += f'[{i["text"]}]({i["url"]})'
        elif (isinstance(i, str)):
            text += i
        else:
            pass
    return text


mainFiles = expandChildren(RemnoteDocs, homepageID)

for file in mainFiles:
    # print(file["key"][0])
    filename = os.path.join(Rem2ObsPath, file["key"][0] + ".md")

    child = expandChildren(RemnoteDocs, file["_id"])
    bullets = []
    expandBullets = ""
    for x in child:
        bullets.append("* " + x + "\n")
        expandBullets += "* " + x + "\n"
    with open(filename, mode="wt", encoding="utf-8") as f:
        f.write("# " + file["key"][0] + "\n" + expandBullets)

print(str(len(mainFiles)) + " files generated")
