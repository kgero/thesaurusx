# Avantpie

A Flask app that implements a new kind of thesaurus based on word embeddings.

## Setup

Runs on python3. Install requirements using requirements.txt. I recommend using a virtual environment.

When running the jupyter notebook, make sure you are running the right python executable. To get a regular virtualenv as a kernel, run:

`python -m ipykernel install --user --name=my-virtualenv-name`

You'll also need a `dat/vecs` directory with the word embeddings and `dat/corpora` directory with the raw corpora (for pulling example sentences). Currently requires internet connection; makes an API call to [DataMuse](http://www.datamuse.com/api/).

## Word embeddings

Word embeddings should be in `.txt` format with the vocab and dimension on the first line. Use `src/make_annoy.py` to convert any files in `/dat/vecs/` into [annoy](https://github.com/spotify/annoy) format, which is a approximate nearest neighbors library to very fast look-ups.

### Deprecated

Train new word embeddings with `src/make_embeddings.py`. This save the embeddings to the `tmp` directory as .txt file. You'll then need to convert them to magniute format. (Learn more about [Magnitude: a fast, simple vector embedding utility library](https://github.com/plasticityai/magnitude); also includes some pre-trained word embeddings to download.) Need a `dat` directory with some `.magnitude` embeddings; will select whatevers in the `dat` directory with the right extension. (Make sure that it's in the list in `main.js`.)

To convert other word embedding formats to magnitude:

`python -m pymagnitude.converter -i <PATH TO FILE TO BE CONVERTED> -o <OUTPUT PATH FOR MAGNITUDE FILE>`


## Run app

Main way to run:

`python main.py`

Or:

`export FLASK_APP=server.py`

Then to run:

`flask run`
