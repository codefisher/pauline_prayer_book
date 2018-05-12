import re
import os
import codecs
from lxml import etree, html
import sys

if len(sys.argv) == 4:
    index_file, HTML, output = sys.argv[1:]
elif len(sys.argv) == 3:
    index_file = None
    HTML, output = sys.argv[1:]
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
            fp.write("\\medbreak\n")
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
    return (text.replace("… ", r"\ldots ~").replace("\u00A0", "~").replace("…", r"\ldots ")
            .replace('†', r'\GreDagger').replace('—', '---').replace('–', '--').replace('“', '``')
            .replace('”', "''").replace('’', "'").replace('‘', "`").replace("☩", r"\ding{64}"))
    
def format_help(node, span_as_normal=False):
    result = [node.text]
    for n in node.getchildren():
        result.append(simple_format(n, white=True, span_as_normal=span_as_normal))
    return "".join(filter(None, result))

def simple_format(node, white=False, span_as_normal=False):
    result = []
    if node.tag == "sup":
        result.append(r"\textsuperscript{%s}" % format_help(node))
    if node.tag == "sp":
        if node.text == "R/":
            result.append(r"\cross{\Rbar.}")
        if node.text == "V/":
            result.append(r"\cross{\Vbar.}")
        if node.text == "+":
            result.append(r"\red{\GreDagger}")
    elif node.tag == "strong":
        result.append(r"\textbf{%s}" % format_help(node))
    elif node.tag == "em":
        result.append(r"\textit{%s}" % format_help(node))
    elif node.tag == "u":
        result.append(r"\underline{%s}" % format_help(node))
    elif node.tag == "span":
        if node.attrib.get("class") == "rubric":
            span = r"\rubric{%s}" % format_help(node)
        elif node.attrib.get("class") == "cross":
            span = r"\cross{%s}" % format_help(node)
        elif node.attrib.get('class') == 'ref':
            span = "\n\\reference{%s}\n" % format_help(node)
        elif node.attrib.get('class') == 'right':
            span = "\hfill" + format_help(node)
        else:
            if node.attrib.get("class"):
                missing_format.add("%s.%s" % (node.tag, node.attrib.get("class")))
            span = format_help(node)
        if span_as_normal:
            result.append(r"\\ {\small\normalfont %s}" % span)
        else:
            result.append(span)
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
        result.append("\\begin{enumerate}\n" + format_help(node))
    elif node.tag == "li":
        result.append("\\item %s\n" % format_help(node))
    elif node.tag in ['player', 'gregorian']:
        result.append(include_tex("music/%s.tex" % node.text))
    elif node.tag == 'music':
        result.append(include_music("music/lilypond/%s.tex" % node.text))
    else:
        missing_format.add(node.tag)
        result.append(format_help(node, span_as_normal=span_as_normal))
    if node.tag == "a" and "#" in node.attrib.get("href", ""):
        result.append(' p.~\pageref{%s}' % re.sub('[^a-zA-Z]', '', node.attrib.get("href")))
    result.append(node.tail)
    if node.tag == "ul":
        result.append(r"\end{itemize}")
    elif node.tag == "ol":
            result.append(r"\end{enumerate}")
    elif node.tag == "blockquote":
        result.append(r"\end{addmargin}")
    text = "".join(filter(None, result))
    if white:
        return special_chars(text)
    else:
        return special_chars(no_white(text))

def heading_help(node, heading, index):
    global appendix
    extra = ""
    if index:
        extra += "\n\\addcontentsline{toc}{%s}{%s}" % (heading[:-1], title(node.text_content()))
    result = ""
    if not len(node) or not node[0].text:
        result = (r"""
\%s{%s}""" % (heading, title(simple_format(node))))
    else:
        full_title = title(simple_format(node, span_as_normal=True)).lstrip(r"\\ ")
        print(full_title)
        main_title = title(no_white(node.text)).strip()
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
    return "\n%s%s\n\n" % (result, extra)

def heading(node, doc):
    prefex = ''
    if not node.text or not title_clean.match(node.text):
        prefex = '*'
    index = node.attrib.get("class") and "index" in node.attrib.get("class")
    if node.attrib.get('id'):
        before = "\n\\label{%s}" % re.sub("[^a-zA-Z]", "", os.path.basename(doc) + node.attrib.get('id'))
    if node.tag == 'h1':
        if node.attrib.get("class") and 'section' in node.attrib.get('class'):
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
    text = text.replace(r"\par \par", r"\par \medbreak")
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
            result.append(r"\medbreak")
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
            result.append(r"%s \par" % row.strip())
    return "\\begin{litany}%s\n\\end{litany}\n" % "\n".join(result)

