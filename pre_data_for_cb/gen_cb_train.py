#coding=utf-8
import sys
sys.path.append('../')
reload(sys)
sys.setdefaultencoding('utf-8')

import jieba
import jieba.posseg
import jieba.analyse

input_file = "../data/merge_base.data"

# 输出cb训练数据
output_file = '../data/cb_train.data'
ofile = open(output_file, 'w')

RATIO_FOR_NAME = 0.9
RATIO_FOR_DESC = 0.1
RATIO_FOR_TAGS = 0.05

idf_file = '../data/idf.txt'
idf_dict = {}
with open(idf_file, 'r') as fd:
    for line in fd:
        token, idf_score = line.strip().split(' ')
        idf_dict[token] = idf_score


itemid_set = set()
with open(input_file, 'r') as fd:
    for line in fd:
        ss = line.strip().split('\001')
        # 用户行为
        userid = ss[0].strip()
        itemid = ss[1].strip()
        watch_len = ss[2].strip()
        hour = ss[3].strip()
        # 用户画像
        gender = ss[4].strip()
        age = ss[5].strip()
        salary = ss[6].strip()
        user_location = ss[7].strip()
        # 物品元数据
        name = ss[8].strip()
        desc = ss[9].strip()
        total_timelen = ss[10].strip()
        item_location = ss[11].strip()
        tags = ss[12].strip()

        # itemid去重
        if itemid not in itemid_set:
            itemid_set.add(itemid)
        else:
            continue

        # token for name, desc
        token_dict = {}
        for a in jieba.analyse.extract_tags(name, withWeight=True):
            token = a[0]
            score = float(a[1])
            token_dict[token] = score * RATIO_FOR_NAME

        # token for desc
        for a in jieba.analyse.extract_tags(desc, withWeight=True):
            token = a[0]
            score = float(a[1])
            if token in token_dict:
                token_dict[token] += score * RATIO_FOR_DESC
            else:
                token_dict[token] = score * RATIO_FOR_DESC

        # token for tags
        for tag in tags.strip().split(','):
            if tag not in idf_dict:
                continue
            else:
                if tag in token_dict:
                    token_dict[tag] += float(idf_dict[tag]) * RATIO_FOR_TAGS
                else:
                    token_dict[tag] = float(idf_dict[tag]) * RATIO_FOR_TAGS


        for k, v in token_dict.items():
            token = k.strip()
            score = str(v)
            #print token, itemid, score
            ofile.write(','.join([token, itemid, score]))
            ofile.write("\n")


ofile.close()
