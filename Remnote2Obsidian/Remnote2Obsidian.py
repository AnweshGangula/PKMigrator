# terminal code: "cd Remnote2Obsidian && python Remnote2Obsidian.py"

import sys, os, json, re

dir_path = os.path.dirname(os.path.realpath(__file__))

# user-input variables: ----------------------------------------
jsonFile = "rem.json"
# jsonPath = sys.argv[1]
# homepageName = "Personal"
homepageID = "pAbgiAqZ45tLDzSpS" # you can find this in the URL (eg: https://www.remnote.io/document/HrxrQbMC3fXbBpWPB)
dailyDocsID = "dyqaWLHtstN4iqAYk"
includeTopLevelRem = True
includeCustomCSS = True
folderName = "Rem2Obs"
# ---------------------------------------------------------------

jsonPath = os.path.join(dir_path, jsonFile)
Rem2ObsPath = os.path.join(dir_path, folderName)
os.makedirs(Rem2ObsPath, exist_ok=True)

remnoteJSON = json.load(open(jsonPath, mode="rt", encoding="utf-8", errors="ignore"))
RemnoteDocs = remnoteJSON["docs"]

allParentRem = [x for x in RemnoteDocs if "n" in x and  x["n"] == 1]
allFolders = [x for x in RemnoteDocs if "forceIsFolder" in x and  x["forceIsFolder"]]
topFolders = [x for x in allFolders if x["parent"] == None]

mainPageID = [x["children"] for x in RemnoteDocs if x["_id"] == homepageID][0]
# print([[x["key"], x["_id"]] for x in RemnoteDocs if x["key"] == [homepageName]])

if includeTopLevelRem:
    parentRem = [x["_id"] for x in RemnoteDocs if "parent" in x and x["parent"] == None]
    # print(parentRem)
    mainPageID = mainPageID + list(set(parentRem) - set(mainPageID))

def main():

    created = []
    notCreated = []
    for folder in topFolders:
        for file in folder["children"]:
            folderPath = os.path.join(Rem2ObsPath, folder["key"][0])
            os.makedirs(folderPath, exist_ok=True)
            filename = textFromID(file)
            # filename = re.sub('[^\w\-_\. ]', '_', filename)
            filePath = os.path.join(folderPath, filename + ".md")

            try:
                with open(filePath, mode="wt", encoding="utf-8") as f:
                    child = expandChildren(file)
                    expandBullets = "\n".join(child)

                    f.write("# " + filename + "\n" + expandBullets)
                # print(f'{file["key"][0]}.md created')
                created.append("ID: " + file + ",  Name: " + filename)
            except:
                notCreated.append("ID: " + file + ",  Name: " + filename)
                print("\ncannot create file with name: " + filename)

    print("\n" + str(len(created)) + " files generated")
    print(str(len(notCreated)) + " file/s listed below could not be generated\n" + "\n".join(notCreated)) if len(notCreated)>0 else None


def ignoreRem(ID):
    dict = dictFromID(ID)
    if((dict["key"] == []) 
    or ("contains:" in dict["key"]) 
    or ("rcrp" in dict) 
    or ("rcrs" in dict) 
    or ("rcrt" in dict and dict["rcrt"] != "c")
    or ("type" in dict and dict["type"] == 6)
    ):
        return True
    else:
        return False


def expandChildren(ID, level=0):
    childID = [x["children"] for x in RemnoteDocs if x["_id"] == ID][0]
    filteredChildren = []
    text = ""

    childData = [x for x in RemnoteDocs if x["_id"] in childID]
    for x in childData:
        if not ignoreRem(x["_id"]):
            if(ID == homepageID) or ("parent" in x and x["parent"] == None):
                # filteredChildren.append(x)
                pass
            else:
                prefix = ""
                if level >= 1:
                    prefix = "    " * level
                prefix += "* "
                text = prefix +  textFromID(x["_id"])
                if "references" in x and not(x["references"] == []):
                    text += f' ^{x["_id"].replace("_", "-")}'
                if "\n" in text:
                    text = text.replace("\r ", "\n")
                    text = text.replace("\n", "\n" + prefix.replace("*", " "))
                filteredChildren.append(text)

                filteredChildren.extend(expandChildren(x["_id"], level + 1 ))

    return filteredChildren


def dictFromID(ID):
    dict=[]
    try:
        dict = [x for x in RemnoteDocs if x["_id"] in ID][0]
    except:
        print(f"REM with ID: '{ID}' not found")
        # pass
    return dict

def textFromID(ID):
    key = dictFromID(ID)["key"]
    text = ""
    for item in key:
        if(isinstance(item, str)):
            text += item
        elif(item["i"] == "q" and "_id" in item):
            newDict = dictFromID(item["_id"])
            newID = newDict["_id"]
            if newID in mainPageID:
                text += f'[[{parentFromID(newID)}]]'
            else:
                text += f'![[{parentFromID(newID)}#^{newID}]]'
        elif(item["i"] == "o"):
            text += f'```{item["language"]}\n{item["text"]}\n  ```'
        elif(item["i"] == "m"):
            currText = item["text"]
            if ("url" in item):
                text += f'[{currText}]({item["url"]})'
            if (currText.strip() == ""):
                text += currText
            elif("q" in item and item["q"]):
                text += f'`{currText}`'
            elif("b" in item and item["b"]):
                if("h" in item and item["h"]):
                    text += f'==**{currText}**=='
                else:
                    text += f'**{currText}**'
            elif("x" in item and item["x"]):
                text = f'$${currText}$$'
            elif("u" in item and item["u"]):
                text += currText
        elif(item["i"] == "i" and "url" in item):
            text += f'![]({item["url"]})'
        else:
            print("ERROR at textFromID function for ID: " + ID)
    return text


def parentFromID(ID):
    fileName = ""
    dict = dictFromID(ID)
    if(ID in mainPageID or "parent" not in dict or dict["parent"] == None):
        fileName =  textFromID(ID)
    elif dict["parent"] in mainPageID:
        fileName = textFromID(dict["parent"])
    else:
        fileName = parentFromID(dict["parent"])

    return fileName

if __name__ == '__main__':
    main()
