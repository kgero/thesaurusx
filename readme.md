# Field Thesaurus

A Flask app that implements a new kind of thesaurus based on word embeddings.

A live version of this application can be found at [thesaurus.ml].

You can run also run a local version, and create your own custom thesauruses based on your own corpora.

To create a new theseaurus run:

`python prepare_thesaurus.py -f corpus_name`

Where `corpus_name` is the name of a folder in `dat/corpora` and contains one or more text files.

To view the thesaurus locally run:

`python server.py`

## Todo

* better way to select vectors for web interface
* test doing whole thing from "new" download from github

## Setup

Runs on python3. Install requirements using requirements.txt. I recommend using a virtual environment.

This github repo comes with some pre-trained word embeddings for the user interface in dat/annoy.

### Spacy for part-of-speech tagging

To create your own word embeddings, you'll need to parse your corpuss using the spacy parser. [spacy.io] has great documentation, but really the only thing you need to do to make sure it works is to download a model with the following command:

`python -m spacy download en`

## Word embeddings

Word embeddings are first created with the gensim library, and then converted into [annoy](https://github.com/spotify/annoy) format, which is a approximate nearest neighbors library to very fast look-ups.


## Corpora

Most of the literary stuff comes from the Gutenberg project. Google's [word2vec project page](https://code.google.com/archive/p/word2vec/) contains links to some "general" English corpora (e.g. [Onbe Billion Word Benchmark](https://arxiv.org/abs/1312.3005). [This](https://www.docnow.io/catalog/) is a great resource for Tweet ID Datesets.
