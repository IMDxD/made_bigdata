#!/usr/bin/env python3
import sys
import re
from xml.etree import ElementTree

tags_punkt_re = re.compile(r"[<> ]+")

for line in sys.stdin:
    line = line.strip()
    if line.startswith("<row"):
        row = ElementTree.fromstring(line)
        creation_year = row.get("CreationDate")[:4]
        tags = row.get("Tags")
        if tags:
            tags = tags_punkt_re.sub(" ", tags).strip()
            for tag in tags.split():
                print(creation_year, tag, 1, sep="\t")
