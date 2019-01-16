"""
Functions for doing simply thesaurus + style look-ups.

Details on pymagnitude, a fast interface for word vectors:
https://github.com/plasticityai/magnitude
"""
import json
import numpy as np
import requests

from pymagnitude import Magnitude
from sklearn.decomposition import PCA



print('loading embeddings...')
emb = {
    "glove-6B-200d": Magnitude("dat/glove-6B-200d.magnitude"),
    "glove-twitter-27B-50d": Magnitude("dat/glove-twitter-27B-50d.magnitude"),
    "GoogleNews-vectors-negative300": Magnitude("dat/GoogleNews-vectors-negative300.magnitude"),
    "food": Magnitude("dat/food.magnitude"),
    "poetry": Magnitude("dat/poetry.magnitude"),
    "sherlock": Magnitude("dat/sherlock.magnitude"),
    "joyce": Magnitude("dat/joyce.magnitude"),
    "darwin": Magnitude("dat/darwin.magnitude"),
    "dickens": Magnitude("dat/dickens.magnitude")
}
print('ready!')

rand_words = [
    ('elephant', 'tortoise'),
    ('hoop', 'basketball'),
    ('girl', 'boy'),
    ('tender', 'faces'),
    ('hysterical', 'light')
]

def warm_up():
    """Do a series of queries across all embeddings to warm them up."""
    for key in emb:
        vectors = emb[key]
        for w1, w2 in rand_words:
            vectors.most_similar(positive=[w1], negative=[w2])
            vectors.most_similar(positive=[w1, w2])


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

    # also just get the words closest based on the embedding
    print([w for w, d in vectors.most_similar(keyword, topn=10)])

    return {
        'words': [words[i] for i in order],
        'distance': [dist[i].item() for i in order],
        'closest': [w for w, d in vectors.most_similar(keyword, topn=10)]
        }

def analogy_lookup(keyword, base, goal, n=10, embkey="glove.6B.200d"):
    """Return list of top n words of an analogy lookup, and list of distances.

    base is to goal as keyword is to ???
    """
    vectors = emb[embkey]
    if base and goal:
        res = vectors.most_similar(positive=[keyword, goal], negative=[base], topn=n)
    elif base:
        res = vectors.most_similar(positive=[keyword], negative=[base], topn=n)
    elif goal:
        res = vectors.most_similar(positive=[keyword, goal], topn=n)
    else:
        res = vectors.most_similar(positive=[keyword], topn=n)
    return [text for text, dist in res], [dist.item() for text, dist in res]

def analogy_lookup_wthes(keyword, base, goal, n=10, embkey="glove.6B.200d"):
    """Return list of top n words of an analogy lookup, and list of distances.

    Only return works from a thesaurus lookup.

    base is to goal as keyword is to ???
    """
    words = thesaurus_lookup(keyword)
    vectors = emb[embkey]
    if base and goal:
        loc = vectors.query(keyword) + vectors.query(goal) - vectors.query(base)
    elif base:
        loc = vectors.query(keyword) - vectors.query(base)
    elif goal:
        loc = vectors.query(keyword) + vectors.query(goal)
    else:
        loc = vectors.query(keyword)
    dist = []
    for w in words:
        dist.append(vectors.distance(loc, w))
    order = np.argsort(dist)
    return {'words': [words[i] for i in order], 'distance': [dist[i].item() for i in order]}

def thesaurus_lookup(keyword):
    """Return list of all words from a thesaurus lookup."""
    payload = {'ml': keyword, 'max': 1000}
    r = requests.get('https://api.datamuse.com/words', params=payload)
    return [d["word"] for d in r.json()]

def pca_lookup(keyword, style_words, embkey="glove.6B.200d"):
    """Return data from thesaurus lookup ordered by style_words.

    Args:
    keyword - str, word to lookup
    style_words - list of str, words to define style

    Return:
    data - {
      'components': list of explained variance per component
      'words': list of ordered words
      'range': range of PCA projection of words
    }
    """
    if len(style_words) == 1 and style_words[0] == '':
        return analogy_lookup_wthes(keyword, '', '', embkey=embkey)
    # create PCA from style_words
    vectors = emb[embkey]
    matrix = []
    style_words = [w for w in style_words if w in vectors]
    for w in style_words:
        matrix.append(vectors.query(w) - vectors.query('the'))
    matrix = np.array(matrix)
    num_c = min(10, len(style_words))
    pca = PCA(n_components=num_c)
    pca.fit(matrix)

    closest = [w for w in thesaurus_lookup(keyword) if w in vectors]
    test_vec = [vectors.query(w) for w in closest]
    proj = pca.transform(test_vec)[:, 0]
    res = []
    for i in np.argsort(proj)[::-1]:
        res.append((closest[i], proj[i]))

    com = [ratio.item() for ratio in pca.explained_variance_ratio_]
    data = {
        'components': com,
        'words': [w for w, d in res],
        'range': (max(proj) - min(proj)).item()
    }
    return data
