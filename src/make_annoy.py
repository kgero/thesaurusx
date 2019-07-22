"""Create version of embeddings that is very quick to load."""

import argparse
import pickle
import os
import sys

from time import time
from annoy import AnnoyIndex


def make_ann(filename, emb_nm):
    print(f'making annoy version of {filename}')
    vocab = []

    with open(filename, 'r') as fle:
        sz, dim = [int(num) for num in fle.readline().split(' ')]
        print('vocab: {} dim: {}'.format(sz, dim))

        t = AnnoyIndex(dim)
        i = 0
        for line in fle:
            word = line.split(' ')[0]
            vec = [float(num) for num in line.strip('\n').strip(' ').split(' ')[1:]]
            vocab.append(word)
            t.add_item(i, vec)
            i += 1

    start = time()
    t.build(10)
    print('time to build:', time() - start)
    t.save('dat/annoy/{}.ann'.format(emb_nm))
    pickle.dump(vocab, open('dat/annoy/{}.v.pkl'.format(emb_nm), 'wb'))

    key = 50
    print([vocab[idx] for idx in t.get_nns_by_item(key, 10)])
    print('\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename',
                        help=('The name of embedding file (incl .txt extension).  '
                              'Should be in the /dat/vecs directory.'))
    args = parser.parse_args()

    fname = os.path.join('dat/vecs', args.filename)

    if not os.path.exists(fname):
        print(f"Embedding file {fname} doesn't exist.")
        sys.exit()

    name = args.filename[:-4]

    make_ann(fname, name)
