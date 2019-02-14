"""
Functions for doing simply thesaurus + style look-ups.

Details on pymagnitude, a fast interface for word vectors:
https://github.com/plasticityai/magnitude
"""
import json
import numpy as np
import os
import requests
import pickle

from annoy import AnnoyIndex
from nltk.corpus import wordnet as wn


# ASSUMES ALL EMBEDDINGS ARE 100 DIMENSION!!
DIM = 100
print('Loading embeddings from dat/annoy directory...')
EMB = {}
VOC = {}
for filename in os.listdir('dat/annoy'):
    if filename.split('.')[-1] == 'ann':
        name = filename.split('.')[0]
        print(name, filename)
        u = AnnoyIndex(DIM)
        u.load(os.path.join('dat/annoy', filename))
        EMB[name] = u
    if filename.split('.')[-1] == 'pkl':
        name = filename.split('.')[0]
        print(name, filename)
        VOC[name] = pickle.load(open(os.path.join('dat/annoy', filename), 'rb'))
print('Ready!')


def check_words(words, embkey="glove.6B.200d"):
    """Return error message is any words not in word embeddings."""
    vocab = VOC[embkey]
    resp = ""
    for w in words:
        if w and w not in vocab:
            resp += '{} not in vocab. '.format(w)
    return resp

def get_pos(word):
    """Return list of all possible parts of speech of word."""
    pos = []
    for ss in wn.synsets(word):
        if ss.pos() == 's':  # synonym
            continue
        elif ss.pos() == 'r':
            pos.append('adv')
        elif ss.pos() == 'a':
            pos.append('adj')
        else:
            pos.append(ss.pos())
    return list(set(pos))

def simple_lookup(keyword, pos, embkey="glove.6B.200d"):
    """Return words from thesaurus lookup, ordered by embedding distance."""
    vectors = EMB[embkey]
    vocab = VOC[embkey]
    if keyword not in vocab:
        return {'error': '{} not in embeddings.'.format(keyword)}

    keyidx = vocab.index(keyword)
    words = [w for w in thesaurus_lookup(keyword, pos) if w in vocab]
    dist = []
    for w in words:
        dist.append(vectors.get_distance(keyidx, vocab.index(w)))
    order = np.argsort(dist)

    raw = [vocab[idx] for idx in vectors.get_nns_by_item(keyidx, 10)]

    return {
        'closest': [words[i] for i in order][:10],  # muted
        'distance': [dist[i] for i in order],
        'words': raw  # first
        }

def thesaurus_lookup(keyword, pos):
    """Return list of all words from a thesaurus lookup with pos in tags."""
    payload = {'ml': keyword, 'max': 1000}
    r = requests.get('https://api.datamuse.com/words', params=payload)
    wellformed = [d for d in r.json() if d.get('tags') is not None]
    return [d["word"] for d in wellformed if pos in d.get('tags')]
