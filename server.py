import json

from flask import Flask, Response, render_template, request

from src.simple_lookup import simple_lookup, thesaurus_lookup


app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html', results=['a', 'b'])

@app.route('/get_words_thes', methods=['POST'])
def get_words_thes():
    data = thesaurus_lookup(request.form['keyword'])
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp

@app.route('/get_words_algo', methods=['POST'])
def get_words_algo():
    rform = request.form
    data = simple_lookup(rform['keyword'], embkey=rform['embd'])

    # deal with no word in embeddings
    if 'error' in data:
        found = False
        sub_data = thesaurus_lookup(request.form['keyword'])
        if 'results' in sub_data:
            for key, val in sub_data['results'].items():
                if key == 'pos':
                    continue
                if found:
                    break
                for i in range(3):
                    new_data = simple_lookup(val[i], embkey=rform['embd'])
                    if 'results' in new_data:
                        print(f"error in {rform['embd']}, found a new one with {val[i]}")
                        data = new_data
                        found = True
                        break

    data['embd'] = rform['embd']
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp


if __name__ == "__main__":
    app.run(debug=False)
