#coding=utf-8
import sys

infile = '../data/cf.result'
outfile = '../data/cf_reclist.redis'

ofile = open(outfile, 'w')

MAX_RECLIST_SIZE = 100
PREFIX = 'CF_'

rec_dict = {}
with open(infile, 'r') as fd:
    for line in fd:
        itemid_A, itemid_B, sim_score = line.strip().split('\t')

        if itemid_A not in rec_dict:
            rec_dict[itemid_A] = []
        rec_dict[itemid_A].append((itemid_B, sim_score))


for k, v in rec_dict.items():
    key_item = PREFIX + k
    reclist_result = '_'.join([':'.join([tu[0], str(round(float(tu[1]), 6))]) \
              for tu in sorted(v, key=lambda x: x[1], reverse=True)[:MAX_RECLIST_SIZE]])

    ofile.write(' '.join(['SET', key_item, reclist_result]))
    ofile.write("\n")

ofile.close()