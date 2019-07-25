"""
Functions for doing simply thesaurus + style look-ups.
"""

import os
import pickle

from annoy import AnnoyIndex


# ASSUMES ALL EMBEDDINGS ARE 100 DIMENSION!!
DIM = 100
print('Loading embeddings from dat/annoy directory...')
EMB_nms = []
EMB_lem = {}
EMB_pos = {}
VOC = {}
for filename in os.listdir('dat/annoy'):
    extension = filename.split('.')[-1]
    name = filename.split('.')[0]
    if extension == 'ann':
        if name.split('_')[-1] == 'lemma':
            u = AnnoyIndex(DIM)
            u.load(os.path.join('dat/annoy', filename))
            EMB_lem[name] = u
            EMB_nms.append(name)
        elif name.split('_')[-1] == 'pos':
            u = AnnoyIndex(DIM)
            u.load(os.path.join('dat/annoy', filename))
            EMB_pos[name] = u
            EMB_nms.append(name)

for filename in os.listdir('dat/annoy'):
    extension = filename.split('.')[-1]
    name = filename.split('.')[0]
    if extension == 'pkl' and name in EMB_nms:
        VOC[name] = pickle.load(open(os.path.join('dat/annoy', filename), 'rb'))
print('EMB_lem:\n', EMB_lem.keys())
print('EMB_pos:\n', EMB_pos.keys())
print('EMB_nms:\n', EMB_nms)
print('VOCAB:\n', VOC.keys())
print('Ready!\n\n')


# ALL_POS = ['PRON', 'VERB', 'ADJ', 'NOUN', 'PROPN', 'PART', 'DET', 'ADP', 'CCONJ', 'X', 'NUM']
ALL_POS = ['PRON', 'VERB', 'ADJ', 'NOUN', 'PART', 'DET', 'ADP']



def get_pos(word, vocab):
    """Return list of all possible parts of speech of word."""
    possible = []
    for pos in ALL_POS:
        if word+'_'+pos in vocab:
            possible.append(pos)
    return possible

def get_pos_words(keyword_pos, vocab, vectors):
    """Return top 10 words with same pos as keyword.

    keywork_pos is str in form word_POS."""
    pos = keyword_pos.split('_')[-1]
    keyidx = vocab.index(keyword_pos)
    raw = [vocab[idx] for idx in vectors.get_nns_by_item(keyidx, 50)]
    return [w.split('_')[0] for w in raw if w.split('_')[-1] == pos]

def simple_lookup(keyword, embkey="arxiv_abs_lemma"):
    """Return words from thesaurus lookup, ordered by embedding distance."""
    if embkey not in EMB_nms:
        return {'error': '{} not a valid embkey.'.format(keyword)}

    vocab = VOC[embkey]
    
    data = {}
    if embkey in EMB_pos:
        vectors = EMB_pos[embkey]
        possible_pos = get_pos(keyword, vocab)
        if not possible_pos:
            return {'error': '{} not in embeddings.'.format(keyword)}
        data['pos'] = True
        results = {}
        for pos in possible_pos:
            raw = get_pos_words(keyword+'_'+pos, vocab, vectors)
            if len(raw) > 3:
                results[keyword+'_'+pos] = raw[1:11]
        data['results'] = results
    else:
        if keyword not in vocab:
            return {'error': '{} not in embeddings.'.format(keyword)}
        vectors = EMB_lem[embkey]
        data['pos'] = False
        keyidx = vocab.index(keyword)
        raw = [vocab[idx] for idx in vectors.get_nns_by_item(keyidx, 10)]
        data['results'] = {keyword: raw[1:]}

    return data

def thesaurus_lookup(keyword):
    """Return list of all words from a thesaurus lookup."""

    results = {}
    with open('dat/thes/mac_thes.txt', 'r') as fle:
        for line in fle:
            if line.split(' ')[0] == keyword:
                line = line.strip('\n')
                entry, words = line.split(':')
                pos = entry.split(' ')[1]
                results[keyword+'_'+pos.upper()] = words.split(', ')
    return {'embd': 'rogets', 'pos': True, 'results': results}
