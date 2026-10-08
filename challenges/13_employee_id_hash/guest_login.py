import requests
import json
import hashlib

BASE_URL = "http://chatelaine.cylabacademy.net:46099"

s = requests.Session()

# 1. Login como guest
print("[*] 1. Iniciando sesión con credenciales de guest...")
r = s.post(f"{BASE_URL}/login", json={
    "email": "guest@cylabacademy.org",
    "password": "guest"
}, allow_redirects=True)

print(f"Status: {r.status_code}, URL: {r.url}")
print("Cookies:", s.cookies.get_dict())
print("\nContenido tras login:")
print(r.text)
