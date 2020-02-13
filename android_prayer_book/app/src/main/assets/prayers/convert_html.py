# -*- coding: utf-8 -*-

#from slugify import slugify
from lxml import html
from os import listdir
from os.path import isfile, join, isdir
from lxml.etree import Element
import re
import codecs
import sys
import getopt
import os

opts, args = getopt.getopt(sys.argv[1:], "p",
                           ["input=", "output="])

command_opts = dict(opts)

pathroot = command_opts.get("--input", "./src/")
path_output = command_opts.get("--output", "./")

import unicodedata

def slugify(string):
    """
    Taken from the slugify package, but working with Py3
    """

    return re.sub(r'[-\s]+', '-',
                  str(re.sub(r'[^\w\s-]', '',
                             unicodedata.normalize('NFKD', string))
                          .strip()
                          .lower()))

class Library(object):
    tags = {}

    @classmethod
    def tag(cls, name=None, func=None):
        cls.tags[name] = func

def format_prayer(node, *args, **kwargs):
    text = (node.text if node.text else '') + ''.join(html.tostring(n).decode() for n in node)
    if "lines" in node.attrib:
        items = []
        for row in text.strip().split("\n"):
            if not row.strip():
                row = "&nbsp;"
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

def format_player(node, depth=1, *args, **kwargs):
    name = node.text_content()
    if "mutiple" in node.attrib:
        mutiple = ", " + node.attrib.get("mutiple")
    else:
        mutiple = ""
    depth_text = ""
    if depth == 2:
        depth_text = "../"
    return html.fromstring("""
    <div class="menu">
        <button class="play" id="{0}-play" onclick="playSong('{0}-svg', '{0}', '{2}../sound/{0}.json'{1});" >&nbsp;</button>
        <button disabled="disabled" class="stop" id="{0}-stop" onclick="stopSong('{0}-svg', '{0}');" >&nbsp;</button>
    </div>
    <div>
        <object class="img-content" id="{0}-svg" data="{2}../music/{0}.svg" type="image/svg+xml">&nbsp;</object>
    </div>
    """.format(name, mutiple, depth_text))

Library.tag("//player", format_player)

# such a tag might seem useless, but it was needed for
# the script that converted the html to tex
def format_music(node, *args, **kwargs):
    name = node.text_content()
    return html.fromstring("""
    <img class="img-content" src="../music/{}.svg" />
    """.format(name))

Library.tag("//music", format_music)
Library.tag("//gregorian", format_music)

def format_head(node, path='', *args, **kwargs):
    if isfile(os.path.join(path, '../../../style.css')):
        code_nodes = html.fragments_fromstring("""
        <meta http-equiv="content-type" content="text/html; charset=UTF-8">
        <link href="../../style.css" rel="stylesheet">
        """)
    else:
        code_nodes = html.fragments_fromstring("""
        <meta http-equiv="content-type" content="text/html; charset=UTF-8">
        <link href="../style.css" rel="stylesheet">
        """)
    for code_node in code_nodes:
        node.append(code_node)
    return node

Library.tag("//head", format_head)

if "-p" in command_opts:
    def format_print(node, *args, **kwargs):
        root = Element("div")
        for n in node:
            root.append(n)
        return root
    def format_ebook(node, *args, **kwargs):
        return None
else:
    def format_print(node, *args, **kwargs):
        return None
    def format_ebook(node, *args, **kwargs):
        root = Element("div")
        root.attrib["class"] = "ebook"
        for n in node:
            root.append(n)
        return root

Library.tag("//print", format_print)
Library.tag("//ebook", format_ebook)

Library.tag("//break", lambda x, *args, **kwargs: None)


def from_string(text):
    try:
        return html.fragment_fromstring(text)
    except:
        return html.fragment_fromstring(text, create_parent='div')

def format_litany(node, *args, **kwargs):
    root = Element("div")
    root.attrib["class"] = "litany"
    if "class" in node.attrib:
        root.attrib["class"] += " " + node.attrib.get("class")
    text = (node.text if node.text else '') + ''.join(html.tostring(n).decode() for n in node)
    text = re.sub("\n\s+\n", "\n\n", text)
    if "includeblank" in node.attrib:
        for row in text.strip().split("\n\n"):
            root.append(litany_helper(row, node))
    else:
         litany_helper(text, node, root)
    return root

def litany_helper(text, node, root=None):
    if root is None:
        root = Element("div")
        root.attrib["class"] = "litany"
    for i, row in enumerate(text.strip().split("\n")):
        if row.strip() == "":
            continue
        row_node = Element("div")
        row_node.attrib["class"] = "litany_item"
        if row.strip().startswith('-'):
            row_node.attrib["class"] = "litany_item indent-psalm-line"
            row = row.strip().lstrip("-")
        row_node.append(from_string(row))
        root.append(row_node)
        if (i == 0 and "responce" in node.attrib) or "all" in node.attrib:
            res_node = Element("div")
            res_node.text = node.attrib.get("responce", "")
            row_node.attrib["class"] = "litany_first litany_item"
            res_node.attrib["class"] = "litany_responce"
            root.append(res_node)
    return root

