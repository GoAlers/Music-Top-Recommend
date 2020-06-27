#coding=utf-8
import sys
sys.path.append('../')
reload(sys)
sys.setdefaultencoding('utf-8')

import jieba
import jieba.analyse
import jieba.posseg

merge_base_infile = '../data/merge_base.data'
output_file = '../data/samples.data'

output_user_feature_file = '../data/user_feature.data'
output_item_feature_file = '../data/item_feature.data'

output_itemid_to_name_file = '../data/name_id.dict'

def get_base_samples(infile):
    ret_samples_list = []
    user_info_set = set()
    item_info_set = set()
    item_name2id = {}
    item_id2name = {}

    with open(infile, 'r') as fd:
        for line in fd:
            ss = line.strip().split('\001')
            if len(ss) != 13:
                continue
            userid = ss[0].strip()
            itemid = ss[1].strip()
            watch_time = ss[2].strip()
            total_time = ss[10].strip()

            # user info
            gender = ss[4].strip()
            age = ss[5].strip()
            user_feature = '\001'.join([userid, gender, age])

            # item info
            name = ss[8].strip()
            item_feature = '\001'.join([itemid, name])

            # label info
            label = float(watch_time) / float(total_time)
            final_label = '0'

            if label >= 0.82:
                final_label = '1'
            elif label <= 0.3:
                final_label = '0'
            else:
                continue

            # gen name2id dict for item feature
            item_name2id[name] = itemid

            # gen id2name dict
            item_id2name[itemid] = name

            # gen all samples list
            ret_samples_list.append([final_label, user_feature, item_feature])

            # gen uniq userinfo
            user_info_set.add(user_feature)
            item_info_set.add(name)

    return ret_samples_list, user_info_set, item_info_set, item_name2id, item_id2name


# step1. generate base samples(label, user feature, item feature)
base_sample_list, user_info_set, item_info_set, item_name2id, item_id2name = \
    get_base_samples(merge_base_infile)


# step2. extract user feature
user_fea_dict = {}
for info in user_info_set:
    userid, gender, age = info.strip().split('\001')
    #gender
    idx = 0 # default 女
    if gender == '男':
        idx = 1

    gender_fea = ':'.join([str(idx), '1'])

    # age
    idx = 0
    if age == '0-18':
        idx = 0
    elif age == '19-25':
        idx = 1
    elif age == '26-35':
        idx = 2
    elif age == '36-45':
        idx = 3
    else:
        idx = 4

    idx += 2

    age_fea = ':'.join([str(idx), '1'])

    user_fea_dict[userid] = ' '.join([gender_fea, age_fea])

# step3. extract item feature

token_set = set()

item_fs_dict = {}
for name in item_info_set:
    token_score_list = []
    for x, w in jieba.analyse.extract_tags(name, withWeight=True):
        token_score_list.append((x, w))
        token_set.add(x)
    item_fs_dict[name] = token_score_list

user_feature_offset = 10
# gen item id feature
token_id_dict = {}
for tu in enumerate(list(token_set)):
    # token -> token id
    token_id_dict[tu[1]] = tu[0]

item_fea_dict = {}
for name, fea in item_fs_dict.items():
    tokenid_score_list = []
    for (token, score) in fea:
        if token not in token_id_dict:
            continue
        token_id = token_id_dict[token] + user_feature_offset
        tokenid_score_list.append(':'.join([str(token_id), str(score)]))

    item_fea_dict[name] = ' '.join(tokenid_score_list)


# step 4.generate final samples
ofile = open(output_file, 'w')
for (label, user_feature, item_feature) in base_sample_list:
    userid = user_feature.strip().split('\001')[0]
    item_name = item_feature.strip().split('\001')[1]
    if userid not in user_fea_dict:
        continue
    if item_name not in item_fea_dict:
        continue

    ofile.write(' '.join([label, user_fea_dict[userid], item_fea_dict[item_name]]))
    ofile.write('\n')
ofile.close()
# step 5. generate user feature mapping file
o_u_file = open(output_user_feature_file, 'w')
for userid, feature in user_fea_dict.items():
    o_u_file.write('\t'.join([userid, feature]))
    o_u_file.write('\n')
o_u_file.close()

# step 6. generate item feature mapping file
o_i_file = open(output_item_feature_file, 'w')
for item_name, feature in item_fea_dict.items():
    if item_name not in item_name2id:
        continue
    itemid = item_name2id[item_name]
    o_i_file.write('\t'.join([itemid, feature]))
    o_i_file.write('\n')
o_i_file.close()

# step 7. generate item id to name mapping file
o_file = open(output_itemid_to_name_file, 'w')
for itemid, item_name in item_id2name.items():
    o_file.write('\t'.join([itemid, item_name]))
    o_file.write('\n')
o_file.close()
