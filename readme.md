# Field Thesaurus

A Flask app that implements a new kind of thesaurus based on word embeddings.

## Setup

Runs on python3. Install requirements using requirements.txt. I recommend using a virtual environment.

When running the jupyter notebook, make sure you are running the right python executable. To get a regular virtualenv as a kernel, run:

`python -m ipykernel install --user --name=my-virtualenv-name`

You'll also need a `dat/vecs` directory with the word embeddings and `dat/corpora` directory with the raw corpora (for pulling example sentences). Currently requires internet connection; makes an API call to [DataMuse](http://www.datamuse.com/api/).

## Spacy for part-of-speech tagging

`python -m spacy download en`

## Word embeddings

Word embeddings should be in `.txt` format with the vocab and dimension on the first line. Use `src/make_annoy.py` to convert any files in `/dat/vecs/` into [annoy](https://github.com/spotify/annoy) format, which is a approximate nearest neighbors library to very fast look-ups.

## Run app

Main way to run:

`python main.py`

Or:

`export FLASK_APP=server.py`

Then to run:

`flask run`

## Corpora

Most of the literary stuff comes from the Gutenberg project. Google's [word2vec project page](https://code.google.com/archive/p/word2vec/) contains links to some "general" English corpora (e.g. [Onbe Billion Word Benchmark](https://arxiv.org/abs/1312.3005). [This](https://www.docnow.io/catalog/) is a great resource for Tweet ID Datesets.

### Aretha Tweets

Aretha Franklin
Creator: Bergis Jules, Ed Summers
Tweets: 4,164,570
Published: 2018-09-05
Date Coverage: 2018-08-08 - 2018-09-03
Tags: Music, Civil Rights Movement, African Americans

Description
On August 16, 2018 Aretha Franklin died in Detroit, Michigan at the age of 76. Franklin, also known as the Queen of Soul, had an award winning career as a singer, songwriter, actress and pianist while also being described as the voice of the civil rights movement. This dataset contains two tweet id files. The first was collected from the search API during the response to the announcement of her death, which includes tweets from August 8 - August 19 using the query “Aretha Franklin” OR “Queen of Soul”. The second dataset was collected over August 24 to September 3, which includes the date of her funeral on August 31. This second dataset was collected using the query “Aretha Franklin” OR “Queen of Soul” OR ArethaHomegoing OR ArethaFranklinFuneral OR ArethaFranklin which includes hashtags that were trending at the time. The datasets contain 2,832,128 and 1,332,442 tweets respectively.

### Australia Tweets

Creator: Tim Sherratt
Tweets: 55,698
Published: 2017-05-08
Date Coverage: 2017-04-20 - 2017-04-27
Tags: politics, Australia

Description
On 20 April 2017 the Australian Government announced that the Australian citizenship test would be made harder, with an increased focus on ‘Australian values’. Suggestions as to what ‘Australian values’ might actually be soon started to be shared on Twitter using the hashtag #australianvalues. 55,698 tweet ids for #australianvales collected with #Documenting the Now’s Twarc from 20 to 27 April 2017.

### Part of speech tagging (from nltk tagger)

CC coordinating conjunction
CD cardinal digit
DT determiner
EX existential there (like: “there is” … think of it like “there exists”)
FW foreign word
IN preposition/subordinating conjunction
JJ adjective ‘big’
JJR adjective, comparative ‘bigger’
JJS adjective, superlative ‘biggest’
LS list marker 1)
MD modal could, will
NN noun, singular ‘desk’
NNS noun plural ‘desks’
NNP proper noun, singular ‘Harrison’
NNPS proper noun, plural ‘Americans’
PDT predeterminer ‘all the kids’
POS possessive ending parent’s
PRP personal pronoun I, he, she
PRP$ possessive pronoun my, his, hers
RB adverb very, silently,
RBR adverb, comparative better
RBS adverb, superlative best
RP particle give up
TO, to go ‘to’ the store.
UH interjection, errrrrrrrm
VB verb, base form take
VBD verb, past tense took
VBG verb, gerund/present participle taking
VBN verb, past participle taken
VBP verb, sing. present, non-3d take
VBZ verb, 3rd person sing. present takes
WDT wh-determiner which
WP wh-pronoun who, what
WP$ possessive wh-pronoun whose
WRB wh-abverb where, when

## Deprecated

Train new word embeddings with `src/make_embeddings.py`. This save the embeddings to the `tmp` directory as .txt file. You'll then need to convert them to magniute format. (Learn more about [Magnitude: a fast, simple vector embedding utility library](https://github.com/plasticityai/magnitude); also includes some pre-trained word embeddings to download.) Need a `dat` directory with some `.magnitude` embeddings; will select whatevers in the `dat` directory with the right extension. (Make sure that it's in the list in `main.js`.)

To convert other word embedding formats to magnitude:

`python -m pymagnitude.converter -i <PATH TO FILE TO BE CONVERTED> -o <OUTPUT PATH FOR MAGNITUDE FILE>`

