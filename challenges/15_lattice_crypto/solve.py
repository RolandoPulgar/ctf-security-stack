import os
import re
import ast
import hashlib
from flint import fmpz_mat
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes

# 1. Leer parámetros del desafío
chal_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(chal_dir, "output.txt"), "r") as f:
    text = f.read()

p = int(re.search(r'p\s*=\s*(\d+)', text).group(1))
pairs_raw = re.search(r'pairs\s*=\s*(\[.*?\])\s*enc_flag', text, re.DOTALL).group(1)
pairs = ast.literal_eval(pairs_raw)

enc_flag_raw = re.search(r'enc_flag\s*=\s*(\(.*?\))', text).group(1)
iv_hex, ct_hex = ast.literal_eval(enc_flag_raw)

num_points = 20
num_coeffs = 30

# 2. Construir matriz A (20 x 30) y vector Y (20)
A_rows = []
Y_vals = []
for j in range(num_points):
    x_j, y_j = pairs[j]
    row = [pow(x_j, (num_coeffs - 1) - i, p) for i in range(num_coeffs)]
    A_rows.append(row)
    Y_vals.append(y_j)

# 3. Construcción del retículo de Kannan (dimensión 51x51)
B = 2**256
dim = num_coeffs + num_points + 1

entries = []
for i in range(num_coeffs):
    row = [0] * dim
    row[i] = B
    for j in range(num_points):
        row[num_coeffs + j] = A_rows[j][i]
    entries.extend(row)

for j in range(num_points):
    row = [0] * dim
    row[num_coeffs + j] = p
    entries.extend(row)

target_row = [0] * dim
for j in range(num_points):
    target_row[num_coeffs + j] = -Y_vals[j]
target_row[-1] = B
entries.extend(target_row)

print(f"[*] Reduciendo retículo {dim}x{dim} con C-FLINT LLL...")
M = fmpz_mat(dim, dim, entries)
L = M.lll()
print("[+] LLL completado exitosamente.")

# 4. Extracción de coeficientes y descifrado AES-256-CBC
for r in range(dim):
    row = [int(L[r, c]) for c in range(dim)]
    last = row[-1]
    
    if abs(last) == B:
        sign = 1 if last == B else -1
        c0 = (sign * row[0]) // B
        
        if c0 > 0:
            key = long_to_bytes(c0, 32)
            try:
                cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv_hex))
                pt = cipher.decrypt(bytes.fromhex(ct_hex))
                flag = unpad(pt, 16).decode('utf-8')
                print("=" * 60)
                print(f"FLAG: {flag}")
                print("=" * 60)
                break
            except Exception as e:
                pass
