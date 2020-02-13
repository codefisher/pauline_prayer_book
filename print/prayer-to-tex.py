import re
import os
import codecs
from lxml import etree, html
import sys

import argparse
parser = argparse.ArgumentParser()

parser.add_argument('--nomusic', action='store_true')
parser.add_argument('--noimages', action='store_true')
parser.add_argument('arg1', type=str)
parser.add_argument('arg2', type=str)
parser.add_argument('arg3', type=str, nargs='?')

args = parser.parse_args()

NO_MUSIC = args.nomusic
NO_IMAGES = args.noimages

if args.arg3 is not None:
    index_file = args.arg1
    HTML = args.arg2
    output = args.arg3
elif len(sys.argv) == 3:
    index_file = None
    HTML = args.arg1
    output = args.arg2
else:
    exit()
    

title_clean = re.compile("^[0-9]+\.[0-9\.]*|[A-E]\.")
white_space = re.compile("\s+")
number_start = re.compile("^[0-9]+\.")

missing_format = set()
missing_tags = set()
div_class = set()

last_was_space = False
last_was_header = False
headerdepth = "section"
use_drop_cap = None
in_appendix = False

def write_fp(fp, text, no_change=False):
    global last_was_space
    global last_was_header
    fp.write(text)
    if not no_change:
        last_was_space = False
        last_was_header = False

def write_header(fp, text):
    global last_was_space
    global last_was_header
    if last_was_space:
        fp.seek(-len("\\normalbreak\n"), os.SEEK_CUR)
    fp.write(text)
    last_was_space = False
    last_was_header = True

def write_space(fp):
    global last_was_space
    if not last_was_space:
        if last_was_header:
            pass#fp.write("\\smallskip\n")
        else:
            fp.write("\\normalbreak\n")
    last_was_space = True

def title(text):
    return title_clean.sub("", text).strip()

def no_white(text):
    if not text:
        return ''
    return white_space.sub(" ", text).strip()

def special_chars(text):
    if not text:
        return ""
    return (text.replace("_", r"\_ ").replace("~", r"\textasciitilde ").replace("\\", r"\textbackslash ").replace("^", r"\textasciicircum ")
            .replace("… ", r"\ldots ~").replace("\u00A0", "~").replace("…", r"\ldots ").replace("$", r"\$ ")
            .replace("&", r"\& ").replace("%", r"\% ").replace("#", r"\# ").replace("_", r"\_ ")
            .replace('†', r'\GreDagger').replace('—', '---').replace('–', '--').replace('“', '``').replace("¶", r"\P ")
            .replace('”', "''").replace('’', "'").replace('‘', "`").replace("☩", r"\ding{64}").replace("✠", r"\ding{64}"))
    
def format_help(node, span_as_normal=False):
    global use_drop_cap
    if use_drop_cap is not None:
        text = node.text
        if text and text.strip():
            word, _, sentance = text.lstrip().partition(' ')
            sentance = special_chars(sentance)
            word_first, word_remainder = special_chars(word[0]), special_chars(word[1:])
            if use_drop_cap == 'special':
                text = r"\illuminatedcap{%s}{%s} %s" % (word_first, word_remainder, sentance)
            elif use_drop_cap == 'special4':
                text = r"\illuminatedcap[4]{%s}{%s} %s" % (word_first, word_remainder, sentance)
            else:
                text = r"\lettrine[lines=2]{\red{%s}}{%s} %s" % (word_first, word_remainder, sentance)
            use_drop_cap = None
        result = [text]
    else:
        result = [special_chars(node.text)]
    for n in node.getchildren():
        result.append(simple_format(n, white=True, span_as_normal=span_as_normal))
    return "".join(filter(None, result))

