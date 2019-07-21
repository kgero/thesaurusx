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


# issue where it doesn't strip line breaks?
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
                words = line.strip('\n').split(' ')
                if self.strip_pos:
                    words = [w.split('_')[0] for w in words]
                yield [w for w in words if w not in ['', '\n']]

name = 'gothic'
data = 'dat/corpora_lemma/' + name

word_cnt = 0
for fname in os.listdir(data):
    for lne in open(os.path.join(data, fname), errors='ignore'):
        word_cnt += len(lne.split(' '))
print(name, ":", word_cnt, 'words')


# defaults in gensim model:
# size=100, window=5, min_count=5, iter=5,
# should i be removing stop words?
for i in range(1):
    outfile = 'dat/vecs/{}_pos_{}.txt'.format(name, i)
    print(outfile)
    start = time()
    sentences = MySentences_lemma(data, strip_pos=False)  # a memory-friendly iterator
    model = gensim.models.Word2Vec(sentences, size=100, window=5, min_count=10)
    model.wv.save_word2vec_format(outfile)
    print("took {:<2f} seconds".format(time() - start))
