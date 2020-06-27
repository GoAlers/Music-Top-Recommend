#coding=utf-8
import web
import sys
import redis
import json
import math

urls = (
    '/', 'index',
    '/test', 'test',
)

app = web.application(urls, globals())

# load user fea
user_fea_dict = {}
with open('../data/user_feature.data') as fd:
    for line in fd:
        userid, fea_list_str = line.strip().split('\t')
        user_fea_dict[userid] = fea_list_str

# load item fea
item_fea_dict = {}
with open('../data/item_feature.data') as fd:
    for line in fd:
        ss = line.strip().split('\t')
        if len(ss) != 2:
            continue
        itemid, fea_list_str = ss
        item_fea_dict[itemid] = fea_list_str

class index:
    def GET(self):
        r = redis.Redis(host='master', port=6379,db=0)
        # step 1 : 解析请求
        params = web.input()
        userid = params.get('userid', '')
        req_itemid = params.get('itemid', '')

        # step 2 : 加载模型
        model_w_file_path = '../rankmodel/model.w'
        model_b_file_path = '../rankmodel/model.b'

        model_w_list = []
        model_b = 0.
        with open (model_w_file_path, 'r') as fd:
            for line in fd:
                ss = line.strip().split(' ')
                if len(ss) != 3:
                    continue
                model_w_list.append(float(ss[2].strip()))

        with open (model_b_file_path, 'r') as fd:
            for line in fd:
                ss = line.strip().split(' ')
                model_b = float(ss[2].strip())

        # step 3 : 检索候选(match)
        rec_item_mergeall = []
        # 3.1 cf
        cf_recinfo = 'null'
        key = '_'.join(['CF', req_itemid])
        if r.exists(key):
            cf_recinfo = r.get(key)

        if len(cf_recinfo) > 6:
            for cf_iteminfo in cf_recinfo.strip().split('_'):
                item, score = cf_iteminfo.strip().split(':')
                rec_item_mergeall.append(item)

        # 3.2 cb
        cb_recinfo = 'null'
        key = '_'.join(['CB', req_itemid])
        if r.exists(key):
            cb_recinfo = r.get(key)
        if len(cb_recinfo) > 6:
            for cb_iteminfo in cb_recinfo.strip().split('_'):
                item, score = cb_iteminfo.strip().split(':')
                rec_item_mergeall.append(item)

        # step 4: 获取用户的特征
        user_fea = ''
        if userid in user_fea_dict:
            user_fea = user_fea_dict[userid]

        u_fea_dict = {}
        for fea_idx in user_fea.strip().split(' '):
            ss = fea_idx.strip().split(':')
            if len(ss) != 2:
                continue
            idx = int(ss[0].strip())
            score = float(ss[1].strip())
            u_fea_dict[idx] = score

        # step 5: 获取物品的特征
        rec_list = []
        for itemid in rec_item_mergeall:
            if itemid in item_fea_dict:
                item_fea = item_fea_dict[itemid]

                i_fea_dict = dict()
                for fea_idx in item_fea.strip().split(' '):
                    ss = fea_idx.strip().split(':')
                    if len(ss) != 2:
                        continue
                    idx = int(ss[0].strip())
                    score = float(ss[1].strip())
                    i_fea_dict[idx] = score

                wx_score = 0.
                # y = wx
                for fea, score in dict(u_fea_dict.items() + i_fea_dict.items()).items():
                    wx_score += (score * model_w_list[fea])

                # sigmoid: 1 / (1 + exp(-wx))
                final_rec_score = 1 / (1 + math.exp(-(wx_score + model_b)))
                rec_list.append((itemid, final_rec_score))

        # step 6 : 排序(rank)
        rec_sort_list = sorted(rec_list, key=lambda x:x[1], reverse=True)

        # step 7 : 过滤(filter)
        rec_fitler_list = rec_sort_list[:10]

        # step 8 : 返回+包装(return)

        item_dict = {}
        with open('../data/name_id.dict', 'r') as fd:
            for line in fd:
                raw_itemid, name = line.strip().split('\t')
                item_dict[raw_itemid] = name

        ret_list = []
        for tup in rec_fitler_list:
            req_item_name = item_dict[req_itemid]
            item_name = item_dict[tup[0]]
            item_rank_score = str(tup[1])
            ret_list.append('   ->   '.join([req_item_name, item_name, item_rank_score]))

        ret = '\n'.join(ret_list)

        return ret

class test:
    def GET(self):
        print web.input()
        return '222'

if __name__ == "__main__":
    app.run()
