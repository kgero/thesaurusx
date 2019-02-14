import json
from sklearn.decomposition import PCA

from flask import Flask, Response, render_template, request
from time import time

from src.simple_lookup import simple_lookup, check_words, thesaurus_lookup, get_pos
from src.get_usage import get_ex_sen


app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def hello_world():
    return render_template('index.html', results=['a', 'b'])

@app.route('/get_words_simple', methods=['POST'])
def get_words_simple():
    pos = get_pos(request.form['keyword'])
    word = request.form['keyword'].split(':')[0]
    if not pos:
        data = {'error': 'no part of speech found'}
        resp = Response(json.dumps(data), status=200, mimetype='application/json')
        return resp
    if ':' in request.form['keyword']:
        pos_search = request.form['keyword'].split(':')[1]
    else:
        pos_search = pos[0]
    wrds = thesaurus_lookup(word, pos_search)
    data = {'words': wrds}
    data['pos'] = pos
    data['pos_search'] = pos_search
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp

@app.route('/get_words_algo', methods=['POST'])
def get_words_algo():
    rform = request.form
    word = request.form['keyword'].split(':')[0]
    data = simple_lookup(word, rform['pos'], embkey=rform['embd'])
    data.update(get_ex_sen(word, rform['embd']))
    data['embd'] = rform['embd']
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp


if __name__ == "__main__":
    app.run()
