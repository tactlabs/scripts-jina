from flask import Flask, render_template, request
from jina import Client, Document, DocumentArray
import re
import random

app = Flask(__name__)


def send_req(text):
    c = Client( port = 12344, protocol = 'http', host = 'localhost')
    print('sending query to jina flow ...')
    docs = DocumentArray([Document(text = text)])
    res = c.post(
        on = '/search',
        inputs = docs,
        return_results = True,
        on_error = print,
        on_done = lambda x : x.docs[0].matches,
        parameters = {
            'top_K' : 5
        }
    )
    print('Got response from the flow ...')
    return res

def highlight(query, script):
    potential_script = None
    scripts = re.split(r'\.( )[a-zA-Z]+:', script)
    query = '|'.join([i for i in query.split() if len(i) > 2])
    for s in scripts:
        if re.findall(r'{}'.format(query), s.lower()):
            potential_script = s
            break

    if not potential_script:
        potential_script = random.choice(scripts)
    
    return potential_script



@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods = ['POST'])
def index_post():
    text = request.form.get('query_word')
    response = send_req(text)[0].docs[0].matches[:5]

    data = [
        {
            "script" : highlight(text, doc.text),
            "show" : doc.tags['show'],
            'episode' : doc.tags['episode'],
            'season' : doc.tags['season']
        } for doc in response
    ]

    return render_template('index.html', result = data)


if __name__ == '__main__':
    app.run(
        debug = True,
        port = 5050 
    )   