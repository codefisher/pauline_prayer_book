import glob
from lxml import etree
import os

for filename in glob.glob("*/menu.xml"):
	print(filename)
	folder = filename.split("/")[0]
	tree = etree.parse(filename)
	for item in tree.xpath("//menuitem"):
		if not os.path.isfile(os.path.join(folder, item.attrib.get("doc"))):
			print(os.path.join(folder, item.attrib.get("doc")))


