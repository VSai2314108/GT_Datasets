import csv
import pandas as pd
from columns import columns
from worddate import createworddate
# [ 'DATE','INDEX', 'VIX', 'SPY', 'COMM', 'CD', 'CS','ENER', 'FIN', 'HEAL', 'IND', 'MAT', 'RE', 'TECH', 'UTIL']
def createdataset():
    cols = columns()
    df = pd.DataFrame(columns=cols)
    vix = pd.read_csv('vix.csv')
    
    myrows = {}
    # create dict based on VIX
    vix = vix[['Date','Close']]
    vixlist = vix.values.tolist()
    ind = 0
    for elem in vixlist:
        myrows[elem[0]] = {'DATE': elem[0],'INDEX': ind, 'VIX': elem[1]}
        ind+=1
    
    # add the rest of the values
    ind = 3
    for name in ['spy.csv', 'communication.csv', 'consumer discretionary.csv', 'consumer staple.csv', 'energy.csv', 'financial.csv', 'health.csv', 'industrials.csv', 'materials.csv', 'real estate.csv', 'technology.csv', 'utilities.csv']:
        cur = pd.read_csv(name)
        cur = cur[['Date', 'Close']]
        curlist = cur.values.tolist()
        for elem in curlist: 
            if elem[0] in myrows:
                myrows[elem[0]][cols[ind]] = elem[1]
        ind+=1
    
    out = pd.DataFrame(myrows.values())
    out.to_csv('dataset.csv', index=False)
    
        
    
        
createdataset()