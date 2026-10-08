import math
from Crypto.Util.number import long_to_bytes

def continued_fraction(e, n):
    cf = []
    while n != 0:
        q = e // n
        cf.append(q)
        e, n = n, e - q * n
    return cf

def convergents_from_cf(cf):
    convs = []
    n0, d0 = 0, 1
    n1, d1 = 1, 0
    for q in cf:
        n = q * n1 + n0
        d = q * d1 + d0
        convs.append((n, d))
        n0, d0 = n1, d1
        n1, d1 = n, d
    return convs

def is_perfect_square(n):
    if n < 0:
        return False, 0
    root = math.isqrt(n)
    return root * root == n, root

def solve_wiener(e, n, c):
    cf = continued_fraction(e, n)
    convs = convergents_from_cf(cf)
    
    for k, d in convs:
        if k == 0 or d % 2 == 0 or d == 0:
            continue
        
        # ed - 1 = k * phi
        if (e * d - 1) % k != 0:
            continue
            
        phi = (e * d - 1) // k
        
        # Resolviendo x^2 - ((n - phi) + 1)x + n = 0
        s = n - phi + 1
        discriminant = s * s - 4 * n
        
        is_sq, root = is_perfect_square(discriminant)
        if is_sq:
            p = (s + root) // 2
            q = (s - root) // 2
            if p * q == n:
                print(f"[+] d encontrado: {d}")
                m = pow(c, d, n)
                return long_to_bytes(m)
    return None

if __name__ == '__main__':
    # Leer datos del archivo local
    with open("challenges/10_rsa_small_d/data.txt", "r") as f:
        content = f.read()
        
    import re
    n = int(re.search(r'n\s*=\s*(\d+)', content).group(1))
    e = int(re.search(r'e\s*=\s*(\d+)', content).group(1))
    c = int(re.search(r'c\s*=\s*(\d+)', content).group(1))
    
    flag = solve_wiener(e, n, c)
    if flag:
        print("=" * 60)
        print(f"[+] FLAG: {flag.decode('utf-8', errors='ignore')}")
        print("=" * 60)
    else:
        print("[-] No se encontró solución con convergentes directos.")
