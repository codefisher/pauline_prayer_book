import re
import os
import codecs
from lxml import etree, html
import sys

index_file, HTML, output = sys.argv[1:]

title_clean = re.compile("^[0-9]+\.[0-9\.]*|[A-E]\.")
white_space = re.compile("\s+")

missing_format = set()
missing_tags = set()
div_class = set()

last_was_space = False
last_was_header = False

def write_fp(fp, text):
    global last_was_space
    global last_was_header
    fp.write(text)
    last_was_space = False
    last_was_header = False

def write_header(fp, text):
    global last_was_space
    global last_was_header
    fp.write(text)
    last_was_space = False
    last_was_header = True

def write_space(fp):
    global last_was_space
    if not last_was_space:
        if last_was_header:
            pass#fp.write("\\smallskip\n")
        else:
            fp.write("\\smallbreak\n")
    last_was_space = True

def title(text):
    return special_chars(title_clean.sub("", text).strip())

def no_white(text):
    if not text:
        return ''
    return white_space.sub(" ", text).strip()

def special_chars(text):
    return text.replace("…", r"\ldots ").replace('†', r'\GreDagger').replace('—', '---').replace('–', '--').replace('“', '``').replace('”', "''").replace('’', "'").replace('‘', "`")
    
def format_help(node):
    result = [node.text]
    for n in node.getchildren():
        result.append(simple_format(n, True))
    return "".join(filter(None, result))

def simple_format(node, white=False):
    result = []
    if node.tag == "sup":
        result.append(r"\textsuperscript{%s}" % format_help(node))
    elif node.tag == "strong":
        result.append(r"\textbf{%s}" % format_help(node))
    elif node.tag == "em":
        result.append(r"\textit{%s}" % format_help(node))
    elif node.tag == "u":
        result.append(r"\underline{%s}" % format_help(node))
    elif node.tag == "span":
        if node.attrib.get("class") in ["cross", "rubric"]:
            result.append(r"\red{%s}" % format_help(node))
        elif node.attrib.get('class') == 'ref':
            result.append("\n\\reference{%s}\n" % format_help(node))
        else:
            if node.attrib.get("class"):
                missing_format.add("%s.%s" % (node.tag, node.attrib.get("class")))
            result.append(format_help(node))
    elif node.tag == "blockquote":
        result.append(r'\begin{addmargin}[\parindent]{\parindent}')
        result.append(format_help(node))
    elif node.tag == "br":
        result.append(r"\\")
    elif node.tag == 'hr':
        result.append(r"\hrulefill")
    elif node.tag == "ul":
        result.append("\\begin{itemize}\n" + format_help(node))
    elif node.tag == "li":
        result.append("\\item %s\n" % format_help(node))
    elif node.tag in ['player', 'gregorian']:
        result.append(include_tex("music/%s.tex" % node.text))
    elif node.tag == 'music':
        result.append(include_music("music/lilypond/%s.tex" % node.text))
    else:
        missing_format.add(node.tag)
        result.append(format_help(node))
    result.append(node.tail)
    if node.tag == "ul":
        result.append(r"\end{itemize}")
    elif node.tag == "blockquote":
        result.append(r"\end{addmargin}")
    text = special_chars("".join(filter(None, result)))
    if white:
        return text 
    else:
        return no_white(text)

def heading_help(node, heading, index):
    global appendix
    extra = ""
    if index:
        extra = "\n\\addcontentsline{toc}{%s}{%s}" % (heading[:-1], title(node.text))
    result = ""
    if not len(node) or not node[0].text:
        result = (r"""
\%s{%s}""" % (heading, title(simple_format(node))))
    else:
        main_title = title(no_white(node.text)).strip()
        subtitle = no_white(simple_format(node[0]))
        if heading[-1] != "*":
            result = (r"""
\%s[%s]{%s \\ {\small\normalfont %s}}
""" % (heading, main_title, main_title, subtitle))
        else:
            result = (r"""
\%s{%s \\ {\small\normalfont %s}}
""" % (heading, main_title, subtitle))
    return "\n%s%s\n\n" % (result, extra)

