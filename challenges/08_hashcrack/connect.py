import socket
import sys
import hashlib
import urllib.request
import json

HOST = "xebec.cylabacademy.net"
PORT = 38308

def interact():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((HOST, PORT))
    
    data = b""
    while True:
        try:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk
            text = chunk.decode('utf-8', errors='ignore')
            print(text, end="", flush=True)
            
            # Si pide input
            if ":" in text or ">" in text or "?" in text:
                break
        except socket.timeout:
            break
            
    print("\n[+] Fin de recepción inicial.")
    s.close()

if __name__ == '__main__':
    interact()
