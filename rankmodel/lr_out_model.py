import numpy as np

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

def load_data():
    inputdata = datasets.load_iris()

    x_train, x_test, y_train, y_test = \
        train_test_split(inputdata.data, inputdata.target, test_size = 0.2, random_state=0)
    return x_train, x_test, y_train, y_test

def main():
    x_train, x_test, y_train, y_test = load_data()
    model = LogisticRegression(penalty='l2')
    model.fit(x_train, y_train)

    ff_w = open('model.w', 'w')
    ff_b = open('model.b', 'w')

    for w_list in model.coef_:
        for w in w_list:
            print >> ff_w, "w: ", w

    for b in model.intercept_:
        print >> ff_b, "b: ", b

    # print "w: ", model.coef_
    # print "b: ", model.intercept_
    print "precision: ", model.score(x_test, y_test)
    print "MSE: ", np.mean((model.predict(x_test) - y_test) ** 2)

if __name__ == '__main__':
    main()
