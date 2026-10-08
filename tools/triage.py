#!/usr/bin/env python3
"""
Triage Automático de Artefactos de CTF & Forense
Uso: python triage.py <archivo_o_directorio>
"""

import sys
import os
import re
import hashlib
import binascii

FLAG_PATTERNS = [
    rb'(?i)(?:flag|anci|hackrocks|ctf)\{[^\{\}\n\r]+\}',
    rb'(?i)[a-z0-9_]{3,20}\{[a-z0-9_\-\.\!\@\#\$\%\^\&\*\(\)\+]{4,80}\}',
]

def analyze_file(filepath):
    if not os.path.exists(filepath):
        print(f"[-] Archivo no encontrado: {filepath}")
        return

    print("=" * 60)
    print(f"[*] ANALIZANDO ARTEFACTO: {os.path.basename(filepath)}")
    print("=" * 60)

    size = os.path.getsize(filepath)
    print(f"[+] Tamaño: {size} bytes ({size / 1024:.2f} KB)")

    with open(filepath, 'rb') as f:
        data = f.read()

    # Hashes
    md5 = hashlib.md5(data).hexdigest()
    sha256 = hashlib.sha256(data).hexdigest()
    print(f"[+] MD5   : {md5}")
    print(f"[+] SHA256: {sha256}")

    # Magic bytes check
    magic = data[:16]
    print(f"[+] Header Hex: {magic.hex(' ')}")

    file_type = "Desconocido / Binario Genérico"
    if data.startswith(b'\x7fELF'):
        file_type = "Linux ELF Executable"
    elif data.startswith(b'MZ'):
        file_type = "Windows PE / EXE"
    elif data.startswith(b'\x89PNG\r\n\x1a\n'):
        file_type = "Imagen PNG"
    elif data.startswith(b'\xff\xd8\xff'):
        file_type = "Imagen JPEG"
    elif data.startswith(b'PK\x03\x04'):
        file_type = "Archivo ZIP / DOCX / APK"
    elif data.startswith(b'%PDF'):
        file_type = "Documento PDF"
    elif data.startswith(b'\xd4\xc3\xb2\xa1') or data.startswith(b'\n\r\r\n'):
        file_type = "Captura de Red PCAP / PCAPNG"
    elif b'<!DOCTYPE html>' in data[:100] or b'<html' in data[:100]:
        file_type = "Documento HTML"
    
    print(f"[+] Tipo Detectado: {file_type}")

    # Flag hunting
    print("\n[*] Buscando patrones de Flags...")
    found_flags = []
    for pattern in FLAG_PATTERNS:
        matches = re.findall(pattern, data)
        for m in matches:
            decoded = m.decode('utf-8', errors='ignore')
            if decoded not in found_flags:
                found_flags.append(decoded)

    if found_flags:
        print("[!] BANDERAS O POSIBLES MATCHES ENCONTRADOS:")
        for flag in found_flags:
            print(f"    🚩 {flag}")
    else:
        print("[-] No se encontraron banderas en texto plano.")

    # Base64 strings hunting
    b64_matches = re.findall(rb'[A-Za-z0-9+/]{20,}={0,2}', data)
    if b64_matches:
        print(f"\n[*] Strings Base64 detectadas ({len(b64_matches)}):")
        for b64 in b64_matches[:5]:
            try:
                decoded = binascii.a2b_base64(b64)
                if any(c > 31 and c < 127 for c in decoded):
                    print(f"    Raw: {b64[:40].decode()}... -> Decoded: {decoded[:40]}")
            except Exception:
                pass

    print("=" * 60)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python triage.py <archivo>")
        sys.exit(1)
    analyze_file(sys.argv[1])
