import sys
import re
import ast
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes
import numpy as np

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

M = []
for j in range(num_points):
    x_j, y_j = pairs[j]
    row = [pow(x_j, (num_coeffs - 1) - i, p) for i in range(num_coeffs)] + [y_j % p]
    M.append(row)

# Gauss-Jordan mod p
nrows = num_points
ncols = num_coeffs + 1
pivots = []

r = 0
for c in range(num_coeffs):
    pivot_row = None
    for i in range(r, nrows):
        if M[i][c] % p != 0:
            pivot_row = i
            break
    if pivot_row is None:
        continue
    
    M[r], M[pivot_row] = M[pivot_row], M[r]
    inv_lead = pow(M[r][c], -1, p)
    for k in range(c, ncols):
        M[r][k] = (M[r][k] * inv_lead) % p
        
    for i in range(nrows):
        if i != r and M[i][c] % p != 0:
            factor = M[i][c]
            for k in range(c, ncols):
                M[i][k] = (M[i][k] - factor * M[r][k]) % p
                
    pivots.append(c)
    r += 1
    if r == nrows:
        break

print(f"[+] Gauss mod p listo. Pivotes: {len(pivots)}, Libres: {num_coeffs - len(pivots)}", flush=True)
free_vars = [i for i in range(num_coeffs) if i not in pivots]

num_free = len(free_vars)
num_piv = len(pivots)
dim = num_free + num_piv + 1
B = 2**256

basis = []
for k_idx, free_col in enumerate(free_vars):
    row = [0] * dim
    row[k_idx] = B
    for r_idx in range(num_piv):
        row[num_free + r_idx] = M[r_idx][free_col]
    basis.append(row)

for r_idx in range(num_piv):
    row = [0] * dim
    row[num_free + r_idx] = p
    basis.append(row)

target_row = [0] * dim
for r_idx in range(num_piv):
    target_row[num_free + r_idx] = -M[r_idx][-1]
target_row[-1] = B
basis.append(target_row)

print(f"[*] Base de dimensión {len(basis)}x{len(basis[0])}", flush=True)

def to_float(x):
    shift = 900
    sign = 1 if x >= 0 else -1
    ax = abs(x)
    return sign * ((ax >> shift) + (ax & ((1 << shift) - 1)) / (2.0 ** shift))

def lll_fp(B_mat, delta=0.75):
    n = len(B_mat)
    m = len(B_mat[0])
    b = [list(row) for row in B_mat]
    
    b_float = np.zeros((n, m), dtype=np.float64)
    for i in range(n):
        for j in range(m):
            b_float[i, j] = to_float(b[i][j])
            
    b_star = np.zeros((n, m), dtype=np.float64)
    mu = np.zeros((n, n), dtype=np.float64)
    B_sq = np.zeros(n, dtype=np.float64)

    def update_gs(from_idx=0):
        for i in range(from_idx, n):
            b_star[i] = b_float[i].copy()
            for j in range(i):
                if B_sq[j] > 1e-30:
                    mu[i, j] = np.dot(b_float[i], b_star[j]) / B_sq[j]
                else:
                    mu[i, j] = 0.0
                b_star[i] -= mu[i, j] * b_star[j]
            B_sq[i] = np.dot(b_star[i], b_star[i])

    update_gs(0)
    k = 1
    iterations = 0
    max_iter = 50000
    
    while k < n and iterations < max_iter:
        iterations += 1
        
        # Size reduction
        for j in range(k - 1, -1, -1):
            if abs(mu[k, j]) > 0.5000000001:
                q = int(round(mu[k, j]))
                if q != 0:
                    for col in range(m):
                        b[k][col] -= q * b[j][col]
                    b_float[k] -= q * b_float[j]
                    update_gs(k)
                    
        # Lovasz condition
        if B_sq[k] >= (delta - mu[k, k-1]**2) * B_sq[k-1] - 1e-15:
            k += 1
        else:
            b[k], b[k-1] = b[k-1], b[k]
            b_float[[k-1, k]] = b_float[[k, k-1]]
            update_gs(k - 1)
            k = max(k - 1, 1)
            
    print(f"[+] LLL finalizado en {iterations} iteraciones.", flush=True)
    return b

reduced = lll_fp(basis)

# Verificar descifrado
found = False
for idx, row in enumerate(reduced):
    last = row[-1]
    norm = sum(x**2 for x in row)
    if norm < p**2:
        sign = 1 if last >= 0 else -1
        coeffs = [0] * num_coeffs
        for k_idx, free_col in enumerate(free_vars):
            coeffs[free_col] = (sign * row[k_idx]) // B
            
        for r_idx, piv_col in enumerate(pivots):
            coeffs[piv_col] = (sign * row[num_free + r_idx])
            
        c0 = abs(coeffs[0])
        if c0 != 0 and c0.bit_length() <= 256:
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
                pass

if not found:
    print("[*] Probando todos los elementos de vectores reducidos...", flush=True)
    for row in reduced:
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
