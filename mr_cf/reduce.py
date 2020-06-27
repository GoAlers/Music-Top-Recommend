#!/usr/local/bin/python

import sys

previous = ""
count = 0

for line in sys.stdin:
	kv = line.strip('\n').split("\t")
	word = kv[0]
	if (previous != "" and previous != word):
		print "%s\t%s" % (word, count)
		previous = word
		count = 1
	else:
		previous = word
		count += 1

print "%s\t%s" % (word, count)
