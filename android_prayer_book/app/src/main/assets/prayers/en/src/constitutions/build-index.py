
from lxml import html
from os import listdir
from os.path import isfile, join, isdir
import codecs
import json
import re

pathroot = "./"

result = {
    "norms": [],
    "articles": []
}


def add_row(result, type, current):
    current["body"] = re.sub(r"\s+", " ", current["body"].strip())
    result[type].append(current)


for filename in (f for f in listdir(pathroot) if isfile(join(pathroot, f))):
    if filename in ["statutes.html", "history.html", "rule-augustine.html"] or filename.startswith('.') or not filename.endswith('.html'):
        continue
    current = None
    type = None
    with codecs.open(join(pathroot, filename), "r", encoding='utf8') as fp:
        text = fp.read()
        nodes = html.fromstring(text)
        for n in nodes.xpath("//body")[0]:
            if n.tag == 'h2':
                m = re.match('(\w+) (\d+)', n.text)
                if(m):
                    if m.group(1) == "Article":
                        type = "articles"
                    else:
                        type = "norms"
                    if current and type:
                        add_row(result, type, current)
                    current = {"id": int(m.group(2)), "body": "", "doc": filename}
            else:
                if current:
                    current["body"] = current["body"] + " " + n.text_content()
        if current and type:
            add_row(result, type, current)


with open('index.json', 'w') as fp:
    json.dump(result, fp, indent=4,)