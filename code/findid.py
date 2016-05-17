#this function will find the actual n-gram whose id in the target list
import sys
import pickle

target_list = pickle.load( open( "target_caseid.p", "rb" ) )




for line in sys.stdin:
    line = line.strip('\r\n')
    linelist = line.split(',')
    idtmp = linelist[-1]
    idstr = idtmp.strip(' \)')
    
    if idstr in target_list:
    	print line


