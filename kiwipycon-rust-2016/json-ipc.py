#!/home/robertc/.virtualenvs/scratch-pypy/bin/python

import json

import requests

s = requests.Session()
for _ in range(200):
    r = s.post('http://127.0.0.1:12345/', json = {'n': 60})
    x = (json.loads(r.text))['fib']
print(x)
