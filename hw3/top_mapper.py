#!/usr/bin/env python3
import sys

for line in sys.stdin:
    year, tag, count = line.strip().split("\t", 3)
    if year in {"2010", "2016"}:
        print(year, count, tag, sep="\t")
