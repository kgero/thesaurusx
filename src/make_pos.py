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

makeme = ['arxiv_abs', 'nyt-science', 'poetry', 'joyce']

make_lemma_corpus('oneb')

def make_pos_pkl():
    c_path = 'dat/corpora'
    p_path = 'dat/pos'
    for item in os.listdir(c_path):
        if item not in ['merge-science-big']:
            continue
        i_path = os.path.join(c_path, item)
        if os.path.isdir(i_path):
            print('working on', i_path)
            data = {}
            count = 0
            for file in ['summaries.txt'] + os.listdir(i_path):
                count += 1
                if count > 500:
                    break
                # if file.split('.')[-1] == 'txt':
                if True:
                    print('\t', file)
                    f_path = os.path.join(i_path, file)
                    with open(f_path, 'r') as fle:
                        text = fle.read()
                    # batches = text.split('\n\n')
                    batches = text.split('\n')
                    print('num batches:', len(batches))
                    for i, batch in enumerate(batches):
                        if i % 100 == 0:
                            print('.', end=' ', flush=True)
                        doc = nlp(batch)
                        for token in doc:
                            word = token.text
                            pos = token.pos_
                            if word in data:
                                if pos not in data[word]:
                                    data[word].append(pos)
                            else:
                                data[word] = [pos]
            pkl_path = os.path.join(p_path, item) + '.pkl'
            pickle.dump(data, open(pkl_path, 'wb'))
