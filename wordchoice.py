import json
from collections import defaultdict
import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
def keywordbydate():
    dataset = []
    with open('news.json') as f:
        for jsonObj in f:
            cur = json.loads(jsonObj)
            if cur['category'] not in set(['BUSINESS','TECH','POLITICS']):
                continue
            title = cur['headline'].lower()
            desc = cur['short_description'].lower()
            words = title + ' ' + desc
            dataset.append(words)
    new = True
    out = None
    for ind in range(0,len(dataset)-4000,4000):
        tfIdfTransformer = TfidfTransformer(use_idf=True)
        countVectorizer = CountVectorizer(dtype=np.float64)
        wordCount = countVectorizer.fit_transform(dataset[ind:ind+100])
        newTfIdf = tfIdfTransformer.fit_transform(wordCount)
        if new:
            out = pd.DataFrame(newTfIdf[0].T.todense(), index=countVectorizer.get_feature_names(), columns=["TF-IDF"])
            new = False
        else:
            out = pd.concat([out, pd.DataFrame(newTfIdf[0].T.todense(), index=countVectorizer.get_feature_names(), columns=["TF-IDF"])])
    out = out.sort_values('TF-IDF', ascending=False)
    out.to_csv('file_name.csv')

    
    
keywordbydate()

            
        




