# Reto 01: Reverse Engineering / Crackme
# Simulación de binario de validación de licencia con lógica de verificación por restricciones matemáticas

import sys

def check_key(key: str) -> bool:
    if len(key) != 16:
        return False
    
    # Restricciones de validación
    # 1. Prefijo ANCI
    if not key.startswith("ANCI-"):
        return False
    
    # 2. Formato: ANCI-XXXX-YYYY
    parts = key.split("-")
    if len(parts) != 3 or len(parts[1]) != 4 or len(parts[2]) != 5:
        return False
    
    p1 = parts[1] # 4 chars
    p2 = parts[2] # 5 chars

    # Verificación matemática
    if (ord(p1[0]) ^ ord(p1[1])) != 0x15:
        return False
    if (ord(p1[2]) + ord(p1[3])) != 150:
        return False
    if ord(p1[0]) != ord('S'):
        return False
    if ord(p1[1]) != (ord('S') ^ 0x15):
        return False
    if ord(p1[2]) != ord('K'):
        return False
    
    # Parte 2: Hash / checksum simple
    expected_sum = 400
    if sum(ord(c) for c in p2) != expected_sum or p2 != "2026!":
        return False

    return True

if __name__ == '__main__':
    user_input = input("Introduce la clave de activación: ").strip()
    if check_key(user_input):
        print(f"[+] ¡Acceso concedido! Bandera: ANCI{{{user_input}}}")
    else:
        print("[-] Clave incorrecta. Acceso denegado.")
