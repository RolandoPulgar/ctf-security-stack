# Template: Remote TCP / Service Interaction (pwntools)
# Uso: python tcp_solver.py [HOST] [PORT]

import sys
from pwn import *

context.log_level = 'info' # Cambiar a 'debug' si necesitas ver cada byte

HOST = sys.argv[1] if len(sys.argv) > 1 else 'challenges.hackrocks.com'
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 1337

def solve():
    r = remote(HOST, PORT)
    
    # Recibir banner de bienvenida
    banner = r.recvuntil(b'> ')
    print("[+] Banner recibido:")
    print(banner.decode('utf-8', errors='ignore'))
    
    # Enviar payload o respuesta calculada
    payload = b"test_payload\n"
    r.send(payload)
    
    # Recibir respuesta y flag
    response = r.recvall(timeout=3)
    print("[+] Respuesta recibida:")
    print(response.decode('utf-8', errors='ignore'))

if __name__ == '__main__':
    solve()
