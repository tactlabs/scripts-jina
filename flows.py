from jina import Flow, Executor, Document, DocumentArray
from jina.types.document import DocumentSourceType
import pandas as pd 
import numpy as np 


def get_docs(fname):
    docs = DocumentArray()
    df = pd.read_csv(fname)
    for text in df.iterrows():
        doc = Document(text = text[1]['Text'], tags = {
            'episode_name' : text[1]['Episode'],
            'season' : text[1]['Season'],
            'show' : text[1]['Show']
        })

        docs.append(doc)

    return docs


def script_flow():
    flow = (
        Flow(port_expose = 12345, protocol = 'http', cors = True)
        .add(
            name = 'encoder',
            uses = 'jinahub://CLIPTextEncoder'
        )
        .add(
            name = 'indexer',
            uses = 'jinahub://SimpleIndexer'
        )
    )

    return flow



print(get_docs('jina_2.csv')[0].json())
# with script_flow() as f:
#     f.post(
#         on = '/index',
#         inputs = get_docs('jina_2.csv'),
#         on_done = print('indexed successfully....')  
#         )
#     f.block()
        