def psalm(node):
    text = simple_format(node, True).strip()
    extra = ""
    result = []
    numbers = "numbers" in node.attrib
    for i, stanza in enumerate(text.strip().split("\n\n")):
        if numbers:
            result.append(r"\item[%s.]" % (i + 1))
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
    if "red" in node.attrib:
        extra += r"\item[\red{\textbf{%s}}]" % node.attrib.get("red")
    #if numbers or "red" in node.attrib:
    #    return "\\begin{psalm}%s%s\n\\end{psalm}\n" % (extra, "\n".join(result))
    return "\\begin{psalm}%s%s\n\\end{psalm}\n" % (extra, "\n".join(result))

def hymn(node):
    text = simple_format(node, True).strip()

    stanzas = []
    first = None
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
        result.append(r'\medbreak')
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

def include_tex(name):
    script_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_path, name), "r") as fp:
        text = fp.read()
        result = []
        for line in text.split('\n'):
            if line and not (line[0] == '%' or '{document}' in line or '{minipage}' in line or r'\documentclass' in line or r'\RequirePackage' in line or r'\usepackage' in line or r'\input' in line):
                result.append(line.replace(r'\gregorioscore{', r'\gregorioscore{music/'))
        return "\n".join(result)

def include_music(name):
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
        if node.tag != "prayer":
            return False
    return True

def write_tex(nodes, fp, doc):
    global last_was_space
    for node in nodes:
        if node.attrib.get('id'):
            write_fp(fp, "\n\\label{%s}" % re.sub("[^a-zA-Z]", "", os.path.basename(doc) + node.attrib.get('id')))
        if "necrology" in node.attrib.get('id', ''):
            continue
        if node.tag in ["h1", "h2", "h3", "h4", "h5"]:
            if node.attrib.get('class') == 'rubric':
                write_fp(fp, "\n\\titlerubric{%s}\n" % simple_format(node).strip())
            else:
                write_header(fp, heading(node, doc))
        elif node.tag == 'p':
            if node.attrib.get('class') == 'instruction':
                write_space(fp)
                write_fp(fp, "\n\\instruction{%s}\n" % simple_format(node).strip())
            elif node.attrib.get('class') == 'ref':
                write_space(fp)
                write_fp(fp, "\\begin{flushright}\\red{%s}\\end{flushright}\n" % simple_format(node).strip())
            elif node.attrib.get('class') == 'indented-prayer':
                write_space(fp)
                write_fp(fp, "\n\\begin{addmargin}[6em]{0em}\\noindent%s\\end{addmargin}\n" % simple_format(node).strip())
            else:
                if node.attrib.get('class'):
                    missing_tags.add("%s.%s" % (node.tag, node.attrib.get('class')))
                write_space(fp)
                if node.attrib.get('class') and "noindent" in node.attrib.get('class'):
                    write_fp(fp, r"\noindent ")
                write_fp(fp, "\n%s\n" % simple_format(node).strip())
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
                write_fp(fp, r'\begin{paracol}{%s}' % len(node) + "\n")
                for column in node:
                    write_tex(column, fp, doc)
                    if column != node[-1]:
                        write_fp(fp, r'\switchcolumn' + "\n")
                write_fp(fp, r'\end{paracol}' + "\n")
            elif node.attrib.get('class') in ['rubric']:
                write_fp(fp, "\n\\rubric{%s} \n" % simple_format(node))
            else:
                div_class.add(node.attrib.get('class', ''))
                write_tex(node, fp, doc)
        elif node.tag == "img" and "content-image" in node.attrib.get("class", ""):
            write_fp(fp, r"\noindent\includegraphics[width=\textwidth]{%s}" % node.attrib.get("src"))
        elif node.tag in ['ul', 'ol', 'blockquote']:
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
            write_fp(fp, r" \newpage ")
        elif node.tag == 'hr':
            if node.attrib.get("class") == "rubric":
                write_fp(fp, r"\hrlinered")
            else:
                write_fp(fp, r"\hrline")
            write_space(fp)
        elif node.tag == 'reading':
            write_space(fp)
            write_fp(fp, r"\needspace{4\baselineskip}")
            if "label" in node.attrib:
                write_fp(fp, r"\noindent\textsc{\red{%s}}" % node.attrib.get("label") + "\n")
            text = simple_format(node)
            if text:
                if "label" in node.attrib:
                    write_fp(fp, r"\\")
                write_fp(fp, simple_format(node) + "\n")
            if "shorttag" in node.attrib:
                write_fp(fp, r"\noindent\red{%s}" % node.attrib.get('shorttag'))
            if "ref" in node.attrib:
                write_fp(fp, r"\reference{%s}" % node.attrib.get('ref').replace("R/", "\Rbar"))
            if "longref" in node.attrib:
                write_fp(fp, r"\begin{center}\red{%s}\end{center}" % node.attrib.get("longref"))
            if "tagline" in node.attrib:
                write_fp(fp, r"\begin{center}\textit{\footnotesize{\red{%s}}}\end{center}" % node.attrib.get("tagline"))
            write_space(fp)
        else:
            missing_tags.add(node.tag)

