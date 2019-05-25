"""
Simple HTTP server for prediction.

Bottle does not play well with classes, so let's use plain methods

Requirements:
- bottle
- the Dataset object must implement
  - s_parse_request(q) --> batch (list[Example])
    where q = Python object decoded from JSON (with json.loads)
  - s_generate_response(q, batch, logit, prediction) --> any
"""
import datetime
import json

from bottle import post, request, run


@post('/pred')
def process():
    q = request.forms.q
    q = json.loads(q)
    print('[{}] Received {}'.format(datetime.datetime.now().time(), q.get('info')))
    batch = EXP.dataset.s_parse_request(q)
    logit = EXP.model(batch)
    prediction = EXP.model.get_pred(logit, batch)
    return EXP.dataset.s_generate_response(q, batch, logit, prediction)


def start_server(exp, port):
    global EXP
    EXP = exp
    # This will open a global port!
    print('[{}] Starting server'.format(datetime.datetime.now().time()))
    # Feel free to use a better server backend than wsgiref.
    # https://bottlepy.org/docs/dev/deployment.html
    run(server='wsgiref', host='0.0.0.0', port=port)
    print('\nGood bye!')
