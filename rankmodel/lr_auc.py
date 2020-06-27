#coding=utf8
import sys
import numpy as np
from scipy.sparse import csr_matrix

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

data_in = sys.argv[1]

def load_data():
    target_list = []
    fea_row_list = []
    fea_col_list = []
    data_list = []

    row_idx = 0
    max_col = 0

    with open(data_in, 'r') as fd:
        for line in fd:
            ss = line.strip().split(' ')
            label = ss[0]
            fea = ss[1:]

            target_list.append(int(label))

            for fea_score in fea:
                sss = fea_score.strip().split(':')
                if len(sss) != 2:
                    continue
                feature, score = sss

                fea_row_list.append(row_idx)
                fea_col_list.append(int(feature))
                data_list.append(float(score))
                if int(feature) > max_col:
                    max_col = int(feature)

            row_idx += 1

    row = np.array(fea_row_list)
    col = np.array(fea_col_list)
    data = np.array(data_list)

    fea_datasets = csr_matrix((data, (row, col)), shape=(row_idx, max_col + 1))

    x_train, x_test, y_train, y_test = train_test_split(fea_datasets, target_list, test_size=0.2, random_state=0)
    return x_train, x_test, y_train, y_test

# def load_data():
#     inputdata = datasets.load_iris()
#
#     x_train, x_test, y_train, y_test = \
#         train_test_split(inputdata.data, inputdata.target, test_size = 0.2, random_state=0)
#     return x_train, x_test, y_train, y_test

def main():
    x_train, x_test, y_train, y_test = load_data()
    model = LogisticRegression(penalty='l1')
    model.fit(x_train, y_train)

    ff_t = open('T.txt', 'w')
    ff_p = open('P.txt', 'w')

    #for b in model.intercept_:
        #print >> ff_b, "b: ", b

    # print "w: ", model.coef_
    # print "b: ", model.intercept_
    #print "precision: ", model.score(x_test, y_test)
    #print "MSE: ", np.mean((model.predict(x_test) - y_test) ** 2)

    #print y_test, model.predict(x_test)

    # 输出真实label和预测label，到两个不同的文件中
    for y in y_test:
        print >> ff_t, y

    for y in model.predict_proba(x_test):
        print >> ff_p, y


if __name__ == '__main__':
    main()