def parse_html(doc, node, fp):
    with codecs.open(doc, "r", encoding='utf8') as h_fp:
        text = h_fp.read()
        text = re.sub("-(\n|\r)\s*", "", text) # copying from PDF gives words broken by -
        nodes = html.fromstring(text)
        print(doc)
        for title in nodes.xpath("//title"):
            if len(node) and title.text.strip() != node.attrib.get('title').strip():
                print("'{}' != '{}'".format(title.text, node.attrib.get('title')))
        for body in nodes.xpath("//body"):
            write_tex(body, fp, doc)

def index(nodes, fp, chapterheadings=None):
    global appendix
    global headerdepth
    for node in nodes:
        if node.tag == 'chapter':
            if node.getparent().tag == "chapter":
                headerdepth = "chapter"
                write_fp(fp, r'\newpageheader{%s}{%s}' % (special_chars(node.getparent().attrib.get('title')), special_chars(node.attrib.get('title'))))
                if chapterheadings:
                    title = special_chars(node.attrib.get('title'))
                    write_fp(fp, "\n\\section*{%s}\n\\addcontentsline{toc}{section}{%s}\n\n" % (title, title))
            else:
                print(chapterheadings)
                if chapterheadings:
                    title = special_chars(node.attrib.get('title'))
                    write_fp(fp, "\n\\chapter*{%s}\n\\addcontentsline{toc}{chapter}{%s}\n\n" % (title, title))
                headerdepth = "section"
            index(node, fp, chapterheadings)
            headerdepth = "section"
        elif node.tag == 'section':
            if headerdepth == "section":
                write_fp(fp, r'\newpageheader{%s}{%s}' % (special_chars(node.getparent().attrib.get('title')), special_chars(node.attrib.get('title'))))
            parse_html(os.path.join(HTML, node.attrib.get("doc")), node, fp)
            if not node.attrib.get('nobreak') or node is nodes[-1]:
                write_fp(fp, "\\newpage\n")
        elif node.tag == 'appendix':
            write_fp(fp, """\\begin{appendices}\n""")
            index(node, fp, chapterheadings)
            write_fp(fp, "\\end{appendices}\n")
        elif node.tag == 'insert':
            write_fp(fp, r'\includeimage{%s}' % node.attrib.get('file'))
        elif node.tag == 'include':
            write_fp(fp, r'\input{%s}' % node.attrib.get('file'))

def single_index(nodes):
    global headerdepth
    for node in nodes:
        if node.tag == 'chapter':
            if node.getparent().tag == "chapter":
                write_fp(fp, r'\newpageheader{%s}{%s}' % (special_chars(node.getparent().attrib.get('title')), special_chars(node.attrib.get('title'))))
            else:
                headerdepth = "section"
            single_index(node)
            headerdepth = "section"
        elif node.tag == 'section':
            doc = node.attrib.get("doc")
            name, _, ext = doc.rpartition(".")
            with codecs.open(os.path.join(output, "{}.tex".format(name)), "w", encoding='utf8') as fp:
                if headerdepth == "section":
                    write_fp(fp, r'\newpageheader{%s}{%s}' % (special_chars(node.getparent().attrib.get('title')), special_chars(node.attrib.get('title'))))
                parse_html(os.path.join(HTML, node.attrib.get("doc")), node, fp)
                if not node.attrib.get('nobreak') or node is nodes[-1]:
                    write_fp(fp, "\\newpage\n")
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

print(missing_format)
print(missing_tags)
print(div_class)
