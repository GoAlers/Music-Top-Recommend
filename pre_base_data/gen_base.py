#coding=utf-8
import sys

user_action_data = '../data/user_watch_pref.sml'
music_meta_data = '../data/music_meta'
user_profile_data = '../data/user_profile.data'

output_file = '../data/merge_base.data'

# 将3份数据merge后的结果输出，供下游数据处理
ofile = open(output_file, 'w')

# step 1. decode music meta data
item_info_dict = {}
with open(music_meta_data, 'r') as fd:
    for line in fd:
        ss = line.strip().split('\001')
        if len(ss) != 6:
            continue
        itemid, name, desc, total_timelen, location, tags = ss
        item_info_dict[itemid] = '\001'.join([name, desc, total_timelen, location, tags])

# step 2. decode user profile data
user_profile_dict = {}
with open(user_profile_data, 'r') as fd:
    for line in fd:
        ss = line.strip().split(',')
        if len(ss) != 5:
            continue
        userid, gender, age, salary, location = ss
        user_profile_dict[userid] = '\001'.join([gender, age, salary, location])

# step 3. decode user action data
# output merge data
with open(user_action_data, 'r') as fd:
    for line in fd:
        ss = line.strip().split('\001')
        if len(ss) != 4:
            continue
        userid, itemid, watch_len, hour = ss

        if userid not in user_profile_dict:
            continue

        if itemid not in item_info_dict:
            continue

        ofile.write('\001'.join([userid, itemid, watch_len, hour, \
                user_profile_dict[userid], item_info_dict[itemid]]))
        ofile.write("\n")

ofile.close()
