#!/usr/local/bin/python

import sys

for line in sys.stdin:
    i_a, i_b, s = line.strip().split('\t')
    print "%s\t%s" % (i_a + "" + i_b, s)
