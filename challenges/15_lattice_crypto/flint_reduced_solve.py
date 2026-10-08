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

num_points = len(pairs)
num_coeffs = 30

M_aug = []
for j in range(num_points):
    x_j, y_j = pairs[j]
    row = [pow(x_j, (num_coeffs - 1) - i, p) for i in range(num_coeffs)] + [y_j % p]
    M_aug.append(row)

# Gauss-Jordan mod p
nrows = num_points
ncols = num_coeffs + 1
pivots = []

r = 0
for c in range(num_coeffs):
    pivot_row = None
    for i in range(r, nrows):
        if M_aug[i][c] % p != 0:
            pivot_row = i
            break
    if pivot_row is None:
        continue
    
    M_aug[r], M_aug[pivot_row] = M_aug[pivot_row], M_aug[r]
    inv_lead = pow(M_aug[r][c], -1, p)
    for k in range(c, ncols):
        M_aug[r][k] = (M_aug[r][k] * inv_lead) % p
        
    for i in range(nrows):
        if i != r and M_aug[i][c] % p != 0:
            factor = M_aug[i][c]
            for k in range(c, ncols):
                M_aug[i][k] = (M_aug[i][k] - factor * M_aug[r][k]) % p
                
    pivots.append(c)
    r += 1
    if r == nrows:
        break

print(f"[+] Gauss mod p listo. Pivotes ({len(pivots)}), Libres ({num_coeffs - len(pivots)})", flush=True)
free_vars = [i for i in range(num_coeffs) if i not in pivots]

num_free = len(free_vars)
num_piv = len(pivots)
dim = num_free + num_piv + 1
B = 2**256

entries = []

# Filas de variables libres (10 filas)
for k_idx, free_col in enumerate(free_vars):
    row = [0] * dim
    row[k_idx] = B
    for r_idx in range(num_piv):
        row[num_free + r_idx] = M_aug[r_idx][free_col]
    entries.extend(row)

# Filas de mod p (20 filas)
for r_idx in range(num_piv):
    row = [0] * dim
    row[num_free + r_idx] = p
    entries.extend(row)

# Fila objetivo (1 fila)
target_row = [0] * dim
for r_idx in range(num_piv):
    target_row[num_free + r_idx] = -M_aug[r_idx][-1]
target_row[-1] = B
entries.extend(target_row)

print(f"[*] Base 31x31 construida. Ejecutando FLINT LLL...", flush=True)
M = fmpz_mat(dim, dim, entries)
L = M.lll()
print("[+] FLINT LLL 31x31 completado!", flush=True)

found = False
for r in range(dim):
    row = [int(L[r, c]) for c in range(dim)]
    last = row[-1]
    if abs(last) == B:
        sign = 1 if last == B else -1
        coeffs = [0] * num_coeffs
        for k_idx, free_col in enumerate(free_vars):
            coeffs[free_col] = (sign * row[k_idx]) // B
            
        for r_idx, piv_col in enumerate(pivots):
            coeffs[piv_col] = (sign * row[num_free + r_idx])
            
        c0 = abs(coeffs[0])
        print(f"[+] c_0 candidato: {c0}", flush=True)
        if 0 < c0 < 2**256:
            key = long_to_bytes(c0, 32)
            try:
                cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv_hex))
                pt = cipher.decrypt(bytes.fromhex(ct_hex))
                flag = unpad(pt, 16).decode('utf-8')
                print("\n" + "="*60, flush=True)
                print(f"[!] ¡FLAG ENCONTRADA!: {flag}", flush=True)
                print("="*60 + "\n", flush=True)
                with open("challenges/15_lattice_crypto/flag.txt", "w") as out_f:
                    out_f.write(flag)
                found = True
                break
            except Exception as e:
                print(f"[-] Descifrado con c_0 falló: {e}", flush=True)

if not found:
    print("[*] Buscando en todas las filas...", flush=True)
    for r in range(dim):
        row = [int(L[r, c]) for c in range(dim)]
        for val in row:
            for c_cand in [abs(val), abs(val) // B if abs(val) % B == 0 else 0]:
                if 0 < c_cand < 2**256:
                    key = long_to_bytes(c_cand, 32)
                    try:
                        cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv_hex))
                        pt = cipher.decrypt(bytes.fromhex(ct_hex))
                        flag = unpad(pt, 16).decode('utf-8')
                        print("\n" + "="*60, flush=True)
                        print(f"[!] ¡FLAG ENCONTRADA!: {flag}", flush=True)
                        print("="*60 + "\n", flush=True)
                        with open("challenges/15_lattice_crypto/flag.txt", "w") as out_f:
                            out_f.write(flag)
                        found = True
                        break
                    except:
                        pass
            if found:
                break
        if found:
            break
