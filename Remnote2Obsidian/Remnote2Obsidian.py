# terminal code: "cd Remnote2Obsidian && python Remnote2Obsidian.py"

import sys, os, json

dir_path = os.path.dirname(os.path.realpath(__file__))

# user-input variables: ----------------------------------------
jsonFile = "rem.json"
jsonPath = os.path.join(dir_path, jsonFile)
# jsonPath = sys.argv[1]
# homepageName = "Personal"
homepageID = "pAbgiAqZ45tLDzSpS" # you can find this in the URL (eg: https://www.remnote.io/document/HrxrQbMC3fXbBpWPB)
folderName = "Rem2Obs"
# ---------------------------------------------------------------

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
    text = ""
    for x in blockDict:
        if not x["key"] == [] and not "contains:" in x["key"] and not "rcrp" in x:
            if "type" in x and x["type"] == 6:
                continue
            elif ID == homepageID:
                filteredChildren.append(x)
            else:
                text = textFromKey(x["key"])
                filteredChildren.append(text)

                if(len(x["children"])>0):
                    for child in x["children"]:
                        # print({"child: " + child, "Parent: " +  x["_id"]})
                        filteredChildren.extend(expandChildren(RemnoteDocs, child))

    return filteredChildren


def keyByID(ID):
    key=[]
    try:
        key = [x["key"] for x in RemnoteDocs if x["_id"] in ID][0]
    except:
        # print(f"REM with ID: '{ID}' not found")
        pass
    return key

def textFromKey(key):
    text = ""
    for item in key:
        if(isinstance(item, str)):
            text += item
        elif(item["i"] == "q" and "_id" in item):
            text += f'((^{textFromKey(keyByID(item["_id"]))}))'
        elif(item["i"] == "o"):
            text += f'```{item["language"]}\n{item["text"]}\n```'
        elif("q" in item and item["q"]):
            text += f'`{item["text"]}`'
        elif(item["i"] == "m" and "url" in item):
            text += f'[{item["text"]}]({item["url"]})'
        elif(item["i"] == "i" and "url" in item):
            text += f'![{item["url"]}]'
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
    # print(f'{file["key"][0]}.md created')

print(str(len(mainFiles)) + " files generated")