def simple_format(node, white=False, span_as_normal=False, headings=True, paragraph=True):
    result = []
    if node.tag == "sup":
        result.append(r"\textsuperscript{%s}" % format_help(node))
    elif node.tag == "sp":
        if node.text == "R/":
            result.append(r"\cross{\Rbar.}")
        if node.text == "V/":
            result.append(r"\cross{\Vbar.}")
        if node.text == "+":
            result.append(r"\red{\GreDagger}")
    elif node.tag == "break":
        result.append(r" \newpage ")
    elif node.tag == "strong":
        result.append(r"\textbf{%s}" % format_help(node))
    elif node.tag == "em":
        result.append(r"\textit{%s}" % format_help(node))
    elif paragraph and node.tag == "p":
        result.append(r"%s\par " % format_help(node))
    elif headings and node.tag in ["h1", "h2", "h3", "h4", "h5"]:
        result.append(r"\textbf{%s}\par " % format_help(node))
    elif node.tag == "u":
        result.append(r"\underline{%s}" % format_help(node))
    elif node.tag == "span":
        class_name = node.attrib.get("class", "").split()
        if "rubric" in class_name:
            span = r"\rubric{%s}" % format_help(node)
        elif "cross" in class_name:
            span = r"\cross{%s}" % format_help(node)
        elif "upper" in class_name:
            span = r"~\textsc{%s}" % format_help(node, span_as_normal=span_as_normal)
            span_as_normal = False
        elif "ref" in class_name:
            span = "\n\\reference{%s}\n" % format_help(node)
        elif 'right' in class_name:
            span = r"\hfill" + format_help(node)
        else:
            if node.attrib.get("class"):
                missing_format.add("%s.%s" % (node.tag, node.attrib.get("class")))
            span = format_help(node)
        if "small" in class_name:
            span = "{\small %s}" % span
        elif "large" in class_name:
            span = "{\large %s}" % span
        if span_as_normal:
            result.append(r"\hspan{%s}" % span)
        else:
            result.append(span)
        if "index" in node.attrib:
            result.append(r' \index{%s} ' % node.attrib.get('index'))
    elif node.tag == "blockquote":
        result.append(r'\begin{addmargin}[\parindent]{\parindent}')
        result.append(format_help(node))
    elif node.tag == "br":
        result.append(r"\\")
    elif node.tag == 'hr':
        if node.attrib.get("class") == "rubric":
            result.append(r"{\color{red}\hrulefill}")
        else:
            result.append(r"\hrulefill")
    elif node.tag == "ul":
        result.append("\\begin{itemize}\n" + format_help(node))
    elif node.tag == "ol":
        if node.attrib.get("class") == 'alph':
            result.append("\\begin{enumerate}[label=\\alph*)]\n" + format_help(node))
        elif node.attrib.get("class") == 'Alph':
            result.append("\\begin{enumerate}[label=\\Alph*.]\n" + format_help(node))
        elif node.attrib.get("class") == 'arabic':
            result.append("\\begin{enumerate}[label=\\arabic*)]\n" + format_help(node))
        elif node.attrib.get("class") == 'arabic-degree':
            result.append("\\begin{enumerate}[label=\\arabic*°]\n" + format_help(node))
        else:
            result.append("\\begin{enumerate}\n" + format_help(node))
    elif node.tag == "li":
        result.append("\\item %s\n" % format_help(node))
    elif node.tag in ['player', 'gregorian']:
        result.append(include_tex("music/%s.tex" % node.text))
    elif node.tag == 'music':
        result.append(include_music("music/lilypond/%s.tex" % node.text))
    elif node.tag == 'footnote':
        result.append(r"\footnote{%s}" % format_help(node))
    else:
        missing_format.add(node.tag)
        result.append(format_help(node, span_as_normal=span_as_normal))
    if node.tag == "a" and "#" in node.attrib.get("href", ""):
        result.append(' p.~\pageref{%s}' % re.sub('[^a-zA-Z]', '', node.attrib.get("href")))
    result.append(special_chars(node.tail))
    if node.tag == "ul":
        result.append(r"\end{itemize}")
    elif node.tag == "ol":
            result.append(r"\end{enumerate}")
    elif node.tag == "blockquote":
        result.append(r"\end{addmargin}")
    text = "".join(filter(None, result))
    if white:
        return text
    else:
        return no_white(text)

