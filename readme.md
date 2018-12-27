# Avantpie

A Flask app that implements a new kind of thesaurus based on word embeddings.

## Setup

Runs on python3. Install requirements using requirements.txt. 

Relies on word embeddings in magnitude format. (Learn more about [Magnitude: a fast, simple vector embedding utility library](https://github.com/plasticityai/magnitude); also includes the word embeddings to download.) Need a `dat` directory with the following:

```
dat/
    glove.6B.200d.magnitude
    glove.twitter.27B.50d.magnitude
    GoogleNews-vectors-negative300.magnitude
```

## Run app

Main way to run:

`python main.py`

Or:

`export FLASK_APP=server.py`

Then to run:

`flask run`
