from collections import defaultdict
from columns import words
import json
def createworddate():
    datewords = defaultdict(list)
    search = set(words())
    with open('news.json') as f:
        for jsonObj in f:
            cur = json.loads(jsonObj)
            if cur['category'] not in set(['BUSINESS','TECH','POLITICS']):
                continue
            title = cur['headline'].lower()
            desc = cur['short_description'].lower()
            wordlist = title.split() + desc.split()
            for word in wordlist:
                if word.lower() in search:
                    datewords[cur['date']].append(word.lower())
    return datewords
                