def heading_help(node, heading, index):
    global appendix
    extra = ""
    before = ""
    main_title = special_chars(title(no_white(node.text_content())).strip())
    if index:
        if index is True:
            extra += "\n\\addcontentsline{toc}{%s}{%s}" % (heading[:-1], main_title)
        else:
            extra += "\n\\addcontentsline{toc}{%s}{%s}" % (index, main_title)
    if heading.startswith("chapter"):
        extra += r"\enlargethispage{-2\baselineskip}"
    result = ""
    if not len(node) or not node[0].text:
        result = (r"""
\%s{%s}""" % (heading, title(simple_format(node, headings=False))))
    else:
        full_title = title(simple_format(node, span_as_normal=True, headings=False))#.lstrip(r"\\ ")
        #print(full_title)
        if heading[-1] != "*":
            result = (r"""
\%s[%s]{%s}
""" % (heading, main_title, full_title))
        else:
            result = (r"""
\%s{%s}
""" % (heading, full_title))
    #if heading == "subsection":
    #    result = "\\needspace{8\\baselineskip}" + result
    #elif heading == "subsubsection":
    #    result = "\\needspace{4\\baselineskip}" + result
    return "\n%s%s%s\n\n" % (before, result, extra)

def heading(node, doc):
    prefex = ''
    if not node.text or not title_clean.match(node.text):
        prefex = '*'
    index = node.attrib.get("class") and ("index" in node.attrib.get("class") or "section" in node.attrib.get("class"))
    if node.attrib.get('id'):
        before = "\n\\label{%s}" % re.sub("[^a-zA-Z]", "", os.path.basename(doc) + node.attrib.get('id'))
    if node.tag == 'h1':
        if node.attrib.get("class") and 'section' in node.attrib.get('class'):
            return heading_help(node, 'chapter' + prefex, index)
        else:
            if in_appendix:
                index = "subsection"
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
    text = text.replace(r"\par \par", r"\par \normalbreak")
    red = node.attrib.get('red', '')
    red = prayer_prefix.get(red, red)
    if "leader" in node.attrib.get('class', ''):
        text = r"\textbf{%s}" % text
        #red = r"\textbf{%s}" % red
    if "indent" in node.attrib:
        text = r"\prayer[%s]{%s}{%s}" % (node.attrib.get("indent"), red, text)
    else:
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
    rows = text.strip().split("\n")
    for i, row in enumerate(rows):
        row = row.strip()
        if not row and "includeblank" in node.attrib:
            result.append(r"\normalbreak")
            continue
        if row.startswith('-'):
            row = r"\hspace{1em}" + row.lstrip("-")
        if (i == 0 and "responce" in node.attrib) or "all" in node.attrib:
            result.append(r"%s \responce{%s}\par " % (row, node.attrib.get("responce", "").strip()))
        elif "repeat" in node.attrib:
            repeat = int(node.attrib.get("repeat"))
            if i % repeat == 0 or i == len(rows) - 1:
                result.append(r"%s \responce{%s}\par " % (row, node.attrib.get("responce", "").strip()))
            else:
                result.append(r"%s \responce{''\hspace{2em}''\hspace{1em}}\par " % row)
        else:
            if node.attrib.get("class") == "strong":
                result.append(r"\textbf{%s} \par" % row.strip())
            else:
                result.append(r"%s \par" % row.strip())
    return "\\begin{litany}%s\n\\end{litany}\n" % "\n".join(result)

def psalm(node):
    text = simple_format(node, True).strip()
    extra = ""
    result = []
    numbers = "numbers" in node.attrib
    text = re.sub(r"\n[ \t]*\n", "\n\n", text)
    for i, stanza in enumerate(text.strip().split("\n\n")):
        if numbers:
            if node.attrib.get("node.attrib") == "red":
                result.append(r"\item[\red{%s.}]" % (i + 1))
            else:
                result.append(r"\item[%s.]" % (i + 1))
        for line in stanza.strip().split("\n"):
            line = line.strip()
            indent = line.count("-")
            line = re.sub(r"\s*\*", r'~\\red{*}', line)
            line = re.sub(r"\s*(\+|†|\\GreDagger)", r'~\\red{\\GreDagger}', line)
            if indent:
                line = r"\hspace{%sem}" % (indent) + line.lstrip("-")
            result.append(line + r"\par")
        result.append(r'\normalbreak')
    if "red" in node.attrib:
        extra += r"\item[\red{\textbf{%s}}]" % node.attrib.get("red")
    #if numbers or "red" in node.attrib:
    #    return "\\begin{psalm}%s%s\n\\end{psalm}\n" % (extra, "\n".join(result))
    return "\\begin{psalm}%s%s\n\\end{psalm}\n" % (extra, "\n".join(result))

