# Template: Crypto Solvers (RSA, XOR, Z3)
import math
from Crypto.Util.number import long_to_bytes, inverse

def solve_rsa_fermat(n, e, c):
    """
    Ataque de factorización de Fermat cuando p y q están muy cerca (p ≈ q).
    """
    a = math.isqrt(n)
    if a * a < n:
        a += 1
    while True:
        b2 = a * a - n
        b = math.isqrt(b2)
        if b * b == b2:
            p = a - b
            q = a + b
            break
        a += 1
    
    phi = (p - 1) * (q - 1)
    d = inverse(e, phi)
    m = pow(c, d, n)
    return long_to_bytes(m)

def xor_bytes(data: bytes, key: bytes) -> bytes:
    """XOR byte a byte con repetición de clave."""
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

if __name__ == '__main__':
    print("[*] Módulo de funciones criptográficas listo.")
