import json

from flask import Flask, Response, render_template, request
from time import time

from src.simple_lookup import analogy_lookup, check_words, warm_up

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def hello_world():
    return render_template('index.html', results=['a', 'b'])

@app.route('/get_words_simple', methods=['POST'])
def get_words_simple():
    rform = request.form
    err = check_words([rform['keyword'], rform['base'], rform['goal']], embkey=rform['embd'])
    start = time()
    wrds = analogy_lookup(rform['keyword'], rform['base'], rform['goal'], embkey=rform['embd'])
    print('got analogy_lookup in {:<2f} seconds'.format(time() - start))
    data = {'words': wrds}
    if err:
        data['error'] = err

    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp

if __name__ == "__main__":
    print("doing embedding warm-up...")
    start = time()
    warm_up()
    print('did warm-up in {:<2f} seconds'.format(time() - start))
    app.run()