Library.tag("//litany", format_litany)

def format_contents(node, *args, **kwargs):
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

def format_psalm(node, *args, **kwargs):
    root = Element("div")
    root.attrib["class"] = "psalm"
    text = (node.text if node.text else '') + ''.join(html.tostring(n).decode() for n in node)
    if "red" in node.attrib:
        red_node = Element("div")
        red_node.attrib["class"] = "psalm-red"
        red_node.append(from_string(node.attrib.get("red")))
        root.append(red_node)
    text = re.sub(r"\n[ \t]*\n", "\n\n", text)
    for stanza in text.strip().split("\n\n"):
        stanza_node = Element("div")
        stanza_node.attrib["class"] = "stanza"
        for line in stanza.strip().split("\n"):
            line = line.strip()
            line_node = Element("div")
            line_node.attrib["class"] = "psalm-line"
            text = line
            text = text.lstrip("-")
            text = re.sub("\s*\*", """<span class="psalm-marker">&nbsp;*</span>""", text)
            text = re.sub("\s*(\+|†)", """<span class="psalm-marker">&nbsp;&#x2020;</span>""", text)
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

def format_sp(node, *args, **kwargs):
    tail = node.tail if node.tail else ''
    if node.text == 'R/':
        return from_string('<span><span class="rubric">R.</span>' + tail + '</span>')
    if node.text == 'V/':
        return from_string('<span><span class="rubric">V.</span>' + tail + '</span>')
    if node.text == '+':
        return from_string('<span><span class="rubric">&dagger;</span>' + tail + '</span>')

Library.tag("//sp", format_sp)

def format_reading(node, *args, **kwargs):
    root = Element("div")
    if not node.text:
        if "ref" in node.attrib:
            root.append(from_string("<div class='ref'>{}</div>".format(node.attrib.get("ref"))))
    if "label" in node.attrib:
        root.append(from_string("<div class='reading'>{}</div>".format(node.attrib.get("label"))))
    if node.text:
        if "ref" in node.attrib:
            root.append(from_string("<div class='ref'>{}</div>".format(node.attrib.get("ref"))))
        root.append(from_string("<div>{}</div>".format(node.text)))
    for n in node:
        root.append(n)
    if "shorttag" in node.attrib:
        root.append(from_string("<div class='rubric'>{}</div>".format(node.attrib.get("shorttag"))))
    if "longref" in node.attrib:
        root.append(from_string("<div class='rubric' style='text-align:center'>{}</div>".format(node.attrib.get("longref"))))
    if "tagline" in node.attrib:
        root.append(from_string("<div class='rubric' style='text-align:center; font-size:0.8em;'><em>{}</em></div>".format(node.attrib.get("tagline"))))
    return root

Library.tag("//reading", format_reading)

def extended_html(text, *args, **kwargs):
    nodes = html.fromstring(text)
    for name, func in Library.tags.items():
        for n in nodes.xpath(name):
            new = func(n, *args, **kwargs)
            if new is not None:
                n.getparent().replace(n, new)
            else:
                n.getparent().remove(n)
    return nodes.getroottree()

def update_files(pathroot, path_output, depth=1):
    for folder in (f for f in listdir(pathroot) if isdir(join(pathroot, f))):
        update_files(os.path.join(pathroot, folder), os.path.join(path_output, folder), depth=2)
    for filename in (f for f in listdir(pathroot) if isfile(join(pathroot, f))):
        if filename == "empty.html" or filename.startswith('.') or not filename.endswith('.html'):
            continue
        with codecs.open(join(pathroot, filename), "r", encoding='utf8') as fp:
            try:
                text = fp.read()
                text = text.replace("ę", "&#x119;").replace("Ȩ", "&#x228;") # does not display otherwise
                text = text.replace("...", "&hellip;")
                text = re.sub("(-|­)(\n|\r)\s*", "", text) # copying from PDF gives words broken by - or the invisible version
            except UnicodeDecodeError as e:
                print("Can't read: {}".format(filename))
                exit()
            try:
                doc = extended_html(text, path=pathroot, filename=filename, depth=depth)
            except Exception as e:
                print(filename)
                raise  e
            for node in doc.xpath("//div[contains(@class, 'prayer-group')]"):
                if len(re.sub("\s+", "", node.text_content())) < 150:
                    node.classes.add("short-prayer")
            for node in doc.xpath("//div[contains(@class, 'prayer')]"):
                if len(re.sub("\s+", "", node.text_content())) < 100:
                    node.classes.add("short-prayer")
        try:
            doc.write(os.path.join(path_output, filename))
        except FileNotFoundError as e:
            print(os.path.join(path_output, filename))
            raise e

update_files(pathroot, path_output)