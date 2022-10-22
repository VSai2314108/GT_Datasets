import csv
import pandas as pd
from columns import columns, words
from worddate import createworddate
# [ 'DATE','INDEX', 'VIX', 'SPY', 'COMM', 'CD', 'CS','ENER', 'FIN', 'HEAL', 'IND', 'MAT', 'RE', 'TECH', 'UTIL']
def createdataset():
    cols = columns()
    keywords = set(words())
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
    
    # fill in empty sectors
    for elem in myrows:
        missing = set([ 'DATE','INDEX', 'VIX', 'SPY', 'COMM', 'CD', 'CS','ENER', 'FIN', 'HEAL', 'IND', 'MAT', 'RE', 'TECH', 'UTIL']).difference(set(myrows[elem].keys()))
        for mis in missing:
            myrows[elem][mis] = 0        

    # add words 
    worddate = createworddate()
    for day in myrows:
        todayword = set([])
        if day in myrows:
            todayword = set(worddate[day])
        for word in keywords:
            if word in todayword:
                myrows[day][word] = '1'
            else:
                myrows[day][word] = '0'
    
    out = pd.DataFrame(myrows.values())
    out.to_csv('datasetwords.csv', index=False)
    
        
    
        
createdataset()