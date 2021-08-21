# terminal code: "cd Remnote2Obsidian && python Remnote2Obsidian.py"

# print("Python execution started")
import sys, os, json, datetime, re

# Import modules from current project:
from progressBar import printProgressBar 

# Custom Package installation
from dateutil.parser import parse as dateParse

start_time = datetime.datetime.now()
dir_path = os.path.dirname(os.path.realpath(__file__))

# user-input variables: ----------------------------------------
jsonFile = "rem.json"
# jsonPath = sys.argv[1]
folderName = "Rem2Obs"
dailyDocsFolder = "Daily Documents"

re_HTML = re.compile("(?<!`)<(?!\s|-).+?>(?!`)")
# ---------------------------------------------------------------

jsonPath = os.path.join(dir_path, jsonFile)
Rem2ObsPath = os.path.join(os.path.dirname(jsonPath), folderName)
os.makedirs(Rem2ObsPath, exist_ok=True)

remnoteJSON = json.load(open(jsonPath, mode="rt", encoding="utf-8", errors="ignore"))
RemnoteDocs = remnoteJSON["docs"]

allParentRem = []
# allFolders = []
# topFolders = []
for x in RemnoteDocs:
    if("n" in x and  x["n"] == 1):
        allParentRem.append(x)
        if("rcrt" in x and x["rcrt"] == "d"):
            # Convert Daily Documents to folder
            x["key"][0] = dailyDocsFolder
            x["forceIsFolder"] = True
    # if "forceIsFolder" in x and  x["forceIsFolder"]:
    #     allFolders.append(x)
    #     if x["parent"] == None:
    #         topFolders.append(x)


def getAllDocs(RemList):
    IDlist = []
    for rem in RemList:
        if "forceIsFolder" in rem and  rem["forceIsFolder"]:
            childRem = []
            for child in rem["children"]:
                dict = [x for x in RemnoteDocs if x["_id"] == child][0] 
                childRem.append(dict)
            IDlist.extend(getAllDocs(childRem))
        if(len(rem["children"])>0
        or (len(rem.get("portalsIn", []))>0)
        or (len(rem.get("references", []))>0)
        or (len(rem.get("typeChildren", []))>0)):
            IDlist.append(rem["_id"])
        else:
            # print("REM not used anywhere")
            pass
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
        if ignoreRem(dict["_id"]):
            continue
        printProgressBar(i, len(allParentRem), prefix = 'Progress:', suffix = 'Complete', length = 50)
        createFile(dict["_id"], Rem2ObsPath)

    timetaken = str(datetime.datetime.now() - start_time)
    print(f"\nTime Taken to Generate Obsidian Vault: {timetaken}")
    print("\n" + str(len(created)) + " files generated")
    print(str(len(notCreated)) + " file/s listed below could not be generated\n" + "\n".join(notCreated)) if len(notCreated)>0 else None


def createFile(remID, remFolderPath):
    # this is recursive function, so cannot be moved directly to main() function
    if ignoreRem(remID):
        return
    remText = textFromID(remID)
    remDict = dictFromID(remID)
    if "forceIsFolder" in remDict and remDict["forceIsFolder"]:
            newFilePath = os.path.join(remFolderPath, remText)
            for child in remDict["children"]:
                createFile(child, newFilePath)
    else:
        os.makedirs(remFolderPath, exist_ok=True)
        filename = remText
        fileTitle = filename
        # filename = re.sub('[^\w\-_\. ]', '_', filename)
        if(os.path.basename(remFolderPath) == dailyDocsFolder):
            # dailyDocName = datetime.datetime.strptime(filename, "%B %dth, %Y").date()
            dailyDocName = dateParse(filename)
            filename = dailyDocName.strftime("%Y-%m-%d")
            # fileTitle += " (" + filename + ")"
        filePath = os.path.join(remFolderPath, filename + ".md")

        try:
            with open(filePath, mode="wt", encoding="utf-8") as f:
                child = expandChildren(remID)
                expandBullets = "\n".join(child)

                f.write("# " + fileTitle + "\n" + expandBullets)
            # print(f'{remText}.md created')
            created.append("ID: " + remID + ",  Name: " + filename)
        except Exception as e:
            # print(e)
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
    or ("rcrt" in dict and dict["rcrt"] != "c" and dict["rcrt"] != "d")
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
            prefix = ""
            if level >= 1:
                prefix = "    " * level
            prefix += "* "
            text = prefix +  textFromID(x["_id"])
            if "references" in x and not(x["references"] == []):
                text += f' ^{x["_id"].replace("_", "-")}'
            if "\n" in text:
                # text = text.replace("\r", "\n")
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

    todoStatus = getTODO(dict)
    if todoStatus == "Finished":
        text += "[x] "
    elif todoStatus == "Unfinished":
        text += "[ ] "

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
    
    text = fence_HTMLtags(text)
    return text


def addTags(dict):
    text = ""
    for x in dict["typeParents"]:
        if not ignoreRem(x):
            textExtract = textFromID(x, level = 1).strip()
            textExtract = re.sub(r'[^A-Za-z0-9-]+', '_', textExtract)
            text += f' #{textExtract}'
        
    return text


def getTODO(keyDict):
    if isinstance(keyDict["key"][0], dict) and keyDict["key"][0].get("i") == "o":
        # Excludue "Custom CSS" Rem - Dont add Todo check-boxes from here
        # Typically, CSS code-block has only one item in the key dictionary and all code-block have property `"i": "o"` 
        return False
    todo = keyDict.get("crt")
    if todo and "t" in todo:
        todoStatus = todo["t"]["s"]["s"]
        return todoStatus
    else:
        return False

def fence_HTMLtags(string):
    # Reference: https://regex101.com/r/BVWwGK/10
    if not string.startswith("```"):
        # \g<0> stands for whole match - so we're adding backtick (`) as suffix and prefix for whole match
        # reference: https://docs.python.org/3/library/re.html#re.sub
        # \g<0> instead of \0 - reference: https://stackoverflow.com/q/58134893/6908282
        string = re.sub(re_HTML, r"`\g<0>`", string)
    return string


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
