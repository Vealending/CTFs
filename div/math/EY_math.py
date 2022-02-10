#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

url = ('http://math:7070/challenge')

session = requests.Session()

r = session.get(url)
soup = BeautifulSoup(r)

solve = soup.find('span').get_text()
print(solve)
solution = eval(solve)

print(solve, solution)

s = session.post(url=url, data={"answer": solution, "submit": "submit"})

print(s.content)

soup.find("div", {"name": "eq"})