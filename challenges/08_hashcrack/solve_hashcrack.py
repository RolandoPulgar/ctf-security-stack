import socket
import re
import hashlib
import time

HOST = "chatelaine.cylabacademy.net"
PORT = 47556

# Diccionario con las claves resueltas
KNOWN_HASHES = {
    "482c811da5d5b4bc6d497ffa98491e38": "password123",
    "b7a875fc1ea228b9061041b7cec4bd3c52ab3ce3": "letmein",
    "916e8c4f79b25028c9e467f1eb8eee6d6bbdff965f9928310ad30a8d88697745": "qwerty098"
}

WORDLIST = [
    "password123", "letmein", "qwerty098", "password", "admin", "123456", "12345678",
    "welcome", "secret", "iloveyou", "computer", "princess", "starwars", "hunter2"
]

def crack(h):
    h = h.strip().lower()
    if h in KNOWN_HASHES:
        return KNOWN_HASHES[h]
    for w in WORDLIST:
        if hashlib.md5(w.encode()).hexdigest() == h or \
           hashlib.sha1(w.encode()).hexdigest() == h or \
           hashlib.sha256(w.encode()).hexdigest() == h:
            return w
    return None

def solve():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((HOST, PORT))
    
    buffer = ""
    while True:
        try:
            chunk = s.recv(4096).decode('utf-8', errors='ignore')
            if not chunk:
                break
            buffer += chunk
            print(chunk, end="", flush=True)
            
            # Buscar hashes
            hashes = re.findall(r'[0-9a-fA-F]{32,64}', buffer)
            if ("Enter the password" in chunk or "identified a hash" in chunk or "Crack this hash" in chunk) and hashes:
                h = hashes[-1]
                pwd = crack(h)
                if pwd:
                    print(f"\n[+] Enviando contraseña para {h}: {pwd}")
                    s.sendall((pwd + "\n").encode('utf-8'))
                    buffer = "" # reset
                    time.sleep(0.3)
                    
            if "picoctf{" in buffer.lower() or "academy{" in buffer.lower() or "flag:" in buffer.lower():
                print("\n[+] Fin del desafío.")
                break
        except Exception as e:
            print(f"\n[-] Fin de conexión: {e}")
            break
            
    s.close()

if __name__ == '__main__':
    solve()
