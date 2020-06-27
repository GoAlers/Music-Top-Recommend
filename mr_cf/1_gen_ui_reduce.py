#!/usr/local/bin/python

import sys
import math

cur_item = None
user_score_list = []

for line in sys.stdin:
    item, user, score = line.strip().split("\t")
    if not cur_item:
        cur_item = item
    if item != cur_item:
        sum = 0.0
        for tuple in user_score_list:
            (u, s) = tuple
            sum += pow(s, 2)
        sum = math.sqrt(sum)
        for tuple in user_score_list:
            (u, s) = tuple
            print "%s\t%s\t%s" % (u, cur_item, float(s / sum))

        user_score_list = []
        cur_item = item

    user_score_list.append((user, float(score)))

sum = 0.0
for tuple in user_score_list:
    (u, s) = tuple
    sum += pow(s, 2)
sum = math.sqrt(sum)
for tuple in user_score_list:
    (u, s) = tuple
    print "%s\t%s\t%s" % (u, cur_item, float(s / sum))
