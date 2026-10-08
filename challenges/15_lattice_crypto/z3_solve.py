import re
import ast
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes
import z3

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

print(f"[+] p = {p}")
print(f"[+] Puntos = {num_points}")

# 2. Configurar solver de Z3
s = z3.Solver()

c = [z3.Int(f'c_{i}') for i in range(num_coeffs)]
k = [z3.Int(f'k_{j}') for j in range(num_points)]

# Restricciones de c_i in [0, 2^256)
for i in range(num_coeffs):
    s.add(c[i] >= 0)
    s.add(c[i] < (1 << 256))

# Restricciones lineales para cada punto (x_j, y_j)
for j in range(num_points):
    x_j, y_j = pairs[j]
    # Sum_i c_i * x_j^(29-i) = y_j + k_j * p
    expr = 0
    for i in range(num_coeffs):
        coeff_power = pow(x_j, (num_coeffs - 1) - i, p)
        expr = expr + c[i] * coeff_power
    s.add(expr == y_j + k[j] * p)
    # Rango de k_j
    s.add(k[j] >= 0)
    s.add(k[j] <= 30 * (1 << 256))

print("[*] Verificando modelo con Z3...")
res = s.check()
print(f"[*] Resultado Z3: {res}")

if res == z3.sat:
    m = s.model()
    c0 = m[c[0]].as_long()
    print(f"[+] c_0 encontrado: {c0}")
    
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
    except Exception as e:
        print(f"[-] Descifrado falló: {e}")
else:
    print("[-] No se encontró solución con Z3.")
