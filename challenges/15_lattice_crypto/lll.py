import ast
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes
import numpy as np

# Implementación de LLL (Lenstra-Lenstra-Lovász) en Python puro con precisión entera/racional
def lll_reduction(basis, delta=0.75):
    """
    Algoritmo LLL estándar de reducción de bases de retículos.
    basis: lista de vectores (enteros)
    """
    n = len(basis)
    m = len(basis[0])
    
    # Gram-Schmidt orthogonalization (usando float de alta precisión o fracciones)
    b = [list(map(float, v)) for v in basis]
    b_star = [[0.0]*m for _ in range(n)]
    mu = [[0.0]*n for _ in range(n)]
    
    def gram_schmidt():
        for i in range(n):
            b_star[i] = list(b[i])
            for j in range(i):
                dot_b_bstar = sum(b[i][k] * b_star[j][k] for k in range(m))
                dot_bstar_bstar = sum(b_star[j][k] * b_star[j][k] for k in range(m))
                if dot_bstar_bstar == 0:
                    mu[i][j] = 0.0
                else:
                    mu[i][j] = dot_b_bstar / dot_bstar_bstar
                for k in range(m):
                    b_star[i][k] -= mu[i][j] * b_star[j][k]
                    
    def size_reduce(k, l):
        if abs(mu[k][l]) > 0.5:
            q = round(mu[k][l])
            for i in range(m):
                basis[k][i] -= q * basis[l][i]
                b[k][i] -= q * b[l][i]
            gram_schmidt()

    gram_schmidt()
    k = 1
    while k < n:
        for j in range(k - 1, -1, -1):
            size_reduce(k, j)
            
        # Lovász condition
        dot_k = sum(b_star[k][i]**2 for i in range(m))
        dot_k_prev = sum(b_star[k-1][i]**2 for i in range(m))
        
        if dot_k >= (delta - mu[k][k-1]**2) * dot_k_prev:
            k += 1
        else:
            basis[k], basis[k-1] = basis[k-1], basis[k]
            b[k], b[k-1] = b[k-1], b[k]
            gram_schmidt()
            k = max(k - 1, 1)
            
    return basis

print("[*] Algoritmo LLL compilado.")
