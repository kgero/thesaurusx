# Avantpie

A Flask app that implements a new kind of thesaurus based on word embeddings.

## Setup

Runs on python3. Install requirements using requirements.txt. I recommend using a virtual environment.

You'll also need a `dat` directory with the word embeddings, and `tmp` directory if you'll be training your own.

## Word embeddings

Train new word embeddings with `src/make_embeddings.py`. This save the embeddings to the `tmp` directory as .txt file. You'll then need to convert them to magniute format. (Learn more about [Magnitude: a fast, simple vector embedding utility library](https://github.com/plasticityai/magnitude); also includes some pre-trained word embeddings to download.) Need a `dat` directory with the following:

```
dat/
    glove.6B.200d.magnitude
    glove.twitter.27B.50d.magnitude
    GoogleNews-vectors-negative300.magnitude
    ...more
```

To convert other word embedding formats to magnitude:

`python -m pymagnitude.converter -i <PATH TO FILE TO BE CONVERTED> -o <OUTPUT PATH FOR MAGNITUDE FILE>`


## Run app

Main way to run:

`python main.py`

Or:

`export FLASK_APP=server.py`

Then to run:

`flask run`
