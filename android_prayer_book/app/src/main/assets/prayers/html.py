# -*- coding: utf-8 -*-

from lxml import html
from os import listdir
from os.path import isfile, join
from lxml.etree import Element
import re
import codecs
import sys
import getopt
import os

opts, args = getopt.getopt(sys.argv[1:], "p",
                           ["input=", "output="])

command_opts = dict(opts)

class Library(object):
    tags = {}

    @classmethod
    def tag(cls, name=None, func=None):
        cls.tags[name] = func

def format_prayer(node):
    text = (node.text if node.text else '') + ''.join(html.tostring(n).decode() for n in node)
    if "lines" in node.attrib:
        items = []
        for row in text.strip().split("\n"):
            items.append("""<div class="prayer-line">{}</div>""".format(row))
        text = "".join(items)
    if "red" in node.attrib:
        result = html.fromstring("""<div><div class="prayer-red">{}</div>{}</div>""".format(node.attrib.get("red", ""), text))
    else:
        result = html.fromstring("""<div>{}</div>""".format(text))
    if node.attrib.get("class"):
        result.attrib["class"] = node.attrib.get("class") + " prayer"
    else:
        result.attrib["class"] = "prayer"
    return result

Library.tag("//prayer", format_prayer)

def format_head(node):
    code_nodes = html.fragments_fromstring("""
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <link href="../style.css" rel="stylesheet">
    """)
    for code_node in code_nodes:
        node.append(code_node)
    return node

Library.tag("//head", format_head)

if "-p" in command_opts:
    def format_print(node):
        root = Element("div")
        for n in node:
            root.append(n)
        return root
else:
    def format_print(node):
        return None
Library.tag("//print", format_print)

def format_litany(node):
    root = Element("div")
    root.attrib["class"] = "litany"
    for i, row in enumerate(node.text.strip().split("\n")):
        row_node = Element("div")
        row_node.text = row
        row_node.attrib["class"] = "litany_item"
        root.append(row_node)
        if i == 0:
            res_node = Element("div")
            res_node.text = node.attrib.get("responce", "")
            row_node.attrib["class"] = "litany_first litany_item"
            res_node.attrib["class"] = "litany_responce"
            root.append(res_node)
    return root

Library.tag("//litany", format_litany)

def extended_html(text, *args, **kwargs):
    nodes = html.fromstring(text)
    for name, func in Library.tags.items():
        for n in nodes.xpath(name):
            new = func(n)
            if new is not None:
                n.getparent().replace(n, new)
            else:
                n.getparent().remove(n)
    return nodes.getroottree()


pathroot = command_opts.get("--input", "./src/")
path_output = command_opts.get("--output", "./")

for filename in (f for f in listdir(pathroot) if isfile(join(pathroot, f))):
    if filename == "empty.html":
        continue
    with codecs.open(join(pathroot, filename), "r", encoding='utf8') as fp:
        text = fp.read()
        text = text.replace("ę", "&#x119;").replace("Ȩ", "&#x228;") # does not display otherwise
        text = re.sub("-(\n|\r)\s*", "", text) # copying from PDF gives words broken by -
        try:
            doc = extended_html(text)
        except Exception as e:
            print(filename)
            raise  e
    doc.write(os.path.join(path_output, filename))
