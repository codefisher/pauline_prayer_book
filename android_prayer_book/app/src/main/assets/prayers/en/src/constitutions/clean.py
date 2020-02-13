import re

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('html_file', type=str)
args = parser.parse_args()

if args.html_file is not None:
    html_file = args.html_file
else:
    exit()

with open(html_file, 'r') as fp:
    text = fp.read()

text = re.sub(r'(Article \d+)\n', r'\n<h2>\1</h2>\n\n', text)
text = re.sub(r'(Norm \d+.*)\n', r'\n<h2>\1</h2>\n\n', text)
text = re.sub(r'\n§\d+\.(.*)', r'\n<li>\1</li>', text)
text = re.sub(r'\n[a-zA-Z][\)\.](.*)', r'\n<li>\1</li>', text)
text = re.sub(r'\n[0-9]+[\)\.](.*)', r'\n<li>\1</li>', text)
text = re.sub(r'\n[•◦] (.*)', r'\n<li>\1</li>', text)
text = re.sub(r'((<li>.*</li>\s+)+)', r'\n<ol>\n\1</ol>\n\n', text)
text = re.sub(r'([^<>\n][^<>\n]+\n)', r'<p>\n\1</p>\n', text)
text = re.sub(r'(\d)([a-z]{2})', r'\1<sup>\2</sup>', text)

with open(html_file, 'w') as fp:
    fp.write(text)