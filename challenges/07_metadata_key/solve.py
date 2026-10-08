import re
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5

# 1. Leer imagen y extraer la clave hex
with open("challenges/image (1).jpg", "rb") as f:
    img_data = f.read()

# Buscar la secuencia hex que empieza con 2d2d2d2d2d (-----BEGIN PRIVATE KEY-----)
hex_match = re.search(rb'(?:R|r)?(2d2d2d2d2d424547494e2050524956415445204b4559[0-9a-fA-F\n\r]+2d2d2d2d2d454e442050524956415445204b45592d2d2d2d2d[0-9a-fA-F\n\r]*)', img_data)

if not hex_match:
    # Buscar cualquier bloque hex grande
    hex_match = re.search(rb'(2d2d2d2d2d[0-9a-fA-F\r\n]+)', img_data)

raw_hex = hex_match.group(1).decode('utf-8').replace('\n', '').replace('\r', '')
pem_key = bytes.fromhex(raw_hex)

print("[+] Clave Privada PEM recuperada:")
print(pem_key.decode('utf-8'))

# Guardar la clave privada
with open("challenges/07_metadata_key/private.pem", "wb") as f:
    f.write(pem_key)

# 2. Leer archivo flag (1).enc
with open("challenges/flag (1).enc", "rb") as f:
    enc_data = f.read()

key = RSA.import_key(pem_key)

# Probar PKCS1_OAEP
try:
    cipher_oaep = PKCS1_OAEP.new(key)
    decrypted_oaep = cipher_oaep.decrypt(enc_data)
    print("=" * 50)
    print(f"[+] FLAG (OAEP): {decrypted_oaep.decode('utf-8', errors='ignore')}")
    print("=" * 50)
except Exception as e:
    print(f"[-] Falló OAEP: {e}")

# Probar PKCS1_v1_5
try:
    cipher_v15 = PKCS1_v1_5.new(key)
    decrypted_v15 = cipher_v15.decrypt(enc_data, None)
    if decrypted_v15:
        print("=" * 50)
        print(f"[+] FLAG (PKCS1_v1_5): {decrypted_v15.decode('utf-8', errors='ignore')}")
        print("=" * 50)
except Exception as e:
    print(f"[-] Falló PKCS1_v1_5: {e}")

# Probar RSA directo (raw textbook)
try:
    c = int.from_bytes(enc_data, 'big')
    m = pow(c, key.d, key.n)
    raw_pt = m.to_bytes((m.bit_length() + 7) // 8, 'big')
    print(f"[+] Raw RSA Decrypt: {raw_pt}")
except Exception as e:
    print(f"[-] Falló Raw RSA: {e}")
