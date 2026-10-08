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

# Construir matriz aumentada [A | Y] mod p de tamaño 20 x 31
M = []
for j in range(num_points):
    x_j, y_j = pairs[j]
    row = [pow(x_j, (num_coeffs - 1) - i, p) for i in range(num_coeffs)] + [y_j % p]
    M.append(row)

# Eliminación Gaussiana en F_p
nrows = num_points
ncols = num_coeffs + 1
pivots = []

r = 0
for c in range(num_coeffs):
    # Buscar pivote no nulo en columna c desde fila r
    pivot_row = None
    for i in range(r, nrows):
        if M[i][c] % p != 0:
            pivot_row = i
            break
    if pivot_row is None:
        continue
    
    # Intercambiar filas
    M[r], M[pivot_row] = M[pivot_row], M[r]
    
    # Normalizar fila pivote
    inv_lead = pow(M[r][c], -1, p)
    for k in range(c, ncols):
        M[r][k] = (M[r][k] * inv_lead) % p
        
    # Eliminar columna c en todas las demás filas
    for i in range(nrows):
        if i != r and M[i][c] % p != 0:
            factor = M[i][c]
            for k in range(c, ncols):
                M[i][k] = (M[i][k] - factor * M[r][k]) % p
                
    pivots.append(c)
    r += 1
    if r == nrows:
        break

print(f"[+] Eliminación Gaussiana mod p completada instantáneamente!")
print(f"[+] Pivotes ({len(pivots)}): {pivots}")
free_vars = [i for i in range(num_coeffs) if i not in pivots]
print(f"[+] Variables libres ({len(free_vars)}): {free_vars}")

# Para cada fila r (pivote pivots[r]):
# c_{pivots[r]} + sum_{k in free_vars} M[r][k] * c_k = M[r][-1] (mod p)
# => sum_{k in free_vars} M[r][k] * c_k - M[r][-1] + c_{pivots[r]} = k_r * p
#
# Construimos un retículo para hallar (c_free, c_pivot):
# Dimensión: len(free_vars) + len(pivots) + 1 = 10 + 20 + 1 = 31

num_free = len(free_vars)
num_piv = len(pivots)
dim = num_free + num_piv + 1
B = 2**256

basis = []

# Filas para c_{free_k}:
for k_idx, free_col in enumerate(free_vars):
    row = [0] * dim
    row[k_idx] = B
    for r_idx in range(num_piv):
        row[num_free + r_idx] = M[r_idx][free_col]
    basis.append(row)

# Filas para múltiplos de p:
for r_idx in range(num_piv):
    row = [0] * dim
    row[num_free + r_idx] = p
    basis.append(row)

# Fila objetivo:
target_row = [0] * dim
for r_idx in range(num_piv):
    target_row[num_free + r_idx] = -M[r_idx][-1]
target_row[-1] = B
basis.append(target_row)

print(f"[*] Base de retículo {len(basis)}x{len(basis[0])} generada.")

# Ahora LLL usando float de alta precisión o mpmath
import mpmath
mpmath.mp.dps = 150 # 150 dígitos decimales de precisión (~500 bits)

def lll_mpmath(B_mat, delta=0.75):
    n = len(B_mat)
    m = len(B_mat[0])
    
    b = [[mpmath.mpf(x) for x in row] for row in B_mat]
    b_int = [list(row) for row in B_mat]
    
    b_star = [[mpmath.mpf(0)] * m for _ in range(n)]
    mu = [[mpmath.mpf(0)] * n for _ in range(n)]
    B_sq = [mpmath.mpf(0)] * n
    
    def update_gs(from_idx=0):
        for i in range(from_idx, n):
            b_star[i] = list(b[i])
            for j in range(i):
                dot_i_j = sum(b[i][k] * b_star[j][k] for k in range(m))
                mu[i][j] = dot_i_j / B_sq[j] if B_sq[j] != 0 else mpmath.mpf(0)
                for k in range(m):
                    b_star[i][k] -= mu[i][j] * b_star[j][k]
            B_sq[i] = sum(b_star[i][k] ** 2 for k in range(m))

    update_gs(0)
    
    k = 1
    step = 0
    delta_mp = mpmath.mpf(delta)
    half_mp = mpmath.mpf(0.5)
    
    while k < n:
        step += 1
        if step % 20 == 0:
            print(f"    [+] LLL progreso: k = {k}/{n}, step = {step}")
            
        for j in range(k - 1, -1, -1):
            if abs(mu[k][j]) > half_mp:
                q = int(mpmath.nint(mu[k][j]))
                if q != 0:
                    for col in range(m):
                        b_int[k][col] -= q * b_int[j][col]
                        b[k][col] -= q * b[j][col]
                    update_gs(k)
                    
        # Lovasz condition
        if B_sq[k] >= (delta_mp - mu[k][k-1]**2) * B_sq[k-1]:
            k += 1
        else:
            b_int[k], b_int[k-1] = b_int[k-1], b_int[k]
            b[k], b[k-1] = b[k-1], b[k]
            update_gs(k - 1)
            k = max(k - 1, 1)
            
    return b_int

print("[*] Ejecutando LLL con mpmath...")
reduced = lll_mpmath(basis)
print("[+] LLL finalizado!")

for row in reduced:
    last = row[-1]
    if abs(last) == B:
        sign = 1 if last == B else -1
        coeffs = [0] * num_coeffs
        for k_idx, free_col in enumerate(free_vars):
            coeffs[free_col] = (sign * row[k_idx]) // B
            
        for r_idx, piv_col in enumerate(pivots):
            coeffs[piv_col] = (sign * row[num_free + r_idx])
            
        print("[+] ¡Vector solución obtenido!")
        c0 = abs(coeffs[0])
        print(f"[+] c_0: {c0}")
        
        key = long_to_bytes(c0, 32)
        try:
            cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv_hex))
            pt = cipher.decrypt(bytes.fromhex(ct_hex))
            flag = unpad(pt, 16).decode('utf-8')
            print("\n" + "="*60)
            print(f"[!] FLAG OBTENIDA: {flag}")
            print("="*60 + "\n")
            with open("challenges/15_lattice_crypto/flag.txt", "w") as out_f:
                out_f.write(flag)
            break
        except Exception as e:
            print(f"[-] Descifrado falló: {e}")