def hymn(node):
    text = simple_format(node, True).strip()

    stanzas = []
    first = None
    text = re.sub(r"\n[ \t]*\n", "\n\n", text)
    for i, stanza in enumerate(text.strip().split("\n\n")):
        result = []
        stanza = stanza.strip()
        if not stanza:
            continue
        lines = stanza.strip().split("\n")
        if not "wrapok" in node.attrib:
            result.append(r"\needspace{%s\baselineskip}" % len(lines))
        for line in lines:
            line = line.strip()
            if not line:
                continue
            match = number_start.match(line)
            if match:
                result.append(r"\item[%s]" % match.group(0))
                line = number_start.sub("", line).strip()
            indent = 0
            for i in line:
                if i == '-':
                    indent += 1
                else:
                    break
            if first is None:
                first = line.strip("'").strip("`").lstrip("-").rstrip(",").rstrip(";").rstrip(".").rstrip("!").rstrip("?").rstrip(":").replace("!", '"!').strip()
                if first in ["Refrain"]:
                    first = None
            line = line.lstrip("-").strip()
            line = line[0].upper() + line[1:]
            if indent:
                line = r"\hspace{%sem}" % (indent) + line
            if line in ["Refrain"]:
                line = r"\hspace{5em}\textit{\textbf{%s}}" % line
            if line in ["Refrain:"]:
                line = r"\textit{%s}" % line
            result.append(line + r"\par")
        result.append(r'\normalbreak')
        stanzas.append("\n".join(result))
    title = node.attrib.get('title')
    author = ""
    if "author" in node.attrib:
        author = "\\medskip\\enlargethispage{\\baselineskip}\\nopagebreak\\textit{\\footnotesize{%s}}" % node.attrib.get('author')
    title_text = ""
    first_text = ""
    if "title" in node.attrib:
        title_text = """\\subsection{%s}\n\\index[hymn-title]{%s}""" % (title, title.replace("!", '"!'))
        if first:
            first_text = """\n\\index[hymn-first-line]{%s}""" % first
    if "columns" in node.attrib:
        texts = []
        length = len(stanzas) // 2
        texts.append(r"""\begin{paracol}{2}
\begin{psalm}
%s
\end{psalm}
\switchcolumn
\begin{psalm}
%s
\end{psalm}
\end{paracol}""" % ("\n".join(stanzas[0:length]), "\n".join(stanzas[length:length*2])))
        if len(stanzas) % 2:
            texts.append(r"\begin{addmargin}[\textwidth/4]{0pt}\begin{psalm}%s\end{psalm}\end{addmargin}" % stanzas[-1])
        return """%s%s\n%s\n%s\n""" % (title_text, first_text, "\n".join(texts), author)
    else:
        return """%s%s\n\\begin{psalm}%s\n\\end{psalm}\n%s\n""" % (title_text, first_text, "\n".join(stanzas), author)

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
    #cols = " c " * length
    return r"""
\noindent\begin{tabu} to \textwidth { X[-1,l] X[l]}
%s
\end{tabu}""" % "\\\\\n".join(rows)

def include_tex(name, keepwidth=False):
    script_path = os.path.dirname(os.path.realpath(__file__))
    #print("%s %s" % (name, keepwidth))
    with open(os.path.join(script_path, name), "r") as fp:
        text = fp.read()
        result = []
        for line in text.split('\n'):
            if line and not (line[0] == '%' or '{document}' in line or ('{minipage}' in line and keepwidth == False) or r'\documentclass' in line or r'\RequirePackage' in line or r'\usepackage' in line or r'\input' in line or r'\pagestyle' in line):
                result.append(line.replace(r'\gregorioscore{', r'\gregorioscore{music/'))
        return "\n".join(result)

def include_music(name):
    if NO_MUSIC:
        return "\n"
    result = []
    script_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_path, name), "r") as fp:
        text = fp.read()
        filename = re.search(r"\\input\{(.+)\}", text).group(1)
        with open(os.path.join(script_path, 'modern/lilypond/', filename), "r") as fp_tex:
            tex = fp_tex.read()
            for graphic in re.findall(r"\\includegraphics\{(.+)\}", tex):
                result.append(r"\noindent\includegraphics[width=\textwidth,height=\textheight,keepaspectratio]{modern/lilypond/%s}" % graphic)
    return "\n\\begin{center}\n" + "\n".join(result) + "\n\\end{center}\n"
    
