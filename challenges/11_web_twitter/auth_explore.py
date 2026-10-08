import requests

BASE_URL = "http://chatelaine.cylabacademy.net:11152"

s = requests.Session()

# 1. Registrar usuario
print("[*] Registrando usuario de prueba...")
r_reg = s.post(f"{BASE_URL}/register", data={"username": "testuser1337", "password": "Password123!"}, allow_redirects=True)
print(f"Registro Status: {r_reg.status_code}, URL: {r_reg.url}")

# 2. Login si no redirigió automáticamente
print("[*] Haciendo login...")
r_log = s.post(f"{BASE_URL}/login", data={"username": "testuser1337", "password": "Password123!"}, allow_redirects=True)
print(f"Login Status: {r_log.status_code}, URL: {r_log.url}")
print("Cookies de sesión:", s.cookies.get_dict())
print("\nContenido tras login:")
print(r_log.text[:800])

# 3. Probar /sessions y otros endpoints autenticados
for path in ["/", "/sessions", "/users", "/admin", "/tweets", "/post", "/flag", "/profile"]:
    r = s.get(f"{BASE_URL}{path}")
    print(f"\n[+] GET {path} -> Status: {r.status_code}, Length: {len(r.text)}")
    if r.status_code == 200:
        print(f"Primeros 400 chars de {path}:")
        print(r.text[:400])
