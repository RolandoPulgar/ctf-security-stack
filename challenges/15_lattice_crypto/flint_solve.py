import re
import ast
import hashlib
from flint import fmpz_mat, fmpz
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes

# 1. Leer datos de output.txt
with open("challenges/15_lattice_crypto/output.txt", "r") as f:
    text = f.read()

p = int(re.search(r'p\s*=\s*(\d+)', text).group(1))
pairs_raw = re.search(r'pairs\s*=\s*(\[.*?\])\s*enc_flag', text, re.DOTALL).group(1)
pairs = ast.literal_eval(pairs_raw)

enc_flag_raw = re.search(r'enc_flag\s*=\s*(\(.*?\))', text).group(1)
iv_hex, ct_hex = ast.literal_eval(enc_flag_raw)

num_points = 20
num_coeffs = 30

# Construir matriz A (20 x 30) y vector Y (20)
A_rows = []
Y_vals = []
for j in range(num_points):
    x_j, y_j = pairs[j]
    row = [pow(x_j, (num_coeffs - 1) - i, p) for i in range(num_coeffs)]
    A_rows.append(row)
    Y_vals.append(y_j)

# Bound B = 2^256
B = 2**256
dim = num_coeffs + num_points + 1

print(f"[*] Construyendo retículo de dimensión {dim}x{dim}...")

entries = []
# 1. Filas de coeficientes c_i (30 filas)
for i in range(num_coeffs):
    row = [0] * dim
    row[i] = B
    for j in range(num_points):
        row[num_coeffs + j] = A_rows[j][i]
    entries.extend(row)

# 2. Filas de mod p (20 filas)
for j in range(num_points):
    row = [0] * dim
    row[num_coeffs + j] = p
    entries.extend(row)

# 3. Fila objetivo (1 fila)
target_row = [0] * dim
for j in range(num_points):
    target_row[num_coeffs + j] = -Y_vals[j]
target_row[-1] = B
entries.extend(target_row)

# Crear matriz FLINT
M = fmpz_mat(dim, dim, entries)

print("[*] Ejecutando LLL con FLINT en C...")
L = M.lll()
print("[+] ¡Reducción LLL completada!")

found_flag = False
# Inspeccionar filas de L
for r in range(dim):
    row = [int(L[r, c]) for c in range(dim)]
    last = row[-1]
    
    if abs(last) == B:
        sign = 1 if last == B else -1
        coeffs_recovered = []
        for i in range(num_coeffs):
            c_i = (sign * row[i]) // B
            coeffs_recovered.append(c_i)
            
        c0 = coeffs_recovered[0]
        print(f"[+] Candidato c_0 encontrado: {c0}")
        
        key = long_to_bytes(c0, 32)
        try:
            cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv_hex))
            pt = cipher.decrypt(bytes.fromhex(ct_hex))
            flag = unpad(pt, 16).decode('utf-8')
            print("\n" + "="*60)
            print(f"[!] ¡FLAG ENCONTRADA!: {flag}")
            print("="*60 + "\n")
            with open("challenges/15_lattice_crypto/flag.txt", "w") as out_f:
                out_f.write(flag)
            found_flag = True
            break
        except Exception as e:
            print(f"[-] Descifrado con c0 falló: {e}")

if not found_flag:
    print("[*] Buscando vectores cortos alternativos...")
    for r in range(dim):
        row = [int(L[r, c]) for c in range(dim)]
        for val in row[:num_coeffs]:
            if val != 0 and abs(val) < p:
                for c_cand in [abs(val) // B if abs(val) % B == 0 else abs(val)]:
                    if 0 < c_cand < 2**256:
                        key = long_to_bytes(c_cand, 32)
                        try:
                            cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv_hex))
                            pt = cipher.decrypt(bytes.fromhex(ct_hex))
                            flag = unpad(pt, 16).decode('utf-8')
                            print("\n" + "="*60)
                            print(f"[!] ¡FLAG ENCONTRADA!: {flag}")
                            print("="*60 + "\n")
                            with open("challenges/15_lattice_crypto/flag.txt", "w") as out_f:
                                out_f.write(flag)
                            found_flag = True
                            break
                        except:
                            pass
        if found_flag:
            break
