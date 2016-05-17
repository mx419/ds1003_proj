__author__ = 'Xingye Zhang'

import pandas as pd
import os
import numpy as np
import string

#100Votelevel
df1_ = pd.DataFrame(columns = ['caseid', 'citation','Circuit','year','month','day','x_aba', 'x_black', 'x_dem'])
for chk in pd.read_stata('100Votelevel_touse.dta', iterator=True, chunksize = 10000):
    df2_ = chk[['caseid', 'citation','Circuit','year','month','day','x_aba', 'x_black', 'x_dem']]
    df1_ = df1_.append(df2_,ignore_index=True)

df1_.drop_duplicates(inplace=True)

#sunstein_data_for_updating
df3_ = pd.read_csv('sunstein_data_for_updating.csv')
df3_.drop_duplicates('citation',inplace = True)
df3_['citation'].replace('', np.nan, inplace=True)
df3_.dropna(subset=['citation'], inplace=True)

df1_['citationN'] = df1_['citation'].map(lambda x: x.replace('.',''))
df3_['citationN'] = df3_['citation'].map(lambda x: x.replace('.',''))

df3f_ = df3_[['citationN','casename','panelvote','circuit','year','issue']]
df3f_.drop_duplicates('citationN',inplace = True)
init_df = pd.merge(df1_,df3f_,on='citationN')
init_df.drop_duplicates(inplace = True)

target_ngram_df = pd.read_table('target_ngram_df', header = None)
target_ngram_df.columns = ['caseid','ngram']
target_ngram_df.drop_duplicates('caseid', inplace = True)
df_final = pd.merge(target_ngram_df, init_df, on = 'caseid')