def heading(node):
    prefex = ''
    if not title_clean.match(node.text):
        prefex = '*'
    index = node.attrib.get("class") == "index"
    if node.tag == 'h1':
        if node.attrib.get('class') == 'section':
            return heading_help(node, 'chapter' + prefex, index)
        else:
            return heading_help(node, 'section' + prefex, index)
    elif node.tag == 'h2':
        return heading_help(node, 'subsection' + prefex, index)
    elif node.tag == 'h3':
        return heading_help(node, 'subsubsection' + prefex, index)
    elif node.tag == 'h4':
        return heading_help(node, 'paragraph' + prefex, index)
    elif node.tag == 'h5':
        return heading_help(node, 'subparagraph' + prefex, index)

prayer_prefix = {
    "V.": "\Vbar.",
    "R.": "\Rbar.",
}

def prayer(node):
    text = simple_format(node, True).strip()
    if node.attrib.get('lines'):
        text = text.replace("\n", r"\par ")
    text = no_white(text).strip()
    if "leader" in node.attrib.get('class', ''):
        text = r"\textbf{%s}" % text
    red = node.attrib.get('red', '')
    red = prayer_prefix.get(red, red)
    text = r"\prayer{%s}{%s}" % (red, text)
    if node.attrib.get('lines'):
        return (r"\begin{litany}%s\end{litany}" % text) + "\n"
    if node.attrib.get('class') == 'leader' and last_was_space == False:
        return "\\smallbreak\n" + text + "\n"
    else:
        return text + "\n"

def litany(node):
    text = simple_format(node, True).strip()
    result = []
    for i, row in enumerate(text.strip().split("\n")):
        if (i == 0 and "responce" in node.attrib) or "all" in node.attrib:
            result.append(r"%s \responce{%s}\par " % (row, node.attrib.get("responce", "").strip()))
        else:
            result.append(r"%s \par" % row.strip())
    return "\\begin{litany}%s\n\\end{litany}\n" % "\n".join(result)

def psalm(node):
    text = simple_format(node, True).strip()
    result = []
    for stanza in text.strip().split("\n\n"):
        for line in stanza.strip().split("\n"):
            line = line.strip().replace('\GreDagger', r'\red{\GreDagger}').replace('†', r'\red{\GreDagger}').replace('+', r'\red{\GreDagger}').replace('*', r'\red{*}')
            indent = 0
            for i in line:
                if i == '-':
                    indent += 1
                else:
                    break
            if indent:
                line = r"\hspace{%sem}" % (indent) + line.lstrip("-")
            result.append(line + r"\par")
        result.append(r'\medbreak')
    return "\\begin{litany}%s\n\\end{litany}\n" % "\n".join(result)

def table(node):
    rows = []
    length = 0
    for row in node:
        cell_text = []
        if len(row) > length:
            length = len(row)
        for i, cell in enumerate(row):
            cell_text.append(simple_format(cell))
        rows.append(" & ".join(cell_text))
    cols = " c " * length
    return r"""
\begin{tabular}{ %s }
%s
\end{tabular}""" % ("p{5em} p{20em}", "\\\\\n".join(rows))

def include_tex(name):
    with open(name, "r") as fp:
        text = fp.read()
        result = []
        for line in text.split('\n'):
            if line and not (line[0] == '%' or '{document}' in line or '{minipage}' in line or r'\documentclass' in line or r'\RequirePackage' in line or r'\usepackage' in line or r'\input' in line):
                result.append(line.replace(r'\gregorioscore{', r'\gregorioscore{music/'))
        return "\n".join(result)

def include_music(name):
    result = []
    with open(name, "r") as fp:
        text = fp.read()
        filename = re.search(r"\\input\{(.+)\}", text).group(1)
        with open(os.path.join('modern/lilypond/', filename), "r") as fp_tex:
            tex = fp_tex.read()
            for graphic in re.findall(r"\\includegraphics\{(.+)\}", tex):
                result.append(r"\noindent\includegraphics[width=\textwidth,height=\textheight,keepaspectratio]{modern/lilypond/%s}" % graphic)
    return "\n\\begin{center}\n" + "\n".join(result) + "\n\\end{center}\n"

