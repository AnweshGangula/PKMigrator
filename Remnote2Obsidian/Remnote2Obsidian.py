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

remnoteJSON = json.load(open(jsonPath, mode="rt", encoding="utf-8", errors="ignore"))
RemnoteDocs = remnoteJSON["docs"]
mainPageID = [x["children"] for x in RemnoteDocs if x["_id"] == homepageID][0]
# print([[x["key"], x["_id"]] for x in RemnoteDocs if x["key"] == [homepageName]])

def main():
    mainFiles = expandChildren(homepageID)

    for file in mainFiles:
        filename = os.path.join(Rem2ObsPath, file["key"][0] + ".md")

        child = expandChildren(file["_id"])
        expandBullets = "\n".join(child)
        with open(filename, mode="wt", encoding="utf-8") as f:
            f.write("# " + file["key"][0] + "\n" + expandBullets)
        # print(f'{file["key"][0]}.md created')

    print(str(len(mainFiles)) + " files generated")


def ignoreRem(dict):
    if((dict["key"] == []) or ("contains:" in dict["key"]) or ("rcrp" in dict) or ("type" in dict and dict["type"] == 6)):
        return True
    else:
        return False


def expandChildren(ID, level=0):
    childID = [x["children"] for x in RemnoteDocs if x["_id"] == ID][0]
    filteredChildren = []
    text = ""

    childData = [x for x in RemnoteDocs if x["_id"] in childID]
    for x in childData:
        if not ignoreRem(x):
            if ID == homepageID:
                filteredChildren.append(x)
            else:
                prefix = ""
                if level >= 1:
                    prefix = "    " * level
                prefix += "* "
                text = prefix +  textFromKey(x["key"])
                filteredChildren.append(text)

                filteredChildren.extend(expandChildren(x["_id"], level + 1 ))

    return filteredChildren


def dictFromID(ID):
    dict=[]
    try:
        dict = [x for x in RemnoteDocs if x["_id"] in ID][0]
    except:
        # print(f"REM with ID: '{ID}' not found")
        pass
    return dict

def textFromKey(key):
    text = ""
    for item in key:
        if(isinstance(item, str)):
            text += item
        elif(item["i"] == "q" and "_id" in item):
            newDict = dictFromID(item["_id"])
            newKey = newDict["key"]
            newID = newDict["_id"]
            text += f'(({textFromKey(newKey)}^{newID}))'
        elif(item["i"] == "o"):
            text += f'```{item["language"]}\n{item["text"]}\n  ```'
        elif("q" in item and item["q"]):
            text += f'`{item["text"]}`'
        elif(item["i"] == "m" and "url" in item):
            text += f'[{item["text"]}]({item["url"]})'
        elif(item["i"] == "i" and "url" in item):
            text += f'![{item["url"]}]'
        else:
            pass
    return text


if __name__ == '__main__':
    main()
