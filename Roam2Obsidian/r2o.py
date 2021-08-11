# Save Roam JSON Export file in same folder and run following code in terminal `python r2o.py my-roam-export.json`

import sys
import os
import json
from tqdm import tqdm
import re
from dateutil.parser import parse
from datetime import datetime

yaml = """---
title:   {title}
created: {created}
---

"""

months = r"January|February|March|April|May|June|July|August|September|October|November|December"

# fr"() is a combination of f-string and raw strings
# escape literal braces in f-string: https://stackoverflow.com/a/5466478/6908282
re_daily = re.compile(fr"({months}) ([0-9]+)[a-z]{{2}}, ([0-9]{{4}})")
re_daylink = re.compile(fr"(\[\[)([{months} [0-9]+[a-z]{{2}}, [0-9]{{4}})(\]\])")
re_blockmentions = re.compile(r"({{mentions: \(\()(.{9})(\)\)}})")
re_blockembed = re.compile(r"({{embed: \(\()(.{9})(\)\)}})")
re_blockref = re.compile(r"(\(\()(.{9})(\)\))")
re_HTML = re.compile("(?<!`)<(?!\s|-).+?>(?!`)")
# Reference to above Regex: https://regex101.com/r/BVWwGK/10
re_Link = r"\[\s*(.+?)\s*\]\(\s*(.+?)\s*\)"
# Reference to above Regex: https://regex101.com/r/iaTu7H/1


def scan(jdict, page):
    u2b = {jdict["uid"]: jdict}
    for child in jdict.get("children", []):
        child["page"] = page
        u2b.update(scan(child, page))
    return u2b


def fence_HTMLtags(string):
    # Reference: https://regex101.com/r/BVWwGK/10
    if not string.startswith("```"):
        # \g<0> stands for whole match - so we're adding backtick (`) as suffix and prefix for whole match
        # reference: https://docs.python.org/3/library/re.html#re.sub
        # \g<0> instead of \0 - reference: https://stackoverflow.com/q/58134893/6908282
        string = re.sub(re_HTML, r"`\g<0>`", string)
    return string


def formatHyperLinks(string):
    # Remove leading and trailing whitespace: https://regex101.com/r/iaTu7H/1
    replacement = r"[\g<1>](\g<2>)"

    if not string.startswith("```"):
        string = re.sub(re_Link, replacement, string)
    return string


def replace_daylinks(s):
    new_s = s
    while True:
        m = re_daylink.search(new_s)
        if not m:
            break
        else:
            head = new_s[: m.end(1)]
            dt = parse(m.group(2))
            replacement = dt.isoformat()[:10]
            tail = "]]" + new_s[m.end(0) :]
            new_s = head + replacement + tail
    return new_s


def replace_blockrefs(s, uid2block, referenced_uids):
    new_s = s
    while True:
        m = re_blockembed.search(new_s)
        if m is None:
            m = re_blockmentions.search(new_s)
            if m is None:
                m = re_blockref.search(new_s)
        if m is None:
            break
        else:
            uid = m.group(2)
            if uid not in uid2block:
                print("************** uid not found:", uid)
            else:
                referenced_uids.add(uid)
                head = new_s[: m.start(1)]
                r_block = uid2block[uid]
                # shall we replace with the text or the link or both
                replacement = ""
                # replacement = r_block['string']
                replacement += f' ![[{r_block["page"]["title"]}#^{r_block["uid"].replace("_", "-")}]]'
                tail = new_s[m.end(3) :]
                new_s = head + replacement + tail
    return replace_daylinks(new_s)


def expand_children(block, uid2block, referenced_uids, level=0):
    lines = []
    for b in block.get("children", []):
        prefix = ""
        if level >= 1:
            prefix = "    " * level
        s = b["string"]
        children = b.get("children", [])

        headinglevel = b.get("heading", None)
        if headinglevel is not None:
            prefix = "#" * (headinglevel) + " " + prefix

        if children is None and level == 0:
            pass
        else:
            prefix += "* "

        uid = b["uid"]
        if uid in referenced_uids:
            postfix = f' ^{uid.replace("_", "-")}'
        else:
            postfix = ""

        # b id magic
        s = prefix + replace_blockrefs(s, uid2block, referenced_uids) + postfix
        if "\n" in s:
            prefix = prefix.replace("*", " ") if not s.startswith("```") else prefix
            new_s = s[:-1]
            new_s = new_s.replace("\n", "\n" + prefix)
            new_s += s[-1]
            new_s = (
                new_s[:-3] + "\n" + prefix + new_s[-3:]
                if not s.startswith("```")
                else s
            )  # move closing backticks (```) of code block to new line
            s = new_s + "\n"

        s = fence_HTMLtags(s)
        s = formatHyperLinks(s)
        lines.append(s)
        lines.extend(expand_children(b, uid2block, referenced_uids, level + 1))
    return lines


j = json.load(open(sys.argv[1], mode="rt", encoding="utf-8", errors="ignore"))

odir = "md"
ddir = "md/daily"
os.makedirs(ddir, exist_ok=True)

print("Pass 1: scan all pages")

uid2block = {}
referenced_uids = set()
pages = []

for page in tqdm(j):
    title = page["title"]
    created = page.get("create-time") or page["edit-time"]
    created = datetime.fromtimestamp(created / 1000).isoformat()[:10]
    children = page.get("children") or []

    is_daily = False
    m = re_daily.match(title)
    if m:
        is_daily = True
        dt = parse(title)
        title = dt.isoformat().split("T")[0]

    page = {
        "uid": None,
        "title": title,
        "created": created,
        "children": children,
        "daily": is_daily,
    }
    uid2block.update(scan(page, page))
    pages.append(page)

print("Pass 2: track blockrefs")
for p in tqdm(pages):
    expand_children(p, uid2block, referenced_uids)

print("Pass 3: generate")
error_pages = []
for p in tqdm(pages):
    title = p["title"]
    if not title:
        continue
    ofiln = f'{odir}/{p["title"]}.md'
    if p["daily"]:
        ofiln = f'{ddir}/{p["title"]}.md'

    # hack for crazy slashes in titles
    if "/" in title:
        d = odir
        for part in title.split("/")[:-1]:
            d = os.path.join(d, part)
            os.makedirs(d, exist_ok=True)

    lines = expand_children(p, uid2block, referenced_uids)
    try:
        with open(ofiln, mode="wt", encoding="utf-8") as f:
            f.write(yaml.format(**p))
            f.write("\n".join(lines))
    except:
        error_pages.append({"page": p, "content": lines})

if error_pages:
    print("The following pages had errors:")
    for ep in error_pages:
        p = ep["page"]
        t = p["title"]
        c = ep["content"]
        print(f"Title: >{t}<")
        print(f"Content:")
        print("    " + "\n    ".join(c))
print("Done!")
