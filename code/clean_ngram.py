#this code will extract the case_id and n_gram fata from docvec_text data Sida Muhe
import sys
import pickle

def transform(values):
    word_dict = {}
    values = values.strip("\ '()\"").split('||')
    for i in range(len(values)):
        word_id, count = values[i].split(':')
        
        word_dict[word_id] = count
    return word_dict

target_list = pickle.load( open( "target_caseid.p", "rb" ) )

for line in sys.stdin:
    line = line.strip('\r\n')
    
    keys = line.split(',')[0]
    case_id = keys.strip("\ '()\"").split('||')[0]
    
    if case_id in target_list:
        
        values = line.split(',')[-1]
        ngram_info = transform(values)
        
        print '%s\t%s' % (case_id, ngram_info)