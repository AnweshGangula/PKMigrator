# terminal code: "cd Remnote2Obsidian && python Remnote2Obsidian.py"

# print("Python execution started")
import sys, os, json, datetime, re

# Import modules from current project:
from progressBar import printProgressBar 

# Custom Package installation

start_time = datetime.datetime.now()
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
Rem2ObsPath = os.path.join(os.path.dirname(jsonPath), folderName)
os.makedirs(Rem2ObsPath, exist_ok=True)

remnoteJSON = json.load(open(jsonPath, mode="rt", encoding="utf-8", errors="ignore"))
RemnoteDocs = remnoteJSON["docs"]

allParentRem = [x for x in RemnoteDocs if "n" in x and  x["n"] == 1]
# allFolders = [x for x in RemnoteDocs if "forceIsFolder" in x and  x["forceIsFolder"]]
# topFolders = [x for x in allFolders if x["parent"] == None]


def getAllDocs(RemList):
    IDlist = []
    for rem in RemList:
        IDlist.append(rem["_id"])
        if "forceIsFolder" in rem and  rem["forceIsFolder"]:
            childRem = []
            for child in rem["children"]:
                dict = [x for x in RemnoteDocs if x["_id"] == child][0] 
                childRem.append(dict)
            IDlist.extend(getAllDocs(childRem))
    return IDlist

allDocID = getAllDocs(allParentRem)
# allDocID is used in textFromID function

created = []
notCreated = []
def main():
    printProgressBar(0, len(allParentRem), prefix = 'Progress:', suffix = 'Complete', length = 50)
    i=0
    for dict in allParentRem:
        i += 1
        printProgressBar(i, len(allParentRem), prefix = 'Progress:', suffix = 'Complete', length = 50)
        createFile(dict["_id"], Rem2ObsPath)

    timetaken = str(datetime.datetime.now() - start_time)
    print(f"\nTime Taken to Process PDF: {timetaken}")
    print("\n" + str(len(created)) + " files generated")
    print(str(len(notCreated)) + " file/s listed below could not be generated\n" + "\n".join(notCreated)) if len(notCreated)>0 else None


def createFile(remID, remFilePath):
    # this is recursive function, so cannot be moved directly to main() function
    if ignoreRem(remID):
        return
    remText = textFromID(remID)
    remDict = dictFromID(remID)
    if "forceIsFolder" in remDict and remDict["forceIsFolder"]:
            newFilePath = os.path.join(remFilePath, remText)
            for child in remDict["children"]:
                createFile(child, newFilePath)
    else:
        os.makedirs(remFilePath, exist_ok=True)
        filename = remText
        # filename = re.sub('[^\w\-_\. ]', '_', filename)
        filePath = os.path.join(remFilePath, filename + ".md")

        try:
            with open(filePath, mode="wt", encoding="utf-8") as f:
                child = expandChildren(remID)
                expandBullets = "\n".join(child)

                f.write("# " + filename + "\n" + expandBullets)
            # print(f'{remText}.md created')
            created.append("ID: " + remID + ",  Name: " + filename)
        except Exception as e:
            print(e)
            notCreated.append("ID: " + remID + ",  Name: " + filename)
            # print("\ncannot create file with ID: " + remID + ", Name: "+ filename + "\n")
    


def ignoreRem(ID):
    # TODO: add more ignore ID's
    ignoreID = ["9onq37x6PbsFxvRqu", "6sz2MJeFLZoTRQofZ"]
    dict = dictFromID(ID)
    if(dict == []
    or dict["key"] == [] 
    or ("contains:" in dict["key"]) 
    or ("rcrp" in dict) 
    or ("rcrs" in dict) 
    or ("rcrt" in dict and dict["rcrt"] != "c")
    or ("type" in dict and dict["type"] == 6)):
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
        dict = [x for x in RemnoteDocs if x["_id"] == ID][0]
    except Exception as e:
        # print(e)
        # print(f"REM with ID: '{ID}' not found")
        pass
    return dict

def textFromID(ID, level = 0):
    dict = dictFromID(ID)
    key = dict["key"]
    text = ""
    for item in key:
        if(isinstance(item, str)):
            text += item
        elif(item["i"] == "q" and "_id" in item):
            newDict = dictFromID(item["_id"])
            newID = newDict["_id"]
            if newID in allDocID:
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

    if level == 0:
        # level is used to disable recursive expansion, since tags don't need to be recursive
        if (("typeParents" in dict and len(dict["typeParents"])>0) 
        and not ID in allDocID 
        and not("forceIsFolder" in dict and  dict["forceIsFolder"])):
            text += addTags(dict)
    return text


def addTags(dict):
    text = ""
    for x in dict["typeParents"]:
        if not ignoreRem(x):
            textExtract = textFromID(x, level = 1).strip()
            textExtract = re.sub(r'[^A-Za-z0-9-]+', '_', textExtract)
            text += f' #{textExtract}'
        
    return text


def parentFromID(ID):
    fileName = ""
    dict = dictFromID(ID)
    if(ID in allDocID or ("parent" in dict and dict["parent"] == None)):
        fileName =  textFromID(ID)
    elif dict["parent"] in allDocID:
        fileName = textFromID(dict["parent"])
    else:
        fileName = parentFromID(dict["parent"])

    return fileName

if __name__ == '__main__':
    main()
