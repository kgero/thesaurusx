"""Create dict for each corpus of words and possible part of speech tags."""

import pickle
import os
import spacy

c_path = 'dat/corpora'
p_path = 'dat/pos'

nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
doc = nlp(u'Apple is looking at buying U.K. startup for $1 billion')

for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
          token.shape_, token.is_alpha, token.is_stop)

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
