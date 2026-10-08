import socket
import re
import math
import urllib.request
import json
from Crypto.Util.number import long_to_bytes, inverse

HOST = "chatelaine.cylabacademy.net"
PORT = 15259

def solve_fermat(n):
    """Ataque de Fermat para p ≈ q"""
    a = math.isqrt(n)
    if a * a < n:
        a += 1
    for _ in range(5000000): # 5 millones de iteraciones max
        b2 = a * a - n
        b = math.isqrt(b2)
        if b * b == b2:
            p = a - b
            q = a + b
            return p, q
        a += 1
    return None, None

def query_factordb(n):
    """Consultar FactorDB API"""
    try:
        url = f"http://factordb.com/api?query={n}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data.get("status") in ["FF", "CF"]:
                factors = [int(f[0]) for f in data.get("factors", [])]
                if len(factors) >= 2:
                    return factors[0], factors[1]
    except Exception as e:
        print(f"[-] Error en FactorDB: {e}")
    return None, None

def get_challenge_data():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((HOST, PORT))
    
    raw = ""
    while True:
        try:
            chunk = s.recv(4096).decode('utf-8', errors='ignore')
            if not chunk:
                break
            raw += chunk
        except Exception:
            break
    s.close()
    return raw

def main():
    print(f"[*] Conectando a {HOST}:{PORT}...")
    raw = get_challenge_data()
    print("[+] Datos recibidos:")
    print(raw)
    
    m_n = re.search(r'N:\s*(\d+)', raw)
    m_e = re.search(r'e:\s*(\d+)', raw)
    m_c = re.search(r'cyphertext:\s*(\d+)', raw)
    
    if not (m_n and m_e and m_c):
        print("[-] No se pudieron extraer los parámetros N, e, cyphertext.")
        return
        
    N = int(m_n.group(1))
    e = int(m_e.group(1))
    c = int(m_c.group(1))
    
    print(f"[*] N (bits: {N.bit_length()}): {N}")
    print(f"[*] e: {e}")
    print(f"[*] c: {c}")
    
    # 1. Probar Fermat (p ≈ q)
    print("\n[*] Probando factorización de Fermat...")
    p, q = solve_fermat(N)
    
    if not p or not q:
        print("[*] Fermat no dio resultado rápido, consultando FactorDB...")
        p, q = query_factordb(N)
        
    if p and q:
        print(f"[+] ¡FACTORIZACIÓN EXITOSA!")
        print(f"[+] p = {p}")
        print(f"[+] q = {q}")
        
        phi = (p - 1) * (q - 1)
        d = inverse(e, phi)
        m = pow(c, d, N)
        flag = long_to_bytes(m).decode('utf-8', errors='ignore')
        
        print("=" * 60)
        print(f"[+] FLAG DESENCRIPTADA: {flag}")
        print("=" * 60)
    else:
        print("[-] Se requiere otro método de ataque (Wiener / Pollard p-1 / etc.)")

if __name__ == '__main__':
    main()
