#!/usr/bin/env python3

import requests

url = ('http://math:7070/challenge')
headers = {'User-Agent' : 'Math Calculator (Python 3)'}

session = requests.Session()
session.headers.update(headers)

r = session.get(url)

solve_this = r.text

for i in range(100):

    data = (eval(solve_this))
    print(solve_this, data)

    s = session.post(url=url, data=str(data))

    print(s.content)
    solve_this = s.text