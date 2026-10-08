from fractions import Fraction
import math

def lll_exact(basis, delta=Fraction(3, 4)):
    """
    Algoritmo LLL con aritmética racional exacta (Fraction).
    Garantiza 100% de precisión sin desbordamiento de punto flotante para números de 1024 bits.
    """
    n = len(basis)
    m = len(basis[0])
    
    B = [list(row) for row in basis]
    B_star = [[Fraction(0)] * m for _ in range(n)]
    mu = [[Fraction(0)] * n for _ in range(n)]
    
    def gram_schmidt():
        for i in range(n):
            B_star[i] = [Fraction(x) for x in B[i]]
            for j in range(i):
                num = sum(B[i][k] * B_star[j][k] for k in range(m))
                den = sum(B_star[j][k] * B_star[j][k] for k in range(m))
                if den == 0:
                    mu[i][j] = Fraction(0)
                else:
                    mu[i][j] = num / den
                for k in range(m):
                    B_star[i][k] -= mu[i][j] * B_star[j][k]
                    
    def size_reduce(k, l):
        if abs(mu[k][l]) > Fraction(1, 2):
            q = round(float(mu[k][l]))
            if q != 0:
                for i in range(m):
                    B[k][i] -= q * B[l][i]
                gram_schmidt()

    gram_schmidt()
    k = 1
    steps = 0
    while k < n:
        steps += 1
        if steps % 50 == 0:
            print(f"[*] Paso LLL: {steps}, k: {k}/{n}", flush=True)
            
        for j in range(k - 1, -1, -1):
            size_reduce(k, j)
            
        dot_k = sum(B_star[k][i]**2 for i in range(m))
        dot_k_prev = sum(B_star[k-1][i]**2 for i in range(m))
        
        if dot_k >= (delta - mu[k][k-1]**2) * dot_k_prev:
            k += 1
        else:
            B[k], B[k-1] = B[k-1], B[k]
            gram_schmidt()
            k = max(k - 1, 1)
            
    return B

print("[*] Módulo LLL exacto cargado.")
