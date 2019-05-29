"""
Functions for doing simply thesaurus + style look-ups.
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
    if filename.split('.')[0] in ['arxiv_abs_pos']:
        if filename.split('.')[-1] == 'ann':
            name = filename.split('.')[0]
            u = AnnoyIndex(DIM)
            u.load(os.path.join('dat/annoy', filename))
            EMB[name] = u
        if filename.split('.')[-1] == 'pkl':
            name = filename.split('.')[0]
            VOC[name] = pickle.load(open(os.path.join('dat/annoy', filename), 'rb'))
print('EMBEDDINGS:\n', EMB.keys())
print('VOCAB:\n', VOC.keys())
print('Ready!\n\n')

ALL_POS = ['PRON', 'VERB', 'ADJ', 'NOUN', 'PROPN', 'PART', 'DET', 'ADP', 'CCONJ', 'X', 'NUM']


def get_pos(word, vocab):
    """Return list of all possible parts of speech of word."""
    possible = []
    for pos in ALL_POS:
        print(word+'_'+pos)
        if word+'_'+pos in vocab:
            possible.append(pos)
    return possible

def get_lemma(word):
    """Return lemma of word."""
    doc = nlp(word)
    for token in doc:
        return token.lemma_

def real_simple_lookup(keyword, embkey, n=5):
    keyword = keyword.strip(',.;:').lower()
    keyword = get_lemma(keyword)
    vectors = EMB[embkey]
    vocab = VOC[embkey]
    possible_pos = get_pos(keyword, vocab)
    if not possible_pos:
        return {'error': '{} not in embeddings.'.format(keyword)}

    data = {'word': keyword, 'results': {}}
    for pos in possible_pos:
        key = keyword + '_' + pos
        keyidx = vocab.index(key)
        raw = [vocab[idx] for idx in vectors.get_nns_by_item(keyidx, n, search_k=100)[1:]]
        match = [w.split('_')[0] for w in raw if w.split('_')[1] == pos]
        data['results'][pos] = match

    return data

def get_vocab(embkey):
    return VOC[embkey]
