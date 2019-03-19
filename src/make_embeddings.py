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
    def __init__(self, dirname):
        self.dirname = dirname

# for one sentence per line
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname), errors='ignore'):
                clean = line.lower().translate(table)
                yield clean.split()

name = 'merge-science-small'
data = 'dat/corpora/' + name

words = 0
for fname in os.listdir(data):
    for line in open(os.path.join(data, fname), errors='ignore'):
        words += len(line.split(' '))
print(name, ":", words, 'words')

start = time()
sentences = MySentences(data)  # a memory-friendly iterator
model = gensim.models.Word2Vec(sentences, size=100, window=5)
model.wv.save_word2vec_format('dat/vecs/{}.txt'.format(name))
print("took {:<2f} seconds".format(time() - start))
