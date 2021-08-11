# Roam JSON To Obsidian Converter

This is a forked repository from [renerocksai/rj2obs](https://github.com/renerocksai/rj2obs) with few more **additional features**:

* Convert code-blocks into proper markdown code-blocks
* Enclose any html tags in backtics so that they are not rendered by obsidian - eg: `` `<br>` ``
* Replace any underscore(`_`) in the UID of a block with hyphen(-) as obsidian doesn't support "`_`" in UID
* Preview Block-Refs by default
    * I have a custom CSS snippet for my Obsidian vault, that style the block-refs to look similar to Roam Research
___

Converts Roam JSON export to Obsidian Markdown files.

I wrote this to convert my own roam export into an Obsidian friendly format.

Output has the following directory structure:

* `md/` : contains all normal Markdown files
* `md/daily/`: contains all daily notes

### Features:

* Daily note format is changed to YYYY-MM-DD
* roam's block IDs are appended (only) to blocks actually referenced
    * e.g. `* this block gets referenced  ^someroamid`
* Blockrefs, block mentions, block embeds are replaced by their content with an appended Obsidian blockref link
    * e.g. `this block gets referenced  [[orignote#^someblockid]]`
* All notes are prefixed with a yaml header containing title and creation date:
```yaml
---
title:   
created: YYYY-MM-DD
---
```

* Top level roam blocks that don't contain children are not formatted as list
* Roam blocks containing linebreaks are broken down into multiple bullets
    * roam: 
        ```markdown

        * line 1
          line 2
        * next block
        ```
*
    * becomes:
        ```markdown
        * line 1
        * line 2

        * next block
        ```

**Note:** Please run Obsidian's Markdown importer after this conversion. It will fix #tag links and formattings (todo syntax, highlights, etc).

I might make it more user friendly and less hardcoded later. It did the job, though.

# Install
No need to install. But you need python3. Google is your friend. 

To install the required python packages:

```bash
pip install -r requirements.txt
```

# Usage:
```bash
python r2o.py my-roam-export.json
```