def all_prayer(nodes):
    for node in nodes:
        if node.tag != "prayer" or len(node.text_content()) > 800:
            return False
    return True


def write_tex(nodes, fp, doc):
    for node in nodes:
        write_tex_tag(doc, fp, node)

def write_next_tex(nodes, next_nodes, first_language, next_language, fp, doc):
    write_fp(fp, "\n\\begin{paracol}{2}\n")
    for node, next_node in zip(nodes, next_nodes):
        write_tex_tag(doc, fp, node)
        write_fp(fp, "\\switchcolumn\n")
        if next_language:
            write_fp(fp, "\\selectlanguage{%s}\n" % next_language)
        write_tex_tag(doc, fp, next_node)
        if next_language:
            write_fp(fp, "\\selectlanguage{%s}\n" % first_language)
        if node != nodes[-1]:
            write_fp(fp, "\\switchcolumn*\n")
    write_fp(fp, "\n\\end{paracol}\n")

def write_tex_tag(doc, fp, node):
    global last_was_space
    global use_drop_cap

    if node.attrib.get('dropcap') in ['dropcap', 'special', 'special4']:
        use_drop_cap = node.attrib.get('dropcap')
    if node.attrib.get('id'):
        write_fp(fp, "\n\\label{%s}" % re.sub("[^a-zA-Z]", "", os.path.basename(doc) + node.attrib.get('id')))
    if "necrology" in node.attrib.get('id', ''):
        return
    if node.tag in ["h1", "h2", "h3", "h4", "h5"]:
        if node.attrib.get('class') == 'rubric':
            write_fp(fp, "\n\\titlerubric{%s}\n" % simple_format(node, headings=False).strip())
        else:
            write_header(fp, heading(node, doc))
    elif node.tag == 'p':
        if node.attrib.get('class') == 'instruction':
            write_space(fp)
            write_fp(fp, "\n\\instruction{%s}\n" % simple_format(node, paragraph=False).strip())
        elif node.attrib.get('class') == 'ref':
            write_space(fp)
            write_fp(fp,
                     "\\begin{flushright}\\red{%s}\\end{flushright}\n" % simple_format(node, paragraph=False).strip())
        elif node.attrib.get('class') == 'indented-prayer':
            write_space(fp)
            write_fp(fp, "\n\\begin{addmargin}[6em]{0em}\\noindent%s\\end{addmargin}\n" % simple_format(node,
                                                                                                        paragraph=False).strip())
        elif node.attrib.get('class') and 'rubric' in node.attrib.get('class'):
            write_space(fp)
            if "noindent" in node.attrib.get('class'):
                write_fp(fp, "\n\\noindent\\red{%s}\n" % simple_format(node, paragraph=False).strip())
            else:
                if node.attrib.get('number'):
                    write_fp(fp, "\n\\noted{%s}{\\red{%s}}\n" % (
                    node.attrib.get('number'), simple_format(node, paragraph=False).strip()))
                else:
                    write_fp(fp, "\n\\red{%s}\n" % simple_format(node, paragraph=False).strip())
        elif node.attrib.get('class') == "columned":
            write_fp(fp, r'\begin{multicols}{2}')
            write_fp(fp, "\n%s\n" % (simple_format(node, paragraph=False).strip()))
            write_fp(fp, r'\end{multicols}')
        elif node.attrib.get('class') == "center":
            write_fp(fp, "\n\\begin{center}\n%s\n\\end{center}\n" % (simple_format(node, paragraph=False).strip()))
        else:
            if node.attrib.get('class'):
                missing_tags.add("%s.%s" % (node.tag, node.attrib.get('class')))
            write_space(fp)
            if node.attrib.get('class') and "noindent" in node.attrib.get('class'):
                write_fp(fp, r"\noindent ")
            write_fp(fp, "\n%s\n" % (simple_format(node, paragraph=False).strip()))
        write_space(fp)
    elif node.tag == 'div':
        class_name = node.attrib.get('class', '')
        if 'prayer-group' in class_name:
            write_space(fp)
            if 'congregation' in class_name:
                write_fp(fp, r'\begin{minipage}{\textwidth}\begin{addmargin}[1.5in]{0em}' + "\n")
                write_tex(node, fp, doc)
                write_fp(fp, r'\end{addmargin}\end{minipage}' + "\n \\par")
            elif 'fathers' in class_name and not 'hymn-first' in class_name:
                write_fp(fp, r'\begin{minipage}{\textwidth}' + "\n")
                write_tex(node, fp, doc)
                write_fp(fp, r'\end{minipage}' + "\n \\par")
            elif all_prayer(node):
                write_fp(fp, r'\begin{samepage}' + "\n")
                last_was_space = True
                write_tex(node, fp, doc)
                write_fp(fp, r'\end{samepage}' + "\n")
            elif "lamb-of-god" in class_name:
                write_fp(fp, r'\noindent\begin{minipage}{\textwidth}' + "\n")
                write_tex(node, fp, doc)
                write_fp(fp, r'\end{minipage}' + "\n")
            else:
                write_tex(node, fp, doc)
            write_space(fp)
        elif node.attrib.get('class') == "columned":
            write_space(fp)
            write_fp(fp, r'\begin{paracol}{%s}' % len(node) + "\n")
            for column in node:
                write_tex(column, fp, doc)
                if column != node[-1]:
                    write_fp(fp, r'\switchcolumn' + "\n")
            write_fp(fp, r'\end{paracol}' + "\n")
            write_space(fp)
        elif node.attrib.get("aside"):
            text = node.attrib.get('aside')
            root = html.fromstring(text)
            content = simple_format(root, paragraph=False)
            write_fp(fp, r"\noindent\llap{%s }\parbox[t]{\textwidth}{" % content)
            last_was_space = True
            write_tex(node, fp, doc)
            write_fp(fp, "}\n")
        elif node.attrib.get('class') in ['rubric']:
            write_fp(fp, "\n\\rubric{%s} \n" % simple_format(node))
        else:
            div_class.add(node.attrib.get('class', ''))
            if node.attrib.get('number'):
                write_fp(fp, "\n\\noted{%s}{" % node.attrib.get('number'))
                last_was_space = True
                write_tex(node, fp, doc)
                write_fp(fp, "}\n")
            else:
                write_tex(node, fp, doc)
    elif node.tag == "img" and "content-image" in node.attrib.get("class", "") and not NO_IMAGES:
        src = os.path.splitext(node.attrib.get("src"))[0]
        write_fp(fp, r"\noindent\includegraphics[width=\textwidth]{%s}" % src)
    elif node.tag in ['ul', 'ol', 'blockquote']:
        write_fp(fp, simple_format(node))
    elif node.tag == 'prayer':
        write_fp(fp, prayer(node))
    elif node.tag == 'feast':
        root = html.fromstring(node.attrib.get('day'))
        day = simple_format(root, paragraph=False)
        write_fp(fp, r"\feast{%s}{%s}{%s}" % (day, node.attrib.get('level'), simple_format(node)))
    elif node.tag in ['player', 'gregorian']:
        if not NO_MUSIC:
            write_fp(fp, include_tex("music/%s.tex" % node.text, "keepwidth" in node.attrib))
    elif node.tag == 'music':
        if not NO_MUSIC:
            write_fp(fp, include_music("modern/lilypond/%s.tex" % node.text))
    elif node.tag == 'litany':
        write_fp(fp, litany(node))
    elif node.tag == 'psalm':
        write_fp(fp, psalm(node))
        write_space(fp)
    elif node.tag == 'hymn':
        write_fp(fp, hymn(node))
        write_space(fp)
    elif node.tag == 'table':
        write_fp(fp, table(node))
        write_space(fp)
    elif node.tag == "br":
        write_fp(fp, r" \\ ")
    elif node.tag == "break":
        write_fp(fp, r" \mybreak ")
    elif node.tag == 'hr':
        if node.attrib.get("class") == "rubric":
            write_fp(fp, r"\hrlinered")
        else:
            write_fp(fp, r"\hrline")
        write_space(fp)
    elif node.tag == 'reading':
        write_space(fp)
        text = simple_format(node)
        label = node.attrib.get("label", "")
        shorttag = node.attrib.get("shorttag", "")
        ref = node.attrib.get("ref", "")
        longref = node.attrib.get("longref", "")
        tagline = node.attrib.get("tagline", "")
        write_fp(fp, r"\reading{%s}{%s}{%s}{%s}{%s}{%s}" % (text, label, shorttag, ref, longref, tagline))
        write_space(fp)
    elif node.tag == "hrubric":
        left = node.attrib.get("left", "")
        center = node.attrib.get("center", simple_format(node))
        right = node.attrib.get("right", "")
        write_fp(fp, r"\hrubric{%s}{%s}{%s}" % (left, center, right))
    elif node.tag == 'include':
        file_name = os.path.join(os.path.dirname(doc), node.attrib.get('href'))
        xfilter = node.attrib.get('filter', '')
        print(xfilter)
        xremove = node.attrib.get('remove', '')
        parse_html(file_name, None, fp, xfilter=xfilter, xremove=xremove)
    elif node.tag == 'latex':
        write_fp(fp, node.text)
    else:
        if node.tag in ["strong", "p", "em", "span"]:
            write_fp(fp, "\n%s\n" % simple_format(node))
        missing_tags.add(node.tag)


