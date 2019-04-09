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
import spacy

from annoy import AnnoyIndex

nlp = spacy.load('en_core_web_sm')

# ASSUMES ALL EMBEDDINGS ARE 100 DIMENSION!!
DIM = 100
print('Loading embeddings from dat/annoy directory...')
EMB = {}
VOC = {}
for filename in os.listdir('dat/annoy'):
    if filename.split('.')[-1] == 'ann':
        name = filename.split('.')[0]
        if name == 'word2vec-slim':
            u = AnnoyIndex(300)
        else:
            u = AnnoyIndex(DIM)
        u.load(os.path.join('dat/annoy', filename))
        EMB[name] = u
    if filename.split('.')[-1] == 'pkl':
        name = filename.split('.')[0]
        VOC[name] = pickle.load(open(os.path.join('dat/annoy', filename), 'rb'))
POS = {}
for filename in os.listdir('dat/pos'):
    if filename.split('.')[-1] == 'pkl':
        name = filename.split('.')[0]
        POS[name] = pickle.load(open(os.path.join('dat/pos', filename), 'rb'))
print('EMBEDDINGS:\n', EMB.keys())
print('VOCAB:\n', VOC.keys())
print('PART OF SPEECH:\n', POS.keys())
print('Ready!\n\n')


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
    for pos_key in POS:
        if word in POS[pos_key]:
            pos += POS[pos_key][word]
    return list(set(pos))

def get_lemma(word):
    """Return lemma of word."""
    doc = nlp(word)
    for token in doc:
        return token.lemma_

def simple_lookup(keyword, pos, embkey="glove.6B.200d"):
    """Return words from thesaurus lookup, ordered by embedding distance."""
    vectors = EMB[embkey]
    vocab = VOC[embkey]
    if keyword not in vocab:
        return {'error': '{} not in embeddings.'.format(keyword)}

    keyidx = vocab.index(keyword)
    # words = [w for w in thesaurus_lookup(keyword, pos) if w in vocab]
    # dist = []
    # for w in words:
    #     dist.append(vectors.get_distance(keyidx, vocab.index(w)))
    # order = np.argsort(dist)

    raw = [vocab[idx] for idx in vectors.get_nns_by_item(keyidx, 50)]
    note = ''
    if embkey in POS.keys():
        raw = [word for word in raw if POS[embkey].get(word) is not None]
        raw = [get_lemma(word) for word in raw if pos in POS[embkey][word]]
        raw = [word for word in raw if word != get_lemma(keyword)]
        seen = set()
        seen_add = seen.add
        raw = [x for x in raw if not (x in seen or seen_add(x))]
        note = '(returning only {} words from {})'.format(pos, embkey)
    else:
        raw = [get_lemma(word) for word in raw]
        raw = [word for word in raw if word != get_lemma(keyword)]
        seen = set()
        seen_add = seen.add
        raw = [x for x in raw if not (x in seen or seen_add(x))]
        note = '(no part-of-speech information available.)'

    return {
        # 'closest': [words[i] for i in order][:10],  # muted
        # 'distance': [dist[i] for i in order],
        'words': raw[1:11],  # first
        'note': note
        }

def get_vocab(embkey):
    return VOC[embkey]

def thesaurus_lookup(keyword, pos):
    """Return list of all words from a thesaurus lookup with pos in tags."""
    payload = {'ml': keyword, 'max': 1000}
    r = requests.get('https://api.datamuse.com/words', params=payload)
    wellformed = [d for d in r.json() if d.get('tags') is not None]
    return [d["word"] for d in wellformed if pos in d.get('tags')]
