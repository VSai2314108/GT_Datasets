import pandas as pd
def words():
    words = pd.read_csv('key_word.csv') 
    words = words[['Word']]
    words = words.values.tolist()
    add = []
    for word in words:
        add.append(word[0])
    return add
        
def columns():
    columns = [ 'DATE','INDEX', 'VIX', 'SPY', 'COMM', 'CD', 'CS','ENER', 'FIN', 'HEAL', 'IND', 'MAT', 'RE', 'TECH', 'UTIL']
    add = words()
    # columns+=add
    return columns
columns() 
    