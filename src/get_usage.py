"""
Functions for getting examples of word usage.
"""
import os

STYLES = ['darwin', 'dickens', 'food', 'joyce', 'poetry', 'sherlock']

def get_ex_sen(word, style):
    """Return string of example usage of word in style corpus."""
    if style not in STYLES:
        return {'dicterror': 'no corpus available for {}.'.format(style)}
    fldr = os.path.join('dat', style)
    for fname in os.listdir(fldr):
        for line in open(os.path.join(fldr, fname), errors='ignore'):
            clean = line.lower()
            if word in clean:
                return {'sentence': line}
    return {'dicterror': "didn't find word in corpus"}
