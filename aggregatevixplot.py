import pandas as pd
from aggregatewordcount import aggregatewc
def aggregatevixplot():
    final = {}
    df = pd.read_csv('vix.csv')
    df = df[['Date','Close']]
    out = df.values.tolist()
    for ind,elem in enumerate(out[91:]):
        add = {}
        add['Date'] = elem[0]
        add['VIX'] = elem[1]
        add['Count'] = aggregatewc(ind,ind+90)
        final[elem[0]] = add
    import json
    with open('vix_word_list.json', 'w') as fp:
        json.dump(final,fp)
        
        
    
    
    
        
    
    
    
aggregatevixplot()
    