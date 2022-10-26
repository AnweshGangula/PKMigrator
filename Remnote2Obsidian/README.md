# RemNote JSON to Obsidian converter

## _TODO
* [ ] include portals in bullets
* [ ] Preserve the order of REM's as per Remnote Web app
* [ ] Remove unnecessary files outside my personal Remnote

## How to use

1. Export your notes from Remnote in JSON format (remnote ouputs the data in a zip folder)
2. Extract the ZIP folder and look for the file `rem.json`
    * OPTIONAL: if you'd like to prettify the `rem.json` file to make it human readable, you can use the following command in terminal (after switching to the same directoty as the file): `type .\Data\rem.json | python -m json.tool > .\Data\prettyRem.json`. A new file called `prettyRem.json` will be created.
3. Copy the file into this directory
4. Once the file is copied, open a terminal and `cd` to this directory
5. Finally, run the following command in terminal `python Remnote2Obsidian.py`
6. This will create a new folder named **Rem2Obs** (folder name can be changed), with all your Remnote files and notes
