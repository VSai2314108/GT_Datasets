import pandas as pd
import random
def aggregatewc(b,e):
    df = pd.read_csv('datasetwords.csv')
    labels = df.columns[15:]
    df = df[b:e]
    df = df.sum(axis = 0)
    df = df[15:]
    # out = df.values.tolist()
    df = df.to_list()
    out = []
    for ind,elem in enumerate(df):
        if elem != 0:
            add = {}
            add['text'] = labels[ind]
            add['value'] =int(10*(elem+(elem*(random.random()))))
            out.append(add)
    return out
        
        
        
    

print(aggregatewc(0,90)) 
    
    