"""Create dict for each corpus of words and possible part of speech tags."""

import pickle
import os
import spacy



nlp = spacy.load('en_core_web_sm')


def get_lemma(token):
    if token.lemma_ == '-PRON-':
        return token.text.lower()
    return token.lemma_.replace('_', '-')

def make_lemma_file(filepath, outpath):
    """Rewrite text file at filepath with every word as lemma_pos."""
    with open(filepath, 'r') as flein, open(outpath, 'w') as fleout:
        for line in flein:
            doc = nlp(line.strip('\n'))
            for sent in doc.sents:
                word_tokens = [t for t in sent if t.pos_ not in ['PUNCT', 'SPACE']]
                lemmas = [get_lemma(t) for t in word_tokens]
                newwords = [l + '_' + t.pos_ for t, l in zip(word_tokens, lemmas)]
                fleout.write(' '.join(newwords) + '\n')

def make_lemma_corpus(name, basepath='dat/corpora/', outpath='dat/corpora_lemma/'):
    """Rewrite all txt files in basepath/name as lemma txt files in outpath/name."""
    basepath = os.path.join(basepath, name)
    outpath = os.path.join(outpath, name)
    if not os.path.exists(outpath):
        os.mkdir(outpath)

    finished = os.listdir(outpath)
    for filename in os.listdir(basepath):
        if filename[0] == '.' or filename in finished:
            print('skipping', filename)
            continue
        print(filename)
        flein = os.path.join(basepath, filename)
        fleout = os.path.join(outpath, filename)
        make_lemma_file(flein, fleout)

# doc = nlp(u"--I'd give you such a belt in a second.")
# for token in doc:
#     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#           token.shape_, token.is_alpha, token.is_stop)

make_lemma_corpus('scifi')
