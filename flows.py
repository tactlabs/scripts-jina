from jina import Flow, Executor, Document, DocumentArray
import pandas as pd 
import numpy as np 
import os 


def get_docs(fname):
    docs = DocumentArray()
    df = pd.read_csv(fname)
    for text in df.iterrows():
        doc = Document(text = text[1]['Text'], tags = {
            'episode' : text[1]['Episode'],
            'season' : text[1]['Season'],
            'show' : text[1]['Show']
        })

        docs.append(doc)

    return docs


flow = (
        Flow(cors = True, protocol = 'http', install_requirements=True, port_expose = 12344)
        .add(
            name = 'encoder',
            uses = 'jinahub://TransformerTorchEncoder/v0.3',
            force=True
        )
        .add(
            name = 'indexer',
            uses = 'jinahub://SimpleIndexer'
        )
    )


os.system('rm -rf workspace')
with flow as f:
    f.post(
        on = '/index',
        inputs = get_docs('jina_2.csv'),
        on_done = print('indexed successfully....')  
        )
    f.block()
        