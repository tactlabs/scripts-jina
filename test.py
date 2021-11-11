from jina import Client, Document, DocumentArray


def send_req(text):
    c = Client( port = 12345, protocol = 'http', host = 'localhost')
    print('sending query to jina flow ...')
    docs = DocumentArray([Document(text = text)])
    res = c.post(
        on = '/search',
        inputs = docs,
        return_results = True,
        on_error = print,
        on_done = lambda x : x.docs[0].matches
    )

    return res


print(send_req('they dont know'))