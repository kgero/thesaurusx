# Avantpie

A Flask app that implements a new kind of thesaurus based on word embeddings.

## Setup

Runs on python3. Install requirements using requirements.txt. I recommend using a virtual environment.

When running the jupyter notebook, make sure you are running the right python executable. To get a regular virtualenv as a kernel, run:

`python -m ipykernel install --user --name=my-virtualenv-name`

You'll also need a `dat` directory with the word embeddings, and `tmp` directory if you'll be training your own.

## Word embeddings

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
