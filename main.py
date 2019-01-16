import json
from sklearn.decomposition import PCA

from flask import Flask, Response, render_template, request
from time import time

from src.simple_lookup import simple_lookup, check_words, warm_up, thesaurus_lookup, pca_lookup
from src.get_usage import get_ex_sen


app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def hello_world():
    return render_template('index.html', results=['a', 'b'])

@app.route('/get_words_simple', methods=['POST'])
def get_words_simple():
    # print('got get_words_simple request...', end=' ')
    # rform = request.form
    # err = check_words([rform['keyword'], rform['base'], rform['goal']], embkey=rform['embd'])
    # start = time()
    # wrds, dist = analogy_lookup(rform['keyword'], rform['base'], rform['goal'], embkey=rform['embd'], n=50)
    # print('finished in {:<2f} seconds'.format(time() - start))
    # data = {'words': wrds, 'distance': dist}
    # if err:
    #     data['error'] = err
    wrds = thesaurus_lookup(request.form['keyword'])
    data = {'words': wrds}
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp

@app.route('/get_words_algo', methods=['POST'])
def get_words_algo():
    
    rform = request.form
    data = simple_lookup(rform['keyword'], embkey=rform['embd'])
    data.update(get_ex_sen(rform['keyword'], rform['embd']))
    data['embd'] = rform['embd']
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp


if __name__ == "__main__":
    # print("doing embedding warm-up...")
    # start = time()
    # warm_up()
    # print('did warm-up in {:<2f} seconds'.format(time() - start))
    app.run()
