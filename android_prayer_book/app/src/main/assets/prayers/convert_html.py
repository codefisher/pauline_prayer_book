# -*- coding: utf-8 -*-

from slugify import slugify
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
    def format_ebook(node):
        return None
else:
    def format_print(node):
        return None
    def format_ebook(node):
        root = Element("div")
        for n in node:
            root.append(n)
        return root

Library.tag("//print", format_print)
Library.tag("//ebook", format_ebook)

def from_string(text):
    try:
        return html.fragment_fromstring(text)
    except:
        return html.fragment_fromstring(text, create_parent='div')

def format_litany(node):
    root = Element("div")
    root.attrib["class"] = "litany"
    if "class" in node.attrib:
        root.attrib["class"] += " " + node.attrib.get("class")
    text = (node.text if node.text else '') + ''.join(html.tostring(n).decode() for n in node)
    for i, row in enumerate(text.strip().split("\n")):
        row_node = Element("div")
        row_node.append(from_string(row))
        row_node.attrib["class"] = "litany_item"
        root.append(row_node)
        if (i == 0 and "responce" in node.attrib) or "all" in node.attrib:
            res_node = Element("div")
            res_node.text = node.attrib.get("responce", "")
            row_node.attrib["class"] = "litany_first litany_item"
            res_node.attrib["class"] = "litany_responce"
            root.append(res_node)
    return root

Library.tag("//litany", format_litany)

def format_contents(node):
    root = Element("ul")
    root.attrib["class"] = "table-of-contents"
    headings = node.xpath("//h2")
    for heading in headings:
        li = Element("li")
        link = Element("a")
        title = heading.text_content()
        link.text = title
        if "id" in heading.attrib:
            link.attrib["href"] = "#" + heading.attrib.get('id')
        else:
            heading_id = slugify(title)
            heading.attrib["id"] = heading_id
            link.attrib["href"] = "#" + heading_id
        li.append(link)
        root.append(li)
    return root

Library.tag("//contents", format_contents)

def format_psalm(node):
    root = Element("div")
    root.attrib["class"] = "psalm"
    text = (node.text if node.text else '') + ''.join(html.tostring(n).decode() for n in node)
    for stanza in text.strip().split("\n\n"):
        stanza_node = Element("div")
        stanza_node.attrib["class"] = "stanza"
        for line in stanza.strip().split("\n"):
            line = line.strip()
            line_node = Element("div")
            line_node.attrib["class"] = "psalm-line"
            text = line
            text = text.lstrip("-")
            text = text.replace("†", """<span class="psalm-marker">&#x2020;</span>""")
            text = text.replace("+", """<span class="psalm-marker">&#x2020;</span>""")
            text = text.replace("*", """<span class="psalm-marker">*</span>""")
            for i in line:
                if i == '-':
                    text = """<div class="indent-psalm-line">{}</div>""".format(text)
                else:
                    break
            line_node.append(from_string(text))
            stanza_node.append(line_node)
        root.append(stanza_node)
    return root

Library.tag("//psalm", format_psalm)

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
        text = text.replace("...", "&hellip;")
        text = re.sub("-(\n|\r)\s*", "", text) # copying from PDF gives words broken by -
        try:
            doc = extended_html(text)
        except Exception as e:
            print(filename)
            raise  e
        for node in doc.xpath("//div[contains(@class, 'prayer-group')]"):
            if len(re.sub("\s+", "", node.text_content())) < 150:
                node.classes.add("short-prayer")
        for node in doc.xpath("//div[contains(@class, 'prayer')]"):
            if len(re.sub("\s+", "", node.text_content())) < 100:
                node.classes.add("short-prayer")
    doc.write(os.path.join(path_output, filename))
