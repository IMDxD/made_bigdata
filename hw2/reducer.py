import sys
import random


r = random.randint(1, 6)
tmp = []

for line in sys.stdin:
    tmp.append(line.rstrip().split("_")[1])
    if len(tmp) == r:
        print ",".join(tmp)
        r = random.randint(1, 6)
        tmp = []

if len(tmp) != 0:
    print ",".join(tmp)
