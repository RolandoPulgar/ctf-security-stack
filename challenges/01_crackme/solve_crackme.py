#!/usr/bin/env python3
"""
Solver Automático para Reto 01 usando Z3 Theorem Prover
Demuestra la resolución matemática asistida por IA en segundos.
"""

from z3 import *

def solve():
    s = Solver()
    
    # 16 caracteres ASCII
    chars = [BitVec(f'c_{i}', 8) for i in range(16)]
    
    # Restricciones ASCII legibles
    for c in chars:
        s.add(c >= 32, c <= 126)
        
    # Prefijo ANCI-
    s.add(chars[0] == ord('A'))
    s.add(chars[1] == ord('N'))
    s.add(chars[2] == ord('C'))
    s.add(chars[3] == ord('I'))
    s.add(chars[4] == ord('-'))
    s.add(chars[9] == ord('-'))
    
    # Lógica de la parte 1 (p1: chars 5, 6, 7, 8)
    s.add(chars[5] == ord('S'))
    s.add(chars[5] ^ chars[6] == 0x15)
    s.add(chars[7] == ord('K'))
    s.add(chars[7] + chars[8] == 150)
    
    # Lógica de la parte 2 (p2: chars 10..14 y 15)
    s.add(chars[10] == ord('2'))
    s.add(chars[11] == ord('0'))
    s.add(chars[12] == ord('2'))
    s.add(chars[13] == ord('6'))
    s.add(chars[14] == ord('!'))
    
    if s.check() == sat:
        m = s.model()
        solution = "".join([chr(m[c].as_long()) for c in chars])
        print("=" * 50)
        print("[+] ¡SOLUCIÓN ENCONTRADA CON Z3!")
        print(f"[+] Clave: {solution}")
        print(f"[+] Bandera: ANCI{{{solution}}}")
        print("=" * 50)
        return solution
    else:
        print("[-] No se encontró solución.")
        return None

if __name__ == '__main__':
    solve()
