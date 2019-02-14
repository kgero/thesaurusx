"""
Functions for getting examples of word usage.
"""
import os

STYLES = ['darwin', 'dickens', 'food', 'joyce', 'poetry', 'sherlock', 'law', 'arxiv_abs']

def get_ex_sen(word, style):
    """Return string of example usage of word in style corpus."""
    if style not in STYLES:
        return {'dicterror': 'no corpus available for {}.'.format(style)}
    fldr = os.path.join('dat/corpora', style)
    for fname in os.listdir(fldr):
        prevline = ''
        for line in open(os.path.join(fldr, fname), errors='ignore'):
            clean = line.lower()
            if word in clean:
                if len(line) > 150:
                    sentences = line.split('. ')
                    for sen in sentences:
                        if word in sen.lower():
                            return {'sentence': sen + '.'}
                elif len(clean.split(word)[0]) < 10:
                    sentences = (prevline + line).split('. ')
                    for sen in sentences:
                        if word in sen.lower():
                            return {'sentence': sen + '.'}
                else:
                    return {'sentence': line}
            prevline = line
    return {'dicterror': "didn't find word in corpus"}
