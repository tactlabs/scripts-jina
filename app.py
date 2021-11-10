from flask import Flask, render_template, request
from jina import Client, Document, DocumentArray

app = Flask(__name__)


def send_req(text):
    c = Client( port = 12345, protocol = 'http', host = 'localhost')
    print('sending query to jina flow ...')
    docs = DocumentArray([Document(text = text)])
    res = c.post(
        on = '/search',
        inputs = docs,
        return_results = True,
        parameters = {
            'top_k' : 10
        },
        on_done = lambda x : x.docs[0].matches
    )

    return res

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods = ['POST'])
def index_post():
    text = request.form.get('query_word')
    print(text)
    matches = send_req(text)

    data = [
        {
            "script" : doc.text,
            "show" : doc.tags['solution'],
            'episode' : doc.tags['episode'],
            'season' : doc.tags['season']
        } for doc in matches
    ]

    return render_template('index.html', result = data)


if __name__ == '__main__':
    app.run(
        debug = True
    )   