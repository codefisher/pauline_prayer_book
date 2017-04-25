# -*- coding: utf-8 -*-

import html5lib
from lxml import html
from html5lib import sanitizer
from os import listdir
from os.path import isfile, join
from lxml.etree import Element
import re
import codecs

class Library(object):
    tags = {}

    @classmethod
    def tag(cls, name=None, func=None):
        cls.tags[name] = func

"""
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import HtmlFormatter

    def format_code(node):
        if not node.attrib.get('codelang'):
            return None
        lexer = get_lexer_by_name(node.attrib.get('codelang'), stripall=True)
        formatter = HtmlFormatter(linenos=True)
        code = node.text + ''.join(html.tostring(n) for n in node)
        result = highlight(code, lexer, formatter)
        code_node = html.fromstring(result)
        return code_node

    Library.tag("//code", format_code)
except ImportError:
    pass
"""

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
    return nodes.getroottree()


pathroot = "src"
for filename in (f for f in listdir(pathroot) if isfile(join(pathroot, f))):
    with codecs.open(join(pathroot, filename), "r", encoding='utf8') as fp:
        text = fp.read()
        text = text.replace("ę", "&#x119;").replace("Ȩ", "&#x228;") # does not display otherwise
        text = re.sub("-(\n|\r)\s*", "", text) # copying from PDF gives words broken by -
        try:
            doc = extended_html(text)
        except Exception as e:
            print(filename)
            raise  e
    doc.write(filename)
