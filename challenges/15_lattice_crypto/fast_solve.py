import re
import ast
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes
import sympy as sp
import numpy as np

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

# Construir A (20x30) y Y (20)
A_mat = []
Y_vec = []
for j in range(num_points):
    x_j, y_j = pairs[j]
    row = [pow(x_j, (num_coeffs - 1) - i, p) for i in range(num_coeffs)]
    A_mat.append(row)
    Y_vec.append(y_j)

print("[*] Calculando RREF mod p con SymPy...")
M = sp.Matrix(A_mat)
M_ext = M.row_join(sp.Matrix(Y_vec))
M_rref, pivots = M_ext.rref(iszerofunc=lambda x: x % p == 0)

pivots = list(pivots)
if 30 in pivots:
    pivots.remove(30)

free_vars = [i for i in range(num_coeffs) if i not in pivots]
print(f"[+] Pivots ({len(pivots)}): {pivots}")
print(f"[+] Free variables ({len(free_vars)}): {free_vars}")

R_mod = []
Y_mod = []

for r, piv in enumerate(pivots):
    lead = int(M_rref[r, piv]) % p
    lead_inv = pow(lead, -1, p)
    row_coeffs = [(int(M_rref[r, k]) * lead_inv) % p for k in free_vars]
    y_val = (int(M_rref[r, 30]) * lead_inv) % p
    R_mod.append(row_coeffs)
    Y_mod.append(y_val)

num_free = len(free_vars)
num_piv = len(pivots)
dim = num_free + num_piv + 1

# Bound B = 2^256
B = 2**256

basis = []

# Filas de variables libres
for k in range(num_free):
    row = [0] * dim
    row[k] = B
    for r in range(num_piv):
        row[num_free + r] = R_mod[r][k]
    basis.append(row)

# Filas de mod p
for r in range(num_piv):
    row = [0] * dim
    row[num_free + r] = p
    basis.append(row)

# Fila objetivo
target_row = [0] * dim
for r in range(num_piv):
    target_row[num_free + r] = -Y_mod[r]
target_row[-1] = B
basis.append(target_row)

print(f"[*] Base de dimensión {len(basis)} x {len(basis[0])} construida.")

def lll_incremental(B_in, delta=0.75):
    """
    Standard Lenstra-Lenstra-Lovasz lattice reduction algorithm with incremental updates.
    """
    from fractions import Fraction
    n = len(B_in)
    m = len(B_in[0])
    
    b = [list(row) for row in B_in]
    
    # Gram-Schmidt
    b_star = [[Fraction(0)] * m for _ in range(n)]
    mu = [[Fraction(0)] * n for _ in range(n)]
    B_sq = [Fraction(0)] * n
    
    def compute_gs(i):
        b_star[i] = [Fraction(x) for x in b[i]]
        for j in range(i):
            dot_i_j = sum(b[i][k] * b_star[j][k] for k in range(m))
            mu[i][j] = dot_i_j / B_sq[j] if B_sq[j] != 0 else Fraction(0)
            for k in range(m):
                b_star[i][k] -= mu[i][j] * b_star[j][k]
        B_sq[i] = sum(b_star[i][k] ** 2 for k in range(m))

    for i in range(n):
        compute_gs(i)
        
    k = 1
    step = 0
    while k < n:
        step += 1
        # Size reduction
        for j in range(k - 1, -1, -1):
            if abs(mu[k][j]) > Fraction(1, 2):
                q = round(mu[k][j])
                for col in range(m):
                    b[k][col] -= q * b[j][col]
                # Update GS for k
                compute_gs(k)
                
        # Lovasz condition
        if B_sq[k] >= (Fraction(delta) - mu[k][k-1]**2) * B_sq[k-1]:
            k += 1
        else:
            # Swap b[k] and b[k-1]
            b[k], b[k-1] = b[k-1], b[k]
            # Recompute GS for k-1 and k
            compute_gs(k-1)
            compute_gs(k)
            k = max(k - 1, 1)
            
    return b

print("[*] Iniciando LLL incremental...")
reduced = lll_incremental(basis)
print("[+] LLL incremental finalizado!")

found = False
for row in reduced:
    last = row[-1]
    if abs(last) == B:
        sign = 1 if last == B else -1
        coeffs = [0] * num_coeffs
        for k_idx, free_idx in enumerate(free_vars):
            coeffs[free_idx] = (sign * row[k_idx]) // B
            
        for r_idx, piv_idx in enumerate(pivots):
            c_piv = (sign * row[num_free + r_idx])
            coeffs[piv_idx] = c_piv
            
        print("[+] Vector candidato extraído!")
        c0 = abs(coeffs[0])
        print(f"[+] c_0: {c0}")
        
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
            found = True
            break
        except Exception as e:
            print(f"[-] Descifrado falló: {e}")

if not found:
    print("[*] Probando todos los vectores reducidos...")
    for row in reduced:
        for val in row:
            if val != 0:
                for c_cand in [abs(val), abs(val) // B if abs(val) % B == 0 else 0]:
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
                            found = True
                            break
                        except:
                            pass
        if found:
            break