def write_tex(nodes, fp):
    for node in nodes:
        if "necrology" in node.attrib.get('id', ''):
            continue
        if node.tag in ["h1", "h2", "h3", "h4", "h5"]:
            write_header(fp, heading(node))
        elif node.tag == 'p':
            if node.attrib.get('class') == 'instruction':
                write_space(fp)
                write_fp(fp, "\n\\instruction{%s}\n" % simple_format(node).strip())
            elif node.attrib.get('class') == 'ref':
                write_fp(fp, "\\nopagebreak\\reference{%s}\n" % simple_format(node).strip())
            elif node.attrib.get('class') == 'indented-prayer':
                write_space(fp)
                write_fp(fp, "\n\\begin{addmargin}[6em]{0em}\\noindent%s\\end{addmargin}\n" % simple_format(node).strip())
            else:
                if node.attrib.get('class'):
                    missing_tags.add("%s.%s" % (node.tag, node.attrib.get('class')))
                write_space(fp)
                write_fp(fp, "\n%s\n" % simple_format(node).strip())
            write_space(fp)
        elif node.tag == 'div':
            class_name = node.attrib.get('class', '')
            if 'prayer-group' in class_name:
                write_space(fp)
                if 'congregation' in class_name:
                    write_fp(fp, r'\begin{minipage}{\textwidth}\begin{addmargin}[2in]{0em}' + "\n")
                    write_tex(node, fp)
                    write_fp(fp, r'\end{addmargin}\end{minipage}' + "\n \\par")
                elif 'fathers' in class_name and not 'hymn-first' in class_name:
                    write_fp(fp, r'\begin{minipage}{\textwidth}' + "\n")
                    write_tex(node, fp)
                    write_fp(fp, r'\end{minipage}' + "\n \\par")
                else:
                    write_tex(node, fp)
                write_space(fp)
            elif node.attrib.get('class') in ['rubric']:
                write_fp(fp, "\n\\red{%s} \n" % simple_format(node))
            else:
                div_class.add(node.attrib.get('class', ''))
                write_tex(node, fp)
        elif node.tag in ['ul', 'blockquote']:
            write_fp(fp, simple_format(node))
        elif node.tag == 'prayer':
            write_fp(fp, prayer(node))
        elif node.tag in ['player', 'gregorian']:
            write_fp(fp, include_tex("music/%s.tex" % node.text))
        elif node.tag == 'music':
            write_fp(fp, include_music("modern/lilypond/%s.tex" % node.text))
        elif node.tag == 'litany':
            write_fp(fp, litany(node))
        elif node.tag == 'psalm':
            write_fp(fp, psalm(node))
        elif node.tag == 'table':
            write_fp(fp, table(node))
        elif node.tag == "br":
            write_fp(fp, r" \\ ")
        elif node.tag == 'hr':
            write_fp(fp, r"\par \hrulefill")
            write_space(fp)
        else:
            missing_tags.add(node.tag)

def parse_html(doc, fp):
    with codecs.open(os.path.join(HTML, doc), "r", encoding='utf8') as h_fp:
        text = h_fp.read()
        text = re.sub("-(\n|\r)\s*", "", text) # copying from PDF gives words broken by -
        nodes = html.fromstring(text)
        print(doc)
        for body in nodes.xpath("//body"):
            write_tex(body, fp)

def index(nodes, fp):
    global appendix
    for node in nodes:
        if node.tag == 'chapter':
            index(node, fp)
        elif node.tag == 'section':
            write_fp(fp, r'\newpageheader{%s}{%s}' % (special_chars(node.getparent().attrib.get('title')), special_chars(node.attrib.get('title'))))
            parse_html(node.attrib.get("doc"), fp)
            if not node.attrib.get('nobreak'):
                write_fp(fp, "\\newpage\n")
        elif node.tag == 'appendix':
            write_fp(fp, """\\begin{appendices}\n""")
            index(node, fp)
            write_fp(fp, "\\end{appendices}\n")
        elif node.tag == 'insert':
            write_fp(fp, r'\includeimage{%s}' % node.attrib.get('file'))
        elif node.tag == 'include':
            write_fp(fp, r'\input{%s}' % node.attrib.get('file'))
with codecs.open(output, "w", encoding='utf8') as fp:
    write_fp(fp, r"""% !TEX program = LuaLaTeX+se
\begin{document}
""")

    tree = etree.parse(index_file)
    for node in tree.xpath("//index"):
        index(node, fp)

    write_fp(fp, r"""
\pagestyle{empty}

\tableofcontents

\newpage\null\thispagestyle{empty}\newpage

\end{document}""")

# read and write the file again so we can do extra processing
with codecs.open(output, "r", encoding='utf8') as fp:
    text = fp.read()
    text = re.sub('\n\n\n+', '\n\n', text)
with codecs.open(output, "w", encoding='utf8') as fp:
    fp.write(text)

print(missing_format)
print(missing_tags)
print(div_class)
