# Style Thesaurus

A Flask app that implements a different kind of thesaurus based on word embeddings. A live version of this application can be found at language-play.com/thesaurusx.

You can run also run a local version, and create your own custom thesauruses based on your own corpora. Download a pre-prepared `dat` directory with everything needed to start running this asap:

`https://www.dropbox.com/s/0fhm46dnp8cc8aq/dat.zip?dl=0`

To view the thesaurus locally run:

`python server.py`

**

To create a new theseaurus run:

`python prepare_thesaurus.py -f corpus_name`

Where `corpus_name` is the name of a folder in `dat/corpora` and contains one or more text files.

## General setup

Runs on python3. Install requirements using requirements.txt. I recommend using a virtual environment.

Download a pre-prepared `dat` directory with some pre-trained word embeddings for the user interface:

`https://www.dropbox.com/s/0fhm46dnp8cc8aq/dat.zip?dl=0`

You should now have files in a folder called `dat/annoy` and one file in `dat/thes`. (In `dat/thes` is a plain-text "normal" thesaurus.)

### Spacy for part-of-speech tagging

To create your own word embeddings, you'll need to parse your corpus using the spacy parser. [Spacy.io] has great documentation, but really the only thing you need to do to make sure it works is to download a model with the following command:

`python -m spacy download en`

### Word embeddings

Word embeddings are first created with the gensim library, and then converted into [annoy](https://github.com/spotify/annoy) format, which is a approximate nearest neighbors library for very fast look-ups.


### Corpora

Most of the literary stuff comes from the Gutenberg project. Google's [word2vec project page](https://code.google.com/archive/p/word2vec/) contains links to some "general" English corpora (e.g. [Onbe Billion Word Benchmark](https://arxiv.org/abs/1312.3005). [This](https://www.docnow.io/catalog/) is a great resource for Tweet ID Datesets.

## Remote server setup

The information below is for running the web app on a remote server.

### How this app is served

```
Browser → nginx (/stylethesaurus) → uWSGI socket → Flask (server.py)
```

nginx receives all traffic for the domain. It reads the path and forwards
`/stylethesaurus` requests to this app via a Unix socket. uWSGI runs the
Flask app as a persistent process, kept alive by systemd.

### Relevant files in this repo

**`thesaurusx.ini`** — uWSGI config. Tells uWSGI how to run the app:
how many processes, where to put the socket, and what path to mount at.

**`server_setup.sh`** — Run once on a fresh server after cloning. It:
1. Creates a Python virtualenv and installs `requirements.txt`
2. Writes a systemd `.service` file to `/etc/systemd/system/` (relative path)
3. Enables and starts the service


### First-time setup on a new server

1. Clone the github repo.
2. Download the embedding files for `/dat` (they're not in the github repo; see above). 
3. Run `bash server_setup.sh`.


### Wiring to nginx

nginx config lives centrally on the server (not in this repo) because it
covers multiple apps running on the domain at once. After running `server_setup.sh`, add these
blocks to the nginx server config:

```nginx
location /stylethesaurus {
    include uwsgi_params;
    uwsgi_pass unix:/home/username/thesaurusx/thesaurusx.sock;
}
```

This should be a `.conf` file in `/etc/nginx/sites-available/`

Then reload nginx:

```bash
sudo nginx -t && sudo systemctl reload nginx
```

[This tutorial](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04) might help.

### Deploying updates

```bash
cd ~/thesaurusx
git pull
sudo systemctl restart stylethesaurus
```


### Useful commands

```bash
sudo systemctl status stylethesaurus       # is it running?
sudo systemctl restart stylethesaurus      # restart after code changes
sudo journalctl -u stylethesaurus -f       # live logs
sudo journalctl -u stylethesaurus -n 100   # last 100 log lines
```