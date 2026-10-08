import requests
from bs4 import BeautifulSoup
import hashlib

BASE_URL = "http://chatelaine.cylabacademy.net:46099"

s = requests.Session()
r = s.get(BASE_URL)
print(f"[*] GET / -> Status: {r.status_code}")
print(r.text)

# Inspeccionar enlaces o formularios
soup = BeautifulSoup(r.text, 'html.parser')
for a in soup.find_all('a'):
    print("Link:", a.get('href'))
for form in soup.find_all('form'):
    print("Form action:", form.get('action'), "method:", form.get('method'))
    for inp in form.find_all('input'):
        print("  Input:", inp.get('name'), inp.get('type'))
