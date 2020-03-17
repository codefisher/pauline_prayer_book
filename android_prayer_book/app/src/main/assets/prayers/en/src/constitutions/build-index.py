
from lxml import html
from os import listdir
from os.path import isfile, join, isdir
import codecs
import json
import re
import sys
import getopt

opts, args = getopt.getopt(sys.argv[1:], "", ["input=", "article="])
command_opts = dict(opts)
pathroot = command_opts.get("--input", "./")
article_title = command_opts.get("--article", "Article")

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
        title_text = nodes.xpath("//title")[0].text.partition(":")[2].strip()
        for n in nodes.xpath("//body")[0]:
            if n.tag == 'h2':
                m = re.match('(\w+) (\d+)', n.text)
                if(m):
                    if m.group(1) == article_title:
                        type = "articles"
                    else:
                        type = "norms"
                    if current and type:
                        add_row(result, type, current)
                    current = {"id": int(m.group(2)), "body": "", "doc": filename, "title": title_text}
            else:
                if current:
                    current["body"] = current["body"] + " " + n.text_content()
        if current and type:
            add_row(result, type, current)


with open(join(pathroot, "../../constitutions", 'index.json'), 'w') as fp:
    json.dump(result, fp, indent=4,)