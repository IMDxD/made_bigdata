#!/usr/bin/env python3
import sys

twentyten_cnt = 0
twentysix_cnt = 0

for line in sys.stdin:
    year, counts, tag = line.strip().split("\t", 3)
    if year == "2010" and twentyten_cnt < 10:
        twentyten_cnt += 1
        print(year, tag, counts, sep="\t")
    if year == "2016" and twentysix_cnt < 10:
        twentysix_cnt += 1
        print(year, tag, counts, sep="\t")