def parse_html(doc, node, fp, xfilter="//body", xremove="", attr_remove=""):
    xpath = read_html(doc, node, xfilter, xremove, attr_remove)
    if node is not None and node.attrib.get("next"):
        next_doc = os.path.join(HTML, node.attrib.get("next"))
        next_xpath = read_html(next_doc, node, xfilter, xremove, attr_remove)
        try:
            body = set(xpath).pop()
            next_body = set(next_xpath).pop()
            first_language = node.attrib.get("first_language", "english")
            next_language = node.attrib.get("next_language")
            write_next_tex(body, next_body, first_language, next_language, fp, doc)
        except KeyError:
            pass
    else:
        try:
            body = set(xpath).pop()
            write_tex(body, fp, doc)
        except KeyError:
            pass

def read_html(doc, node, xfilter, xremove, attr_remove):
    with codecs.open(doc, "rU", encoding='utf8') as h_fp:
        text = h_fp.read()
        text = re.sub("(-|­)(\n|\r)\s*", "", text)  # copying from PDF gives words broken by -
        nodes = html.fromstring(text)
        # print(doc)
        for title in nodes.xpath("//title"):
            if node is not None and len(node) and title.text.strip() != node.attrib.get('title').strip():
                pass  # print("'{}' != '{}'".format(title.text, node.attrib.get('title')))
        if xfilter == None:
            xfilter = "//body"
        if xremove:
            for remove in xremove.split(","):
                for n in nodes.xpath(remove):
                    n.getparent().remove(n)
        if attr_remove:
            for remove in attr_remove.split(","):
                select, _, attr = remove.partition(":")
                for n in nodes.xpath(select):
                    n.attrib.pop(attr)
        xpath = nodes.xpath(xfilter)
    return xpath


