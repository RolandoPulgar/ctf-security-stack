from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

target_hex = "f4de02cdd646ec8434da64338ea3088b19782037a143d83710869e38ec9f690e"
ct_bytes = bytes.fromhex(target_hex)

base_ts = 1790147510
window = 200000 # +/- 200,000 segundos (varios días de margen)

print(f"[*] Iniciando fuerza bruta de timestamp alrededor de {base_ts}...")

found = False
for offset in range(-window, window + 1):
    ts = base_ts + offset
    key = sha256(str(ts).encode()).digest()[:16]
    
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(ct_bytes)
    
    if b"academy{" in decrypted or b"picoCTF{" in decrypted or b"flag{" in decrypted:
        try:
            flag = unpad(decrypted, AES.block_size).decode('utf-8', errors='ignore')
        except Exception:
            flag = decrypted.decode('utf-8', errors='ignore')
        print("=" * 50)
        print(f"[+] ¡TIMESTAMP EXACTO ENCONTRADO!: {ts} (offset: {offset})")
        print(f"[+] LLAVE: {key.hex()}")
        print(f"[+] FLAG: {flag}")
        print("=" * 50)
        found = True
        break

if not found:
    print("[-] No se encontró en la ventana especificada, ampliando búsqueda...")
