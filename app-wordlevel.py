import json
from sklearn.decomposition import PCA

from flask import Flask, Response, render_template, request
from time import time

from src.simple_lookup_pos import real_simple_lookup

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def hello_world():
    return render_template('word-level.html')

@app.route('/real_simple_lookup', methods=['POST'])
def get_words_simple():
    word = request.form['keyword']
    embkey = request.form['embkey']
    if len(word) == 0:
        resp = Response(json.dumps({'error': 'empty string'}), status=200, mimetype='application/json')
        return resp
    if 'n' in request.form:
        n = int(request.form['n'])
    else:
        n = 5
    data = real_simple_lookup(word, embkey, n=n)
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp

if __name__ == "__main__":
    app.run()
