# Modeling
# Author: Sida Ye, Muhe Xie

import math
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from pandas import Series, DataFrame
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import svm, linear_model
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import confusion_matrix
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn import cross_validation
import os
import operator
import pickle
from ast import literal_eval


### helper function
"""
This function is going to get top k word features with its corresponding
coefficients.

Input: list of coefficients
Return: top k words with its coefficients
"""

def get_top_k(origin_list,k):    
    modified_list = []
    for i in range(len(origin_list)):
        modified_list.append((i,origin_list[i]))

    sorted_by_second = sorted(modified_list, key=lambda tup: tup[1],reverse=True)
    positive_part = sorted_by_second[:k]
    negative_part = sorted_by_second[-k:]
    positive_part_index = {}
    negative_part_index={}
    for i,item in enumerate(positive_part):
        positive_part_index[item[0]] = sorted_by_second[i][1]
    for item in negative_part:
        negative_part_index[item[0]] = sorted_by_second[::-1][i][1]
    return positive_part_index,negative_part_index

"""
This function is going to get top k word features

Input: list of coefficients
Return: top k words WITHOUT its coefficients
"""

def get_top_k_nocoeff(origin_list,k):
    modified_list = []
    for i in range(len(origin_list)):
        modified_list.append((i, origin_list[i]))

    sorted_by_second = sorted(modified_list, key=lambda tup: tup[1], reverse=True)
    positive_part = sorted_by_second[:k]
    negative_part = sorted_by_second[-k:]
    positive_part_index = []
    negative_part_index = []
    for item in positive_part:
        positive_part_index.append(item[0])
    for item in negative_part:
        negative_part_index.append(item[0])
    return positive_part_index, negative_part_index[::-1]
"""
Plot AUC graph
"""

def plotAUC(truth, pred, lab):
    fpr, tpr, thresholds = roc_curve(truth, pred)
    roc_auc = auc(fpr, tpr)
    c = (np.random.rand(), np.random.rand(), np.random.rand())
    plt.plot(fpr, tpr, color=c, label=lab+' (AUC = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.xlabel('FPR')
    plt.ylabel('TPR')
    plt.title('ROC')
    plt.legend(loc="lower right")

"""
This function helps to automatically build model on different legal fiedls.
It will print AUC for each legal field.

Input: file_name, k(integar), weight=True/False (With coeff or not)
Return: A list of n-gram index. So, each field will have two lists.
One is for positive and another is for negative.

Note: If there is any overlap
"""

def LR_modeling(file_name, k, AUC=True, weight=False):
    raw_data = pd.read_csv(file_name)
    raw_data = raw_data.drop(['issue', 'field'], axis=1)
    X = raw_data.drop('panelvote', axis=1)
    y = raw_data['panelvote']
    tfidf = TfidfTransformer(norm=u'l2', use_idf=True, smooth_idf=True, sublinear_tf=False)
    X = tfidf.fit_transform(X.values)
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.8, random_state=42)
    lr = LogisticRegression(C=1)
    lr.fit(X_train, y_train)
    auc = np.mean(cross_validation.cross_val_score(lr, X, y, scoring="roc_auc"))
    if AUC == True:
        print "AUC for %s on the test data = %.3f" % (file_name, auc)
    if weight == False:
        top_positive, top_negative = get_top_k_nocoeff(lr.coef_[0], k)
        return raw_data.columns[top_positive], raw_data.columns[top_negative]
    else:
        top_positive, top_negative = get_top_k(lr.coef_[0], k)
        final_pos = {}
        final_neg = {}
        for i in top_positive.keys():
            final_pos[raw_data.columns[i]] = top_positive[i]
        for j in top_negative.keys():
            final_neg[raw_data.columns[j]] = top_negative[j]
        pos = sorted(final_pos.items(), key=operator.itemgetter(1), reverse=True)
        neg = sorted(final_neg.items(), key=operator.itemgetter(1))
        return pos, neg

def main():
    # list all file names under field directory, you can be modified it.
    files = os.listdir('field')

    # get target word id list
    result = []
    for f in files:
        result.append(LR_modeling('field/' + f, 30, AUC=False))
    newlist = []
    for i in range(len(result)):
        for item in result[i][0]:
            newlist.append(item)
        for item in result[i][1]:
            newlist.append(item)
    print "There are {} words".format(len(newlist))
    pickle.dump(newlist, open("word_id_list.p", "wb"))
    print "Save word id list in 'word_id_list.p' file"


if __name__ == '__main__':
    main()
