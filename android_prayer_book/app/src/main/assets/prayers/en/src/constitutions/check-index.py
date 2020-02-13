
from lxml import html
from os import listdir
from os.path import isfile, join, isdir
import codecs
import argparse
import re

parser = argparse.ArgumentParser()

parser.add_argument('html_file', type=str)
args = parser.parse_args()

if args.html_file is not None:
    html_file = args.html_file
else:
    exit()

pathroot = "./"

index_proper = []
index_other = []

def clean_list(items):
    for i, item in enumerate(items):
        items[i] = re.sub("\s+", " ", item).strip().lower()

for filename in (f for f in listdir(pathroot) if isfile(join(pathroot, f))):
    if filename.startswith('.') or not filename.endswith('.html'):
        continue
    with codecs.open(join(pathroot, filename), "r", encoding='utf8') as fp:
        text = fp.read()
        nodes = html.fromstring(text)
        for n in nodes.xpath("//span[@index]"):
            index_proper.append(n.attrib.get("index"))
            index_other.append(n.text)

clean_list(index_proper)
clean_list(index_other)

index_words = set(index_proper)
index_words.update(set(index_other))

with open(html_file, 'r') as fp:
    text = fp.read()
nodes = html.fromstring(text)
for n in nodes.xpath("//span[@index]"):
    n.getparent().remove(n)

words = re.sub("\s+", " ", nodes.text_content()).strip().lower()

for i in index_words:
    if re.search(r"\b%s\b" % i, words):
        print(i)
        for j in re.findall(r'.{0,50}\b%s\b.{0,50}' % i, words):
            print("\t" + j)
