"""
Functions for doing simply thesaurus + style look-ups.

Details on pymagnitude, a fast interface for word vectors:
https://github.com/plasticityai/magnitude
"""
import json
import numpy as np
import os
import requests

from pymagnitude import Magnitude



print('Loading embeddings from dat/ directory...')
emb = {}
for filename in os.listdir('dat'):
    if filename.split('.')[-1] == 'magnitude':
        print(filename)
        emb[filename.split('.')[0]] = Magnitude(os.path.join('dat', filename))
print('Ready!')


def check_words(words, embkey="glove.6B.200d"):
    """Return error message is any words not in word embeddings."""
    vectors = emb[embkey]
    resp = ""
    for w in words:
        if w and w not in vectors:
            resp += '{} not in vocab. '.format(w)
    return resp

def simple_lookup(keyword, embkey="glove.6B.200d"):
    """Return words from thesaurus lookup, ordered by embedding distance."""
    vectors = emb[embkey]
    if keyword not in vectors:
        return {'error': '{} not in embeddings.'.format(keyword)}

    words = [w for w in thesaurus_lookup(keyword) if w in vectors]
    dist = []
    for w in words:
        dist.append(vectors.distance(keyword, w))
    order = np.argsort(dist)

    return {
        'words': [words[i] for i in order],
        'distance': [dist[i].item() for i in order]
        # 'closest': [w for w, d in vectors.most_similar(keyword, topn=10)]
        }

def thesaurus_lookup(keyword):
    """Return list of all words from a thesaurus lookup."""
    payload = {'ml': keyword, 'max': 1000}
    r = requests.get('https://api.datamuse.com/words', params=payload)
    return [d["word"] for d in r.json()]
