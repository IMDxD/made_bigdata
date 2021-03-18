#!/usr/bin/env python3
import sys

current_year = None
current_tag = None
tag_count = 0

for line in sys.stdin:
    year, tag, counts = line.split("\t", 3)
    counts = int(counts)
    if current_tag and tag == current_tag and year == current_year:
        tag_count += counts
    else:
        if current_tag:
            print(current_year, current_tag, tag_count, sep="\t")
        current_year = year
        current_tag = tag
        tag_count = counts

if current_tag:
    print(current_year, current_tag, tag_count, sep="\t")
