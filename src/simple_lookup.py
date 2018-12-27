"""
Functions for doing simply thesaurus + style look-ups.

Details on pymagnitude, a fast interface for word vectors:
https://github.com/plasticityai/magnitude
"""
from pymagnitude import Magnitude



print('loading embeddings...')
emb = {
    "glove.6B.200d": Magnitude("dat/glove.6B.200d.magnitude"),
    "glove.twitter.27B.50d": Magnitude("dat/glove.twitter.27B.50d.magnitude"),
    "GoogleNews-vectors-negative300": Magnitude("dat/GoogleNews-vectors-negative300.magnitude")
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

def analogy_lookup(keyword, base, goal, n=10, embkey="glove.6B.200d"):
    """Returns list of top n words of the following analogy lookup:

    base is to goal as keyword is to ???
    """
    vectors = emb[embkey]
    if base and goal:
        res = vectors.most_similar(positive=[keyword, goal], negative=[base])
    elif base:
        res = vectors.most_similar(positive=[keyword], negative=[base])
    elif goal:
        res = vectors.most_similar(positive=[keyword, goal])
    else:
        res = vectors.most_similar(positive=[keyword])
    return [text for text, dist in res]
