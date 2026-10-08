import socket
import sys

HOST = "chatelaine.cylabacademy.net"
PORT = 47556

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(8)
try:
    s.connect((HOST, PORT))
    print("[+] Conectado exitosamente!")
    banner = s.recv(4096).decode('utf-8', errors='ignore')
    print("[+] Banner del servidor:")
    print(banner)
except Exception as e:
    print(f"[-] Error de conexión local: {e}")
finally:
    s.close()
