# Writeup: Small Private Exponent (Wiener's Continued Fractions Method)

* **Categoría:** Criptografía
* **Plataforma:** picoCTF
* **Dificultad:** Intermedia
* **Flag:** `academy{sm4ll_d_073cf0e5}`

---

## 1. Análisis del Reto

En el código generador se utilizaron dos primos $p$ y $q$ de 1048 bits cada uno ($N \approx 2096$ bits), pero se generó un exponente privado $d$ de solo **256 bits**:
$$d = \text{getPrime}(256)$$
$$e = d^{-1} \pmod{\phi(N)}$$

## 2. Vulnerabilidad

Como $d < \frac{1}{3} N^{1/4}$ ($256 < 524$ bits), se cumple el criterio del **Teorema de Wiener**:
$$\left| \frac{e}{N} - \frac{k}{d} \right| < \frac{1}{2 d^2}$$
La fracción $\frac{k}{d}$ aparece necesariamente como uno de los convergentes en el desarrollo en fracciones continuadas de $\frac{e}{N}$.

## 3. Explotación (Solver)

Implementamos el algoritmo de fracciones continuadas en [solve.py](file:///c:/Users/rpulg/OneDrive/Escritorio/ctf/challenges/10_rsa_small_d/solve.py):
1. Expansión en fracciones continuadas de $\frac{e}{N}$.
2. Generación de cada convergente $(k_i, d_i)$.
3. Validación de $\phi = \frac{e \cdot d - 1}{k}$ y comprobación de las raíces de la ecuación cuadrática $x^2 - (N - \phi + 1)x + N = 0$.
4. Recuperación del exponente privado $d$ y descifrado: $m = c^d \pmod N$.

## 4. Resultado

```text
[+] d encontrado: 93158897719743176499822330425191232938036762646184056124090565452236094983621
[+] FLAG: academy{sm4ll_d_073cf0e5}
```
