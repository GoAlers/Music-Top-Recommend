import sys

for line in sys.stdin:
    ss = line.strip().split('\t')
    if len(ss) != 3:
        continue
    music_id = ss[0].strip()
    music_name = ss[1].strip()
    fea_l = ss[2].strip()


    tmp_list = []
    for fs_tuple_str in fea_l.split(''):
        fea, score = fs_tuple_str.split('')
        tmp_list.append((fea, score))

    for tu in tmp_list:
        #print '\t'.join([music_name, tu[0], str(tu[1])])
        print '\t'.join([tu[0], music_name, str(tu[1])])