def index(nodes, fp, chapterheadings=None):
    global appendix
    global headerdepth
    global in_appendix
    for node in nodes:
        if node.tag == 'chapter':
            if node.getparent().tag == "chapter" or node.getparent().tag == "appendix":
                headerdepth = "chapter"
                write_fp(fp, r'\newpageheader{%s}{%s}' % (special_chars(node.getparent().attrib.get('title')), special_chars(node.attrib.get('title'))))
                if chapterheadings:
                    if chapterheadings == "part":
                        title = special_chars(node.attrib.get('title'))
                        write_fp(fp, "\n\\chapter*{%s}\n\\addcontentsline{toc}{chapter}{%s}\n\n" % (title, title))
                    else:
                        title = special_chars(node.attrib.get('title'))
                        write_fp(fp, "\n\\section*{%s}\n\\addcontentsline{toc}{section}{%s}\n\n" % (title, title))
            else:
                #print(chapterheadings)
                if chapterheadings:
                    title = special_chars(node.attrib.get('title'))
                    if chapterheadings == "part":
                        write_fp(fp, "\n\\part*{%s}\n\\addcontentsline{toc}{part}{%s}\n\n" % (title, title))
                    else:
                        write_fp(fp, "\n\\chapter*{%s}\n\\addcontentsline{toc}{chapter}{%s}\n\n" % (title, title))
                headerdepth = "section"
            if node.attrib.get('chapterheadings') == 'none':
                index(node, fp, None)
            else:
                index(node, fp, chapterheadings)
            headerdepth = "section"
        elif node.tag == 'section':
            if headerdepth == "section":
                write_fp(fp, r'\newpageheader{%s}{%s}' % (special_chars(node.getparent().attrib.get('title')), special_chars(node.attrib.get('title'))))
            xfilter = node.attrib.get("filter")
            xremove = node.attrib.get("remove")
            attr_remove = node.attrib.get("attrremove")
            parse_html(os.path.join(HTML, node.attrib.get("doc")), node, fp, xfilter, xremove, attr_remove)
            if not node.attrib.get('nobreak'):# or node is nodes[-1]:
                write_fp(fp, "\\newpage\n")
        elif node.tag == 'appendix':
            if chapterheadings:
                in_appendix = True
            write_fp(fp, """\\begin{appendices}\n""")
            index(node, fp, chapterheadings)
            write_fp(fp, "\\end{appendices}\n")
        elif node.tag == 'insert':
            write_fp(fp, r'\includeimage{%s}' % node.attrib.get('file'))
        elif node.tag == 'include':
            write_fp(fp, r'\input{%s}' % node.attrib.get('file'))
        elif node.tag == 'latex':
            if node.attrib.get('file'):
                with open(node.attrib.get('file'), 'r') as fp2:
                    write_fp(fp, fp2.read())
            else:
                write_fp(fp, node.text)
            write_fp(fp, "\n")

