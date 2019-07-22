"""
Creates word embedding from text files in dat/corpora/name directory.
Saves word embedding as .txt in dat/vecs/name.txt
"""
import argparse
import os
import string
import sys

import gensim

from time import time


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


def make_emb(datapath, outfile):
    print(outfile)
    start = time()
    sentences = MySentences_lemma(datapath, strip_pos=False)  # a memory-friendly iterator
    model = gensim.models.Word2Vec(sentences, size=100, window=5, min_count=10)
    model.wv.save_word2vec_format(outfile)
    print("took {:<2f} seconds".format(time() - start))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder',
                        help=('The folder containing the input data.  '
                              'Should be in the /dat/corpora_lemma directory.'))
    parser.add_argument('-d', '--duplicates', action='store_true',
                        help=('Flag for creating duplicates of an embedding '
                              'for experimentation purposes.'))
    args = parser.parse_args()

    data = 'dat/corpora_lemma/' + args.folder

    if not os.path.exists(os.path.join('dat/corpora_lemma', args.folder)):
        print(f"Input data folder [dat/corpora_lemma/{args.folder}] doesn't exist.")
        sys.exit()

    if not os.path.exists('dat/vecs'):
        os.mkdir('dat/vecs')

    word_cnt = 0
    for filename in os.listdir(data):
        for lne in open(os.path.join(data, filename), errors='ignore'):
            word_cnt += len(lne.split(' '))
    print(args.folder, ":", word_cnt, 'words')


    # defaults in gensim model:
    # size=100, window=5, min_count=5, iter=5,
    # not currently removing stop words
    if args.duplicates:
        for i in range(5):
            outfile = f'dat/vecs/{args.folder}_pos_{i}.txt'
            make_emb(data, outfile)
    else:
        outfile = f'dat/vecs/{args.folder}_pos.txt'
        make_emb(data, outfile)
