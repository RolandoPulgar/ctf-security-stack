import requests

BASE_URL = "http://chatelaine.cylabacademy.net:11152"

s = requests.Session()

# 1. Registrar usuario
print("[*] Registrando usuario...")
r_reg = s.post(f"{BASE_URL}/register", data={
    "username": "hacker1337",
    "password": "Password123!",
    "conf_password": "Password123!"
}, allow_redirects=True)
print(f"Registro Status: {r_reg.status_code}, URL: {r_reg.url}")

# 2. Login
print("[*] Haciendo login...")
r_log = s.post(f"{BASE_URL}/login", data={
    "username": "hacker1337",
    "password": "Password123!"
}, allow_redirects=True)
print(f"Login Status: {r_log.status_code}, URL: {r_log.url}")
print("Cookies:", s.cookies.get_dict())

print("\n[*] Contenido tras login exitoso:")
print(r_log.text)

# 3. Consultar /sessions ahora que estamos logueados
print("\n[*] Consultando /sessions con cookies de sesión...")
r_sess = s.get(f"{BASE_URL}/sessions")
print(f"Status /sessions: {r_sess.status_code}")
print(r_sess.text)