def single_index(nodes):
    global headerdepth
    for node in nodes:
        if node.tag == 'chapter':
            if node.getparent().tag == "chapter":
                pass#write_fp(fp, r'\newpageheader{%s}{%s}' % (special_chars(node.getparent().attrib.get('title')), special_chars(node.attrib.get('title'))))
            else:
                headerdepth = "section"
            single_index(node)
            headerdepth = "section"
        elif node.tag == 'section':
            doc = node.attrib.get("doc")
            name, _, ext = doc.rpartition(".")
            try:
                with codecs.open(os.path.join(output, "{}.tex".format(name)), "w", encoding='utf8') as fp:
                    if headerdepth == "section":
                        write_fp(fp, r'\newpageheader{%s}{%s}' % (special_chars(node.getparent().attrib.get('title')), special_chars(node.attrib.get('title'))))
                    xfilter = node.attrib.get("filter")
                    xremove = node.attrib.get("remove")
                    attrremove = node.attrib.get("attrremove")
                    parse_html(os.path.join(HTML, node.attrib.get("doc")), node, fp, xfilter, xremove, attrremove)
                    if not node.attrib.get('nobreak') or node is nodes[-1]:
                        write_fp(fp, "\\newpage\n")
            except FileNotFoundError:
                pass
        elif node.tag == 'appendix':
            single_index(node)

if index_file is None:
    with codecs.open(output, "w", encoding='utf8') as fp:
        write_fp(fp, r"""% !TEX program = LuaLaTeX+se
% !TEX encoding = UTF-8 Unicode
\documentclass{book}
\RequirePackage[a5paper,top=0.5in,inner=0.5in,outer=0.5in,bottom=0.5in]{geometry}

\input{../prayer-header}

\renewcommand{\newpageheader}[2]{}
\pagestyle{empty}


\begin{document}

""")
        parse_html(os.path.join(HTML), None, fp)
        write_fp(fp, r"""
\end{document}""")
elif os.path.isdir(output):
    tree = etree.parse(index_file)
    for node in tree.xpath("//index"):
        single_index(node)
else:
    with codecs.open(output, "w", encoding='utf8') as fp:
        write_fp(fp, """% !TEX program = LuaLaTeX+se\n""")
        try:
            tree = etree.parse(index_file)
        except etree.XMLSyntaxError as e:
            print("Could not Parse XML for: %s" % index_file)
        for node in tree.xpath("//index"):
            headerdepth = node.attrib.get("headerdepth", headerdepth)
            chapterheadings = node.attrib.get("chapterheadings")
            index(node, fp, chapterheadings)

    # read and write the file again so we can do extra processing
    with codecs.open(output, "r", encoding='utf8') as fp:
        text = fp.read()
        text = re.sub('\n\n\n+', '\n\n', text)
    with codecs.open(output, "w", encoding='utf8') as fp:
        fp.write(text)

print("Missing lower level: %s" % missing_format)
print("Missing upper level: %s" % missing_tags)
print(div_class)
