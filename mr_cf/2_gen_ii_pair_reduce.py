#!/usr/local/bin/python

import sys

cur_user = None
item_score_list = []

for line in sys.stdin:
    user, item, score = line.strip().split("\t")
    if not cur_user:
        cur_user = user
    if user != cur_user:
        for i in range(0, len(item_score_list) - 1):
            for j in range(i + 1, len(item_score_list)):
                item_a, score_a = item_score_list[i]
                item_b, score_b = item_score_list[j]
                print "%s\t%s\t%s" % (item_a, item_b, score_a * score_b)
                print "%s\t%s\t%s" % (item_b, item_a, score_a * score_b)

        item_score_list = []
        cur_user = user

    item_score_list.append((item, float(score)))

for i in range(0, len(item_score_list) - 1):
    for j in range(i + 1, len(item_score_list)):
        item_a, score_a = item_score_list[i]
        item_b, score_b = item_score_list[j]
        print "%s\t%s\t%s" % (item_a, item_b, score_a * score_b)
        print "%s\t%s\t%s" % (item_b, item_a, score_a * score_b)
