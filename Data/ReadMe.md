# Data & Assets

This folder contains common data and other assets to help with this project.

## Remnote

- [rem.json](./rem.json) - this is the file that is used in all the scripts. This file is often replaced with Custom Sample, Demo Sample or My Original Data to convert files from one PKM tool to other.
- [prettyRem.json](./prettyRem.json) - this is a prettified version of [rem.json](./rem.json). This is generated using a python script:

        type rem.json | python -mjson.tool > prettyRem.json
- [rem-Demo.json](./rem-Demo.json) - this is the exported file from the default Remnote Demo
- [rem-customSample.json](./rem-customSample.json) - this is the exported file from a Remnote guest account with most simplistic Rem's
- [RemLanguages.json](./RemLanguages.json) - this is a JSON file which is used to convert Languages from Remnote to Org-Mode in Org Code-Blocks
- [PBI_RemnoteJSON.pbix](./PBI_RemnoteJSON.pbix) - this is used to understand the structure of the Remnote JSON Export and compare each row to understand what the key-value pair mean

## Org-Roam

- [PBI_Org-Roam database.pbix](./PBI_Org-Roam%20database.pbix) - this shows all the data from `org-roam.db` file create and maintained my org-roam package for emacs.