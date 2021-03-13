import sys
import random

for line in sys.stdin:
    line = line.strip()
    r = random.randint(0, 10001)
    print '%s_%s' % (r, line)
