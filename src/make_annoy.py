import pickle
import os

from annoy import AnnoyIndex
from time import time


for fle_nm in os.listdir('dat/vecs'):
    emb_nm = fle_nm.split('.')[0]
    if emb_nm not in ['merge-science-big', 'merge-science-small']:
        continue
    print(emb_nm)

    vocab = []

    with open('dat/vecs/{}.txt'.format(emb_nm), 'r') as fle:
        sz, dim = [int(num) for num in fle.readline().split(' ')]
        print('vocab: {} dim: {}'.format(sz, dim))

        t = AnnoyIndex(dim)
        i = 0
        for line in fle:
            word = line.split(' ')[0]
            try:
                vec = [float(num) for num in line.strip('\n').strip(' ').split(' ')[1:]]
            except ValueError:
                print(line.strip('\n').split(' ')[1:])
                raise ValueError
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
