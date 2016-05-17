__author__ = 'Xingye Zhang'

import pandas as pd
import numpy as np
import ast
import sklearn
import pickle
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestRegressor

#read the ngram csv file
df = pd.read_csv('ffinal_df.csv')
df.drop(['Unnamed: 0','Unnamed: 0.1'],1, inplace = True)

#change the n_grams from string to dictionay
df['newn_gram'] = df['n_gram'].map(lambda x:ast.literal_eval(x))

#unique legal fields
issuelst = list(set(df.issue))

def featureSelection(df):
    df.reset_index(drop = True, inplace = True)
    X = df['newn_gram']
    v = DictVectorizer(sparse=False) #dictionay to dataframe
    X_test = v.fit_transform(X)
    X_array = X_test.copy()

    #set the numebr of apperance to 1 for each case in order to count
    #the number of articles for a token
    X_array[X_array > 1] = 1

    #if the tokens appear no more than 1 percent of the number of articles in
    #this legal field, we delete them.
    a = np.where( X_array.sum(axis=0) > int(0.01*len(df)))
    fea_index = a[0]
    fea_name = np.asarray(v.get_feature_names())[fea_index]
    fea_matrix = X_test[:, fea_index]
    newdf = pd.DataFrame(fea_matrix, columns = fea_name)
    y = df['panelvote']
    X = newdf
    names = fea_name.tolist()
    rf = RandomForestRegressor()
    rf.fit(X, y)
    fealst = zip(map(lambda x: round(x, 4), rf.feature_importances_), names)

    #By using RandomForest, we delete the tokens with score 0.
    impfealst = [fea[1] for fea in fealst if fea[0] > 0]
    impdf = newdf[impfealst]
    impdf['panelvote'] = df['panelvote']
    impdf['issue'] = df['issue']
    impdf['field'] = df['field']
    legalfield = impdf['field'].tolist()[0].replace('/','')
    impdf.to_csv('./field/' + legalfield + '.csv', index = False)

#get the final dataframe for 16 different legal fields.
for issue in issuelst:
    testdf = df[df['issue'] == issue]
    featureSelection(testdf)