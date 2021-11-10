from flask import Flask, render_template, request
# from flask_cors import CORS, cross_origin
from jina import Client, Document, DocumentArray

app = Flask(__name__)
# cors = CORS(app)


def send_req(text):
    c = Client( port = 12345, protocol = 'http', cors = True )
    res = c.post(
        on = '/search',
        return_results = True,
        parameters = {
            'top_k' : 10
        },
        on_done = lambda x : x.docs[0].matches
    )

@app.route('/', methods = ['POST', 'GET'])
# @cross_origin
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(
        debug = True
    )