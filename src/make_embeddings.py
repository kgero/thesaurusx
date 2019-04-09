"""
Creates word embedding from text files in dat/corpora/name directory.
Saves word embedding as .txt in dat/vecs/name.txt
"""
import os
import string
from time import time
import gensim


table = str.maketrans({key: None for key in string.punctuation})   

class MySentences(object):
    """Return one sentence/line, stripped of punctuation and split at spaces.

    :param object: path to directory of text files.
    """
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname), errors='ignore'):
                clean = line.lower().translate(table)
                yield clean.split()

class MySentences_lemma(object):
    """Return one sentence/line, split at spaces.

    :param object: path to directory of text files.
    :param strip_pos: if true, remove part-of-speech tags which occur after _.
    """
    def __init__(self, dirname, strip_pos=True):
        self.dirname = dirname
        self.strip_pos = strip_pos

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname), errors='ignore'):
                words = line.split(' ')
                if self.strip_pos:
                    words = [w.split('_')[0] for w in words]
                yield [w for w in words if w not in ['', '\n']]

name = 'arxiv_abs'
data = 'dat/corpora/' + name

word_cnt = 0
for fname in os.listdir(data):
    for lne in open(os.path.join(data, fname), errors='ignore'):
        word_cnt += len(lne.split(' '))
print(name, ":", word_cnt, 'words')


for i in range(3):
    print('dat/vecs/{}_lemma_{}.txt'.format(name, i))
    start = time()
    sentences = MySentences(data)  # a memory-friendly iterator
    model = gensim.models.Word2Vec(sentences, size=100, window=5)
    model.wv.save_word2vec_format('dat/vecs/{}_{}.txt'.format(name, i))
    print("took {:<2f} seconds".format(time() - start))
