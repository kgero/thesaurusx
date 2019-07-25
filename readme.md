# Field Thesaurus

A Flask app that implements a new kind of thesaurus based on word embeddings. A live version of this application can be found at [thesaurus.ml].

You can run also run a local version, and create your own custom thesauruses based on your own corpora. Download a pre-prepared `dat` directory with everything needed to start running this asap:

`https://www.dropbox.com/s/0fhm46dnp8cc8aq/dat.zip?dl=0`

To view the thesaurus locally run:

`python server.py`

**

To create a new theseaurus run:

`python prepare_thesaurus.py -f corpus_name`

Where `corpus_name` is the name of a folder in `dat/corpora` and contains one or more text files.

## Setup

Runs on python3. Install requirements using requirements.txt. I recommend using a virtual environment.

Download a pre-prepared `dat` directory with some pre-trained word embeddings for the user interface:

`https://www.dropbox.com/s/0fhm46dnp8cc8aq/dat.zip?dl=0`

You should now have files in a folder called `dat/annoy` and one file in `dat/thes`. (In `dat/thes` is a plain-text "normal" thesaurus.)

### Spacy for part-of-speech tagging

To create your own word embeddings, you'll need to parse your corpus using the spacy parser. [Spacy.io] has great documentation, but really the only thing you need to do to make sure it works is to download a model with the following command:

`python -m spacy download en`

## Word embeddings

Word embeddings are first created with the gensim library, and then converted into [annoy](https://github.com/spotify/annoy) format, which is a approximate nearest neighbors library for very fast look-ups.


## Corpora

Most of the literary stuff comes from the Gutenberg project. Google's [word2vec project page](https://code.google.com/archive/p/word2vec/) contains links to some "general" English corpora (e.g. [Onbe Billion Word Benchmark](https://arxiv.org/abs/1312.3005). [This](https://www.docnow.io/catalog/) is a great resource for Tweet ID Datesets.
