# Writeup: Two is Prime (Weak RSA Modulus Factorization)

* **Categoría:** Criptografía
* **Plataforma:** picoCTF
* **Dificultad:** Fácil
* **Flag:** `academy{tw0_1$_pr!m3d832b35c}`

---

## 1. Análisis del Reto

El reto nos proporciona un servicio interactivo que genera una clave RSA con módulo $N$ y exponente $e = 65537$, y nos entrega el texto cifrado $c$:
* $N = p \cdot q$
* $c = m^e \pmod N$

## 2. Vulnerabilidad

Al inspeccionar el valor de $N$, se observa que termina en número par (el último dígito es `2`).
Por lo tanto, uno de los factores primos de $N$ es trivialmente **$p = 2$** (el único número primo par).
$$q = \frac{N}{2}$$
$$\phi(N) = (p - 1)(q - 1) = (2 - 1)(q - 1) = q - 1$$

## 3. Explotación (Solver)

Calculamos el exponente privado $d$:
$$d = e^{-1} \pmod{\phi(N)}$$
$$m = c^d \pmod N$$

Script implementado en [solve_rsa.py](file:///c:/Users/rpulg/OneDrive/Escritorio/ctf/challenges/09_rsa_factoring/solve_rsa.py).

## 4. Resultado

Bandera obtenida en **0.01 segundos**:
`academy{tw0_1$_pr!m3d832b35c}`
