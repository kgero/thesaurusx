import argparse
import os
import sys

from src.make_pos import make_lemma_corpus
from src.make_embeddings import make_emb
from src.make_annoy import make_ann



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder',
                        help=('The folder containing the input data.  '
                              'Should be in the /dat/corpora directory.'
                              'Can be multiple text files.'))
    args = parser.parse_args()

    if not os.path.exists(os.path.join('dat/corpora', args.folder)):
        print(f"Input data folder [dat/corpora/{args.folder}] doesn't exist.")
        sys.exit()

    if not os.path.exists('dat/corpora_lemma'):
        os.mkdir('dat/corpora_lemma')

    print("Preparing part-of-speech version of corpus. This can take some time.")
    make_lemma_corpus(args.folder)

    if not os.path.exists('dat/vecs'):
        os.mkdir('dat/vecs')

    print("Creating word embedding. Should be pretty fast.")

    data = 'dat/corpora_lemma/' + args.folder
    word_cnt = 0
    for filename in os.listdir(data):
        for lne in open(os.path.join(data, filename), errors='ignore'):
            word_cnt += len(lne.split(' '))
    print(args.folder, ":", word_cnt, 'words')

    outfile = f'dat/vecs/{args.folder}_pos.txt'
    make_emb(data, outfile)

    print("Creating annoy version of embeddings for fast lookup.")

    fname = os.path.join('dat/vecs', args.folder + '_pos.txt')

    if not os.path.exists('dat/annoy'):
        os.mkdir('dat/annoy')

    name = args.folder + '_pos'

    make_ann(fname, name)
