# Reto 15 - Lattice Cryptography (Hidden Number Problem / Small Coefficient Polynomial)

## 📌 Metadatos del Desafío
* **Categoría:** Cryptography (Hard / Lattices)
* **Plataforma:** HackRocks / CTF
* **Archivos provistos:** `chall.py`, `output.txt`
* **Hint:** "What are lattices?"
* **Estado:** ✅ Resuelto
* **Bandera:** `academy{MSS_Advance_but_we_brought_it_back_and_made_it_harder!!!}`

---

## 🔍 Análisis de la Vulnerabilidad y Criptosistema

### 1. Mecanismo del Reto (`chall.py`)
1. Se genera un primo de 1024 bits $p$.
2. Se define un polinomio de grado 29 con 30 coeficientes $c_0, c_1, \dots, c_{29}$:
   $$P(x) = \sum_{i=0}^{29} c_i \cdot x^{29-i} \pmod p$$
   donde cada coeficiente $c_i$ es una salida de SHA-256 ($0 \le c_i < 2^{256}$):
   * $c_0 = \text{bytes\_to\_long}(\text{SHA256}(\text{flag}))$
   * $c_{i+1} = \text{bytes\_to\_long}(\text{SHA256}(\text{long\_to\_bytes}(c_i)))$
3. Se entregan $m = 20$ pares de evaluación $(x_j, y_j)$ donde $y_j = P(x_j) \pmod p$.
4. La bandera está cifrada con **AES-256-CBC** usando como clave `MASTER_KEY = long_to_bytes(c_0)` y vector de inicialización `IV = b"\x00"*16`.

### 2. Formulación Matemática del Problema
Tenemos un sistema lineal indeterminado de 20 ecuaciones con 30 incógnitas sobre el cuerpo $\mathbb{Z}_p$:
$$y_j \equiv \sum_{i=0}^{29} c_i \cdot x_j^{29-i} \pmod p \quad (j = 0, \dots, 19)$$

La vulnerabilidad crítica radica en que **todos los coeficientes $c_i$ son pequeños** en comparación con el módulo $p$:
$$c_i < 2^{256} \ll p \approx 2^{1024}$$

Esto corresponde a una variante del **Hidden Number Problem (HNP)** y se modela como un problema del vector más corto (SVP / CVP) en retículos (**Lattices**) mediante la técnica de **Kannan's Embedding**.

---

## 🛠️ Construcción del Retículo (Kannan's Embedding)

Se construye una matriz base de retículo $M \in \mathbb{Z}^{51 \times 51}$ con cota $B = 2^{256}$:
1. **Filas de coeficientes (30 filas):** Representan la contribución de cada $c_i$ ponderada por $B$ y sus potencias $x_j^{29-i}$.
2. **Filas mod $p$ (20 filas):** Representan las reducciones modulares enteras $k_j \cdot p$.
3. **Fila objetivo (1 fila):** Contiene los valores evaluados $-y_j$ y un término libre $B$.

$$
M = \begin{pmatrix}
B \cdot I_{30} & A^T & 0 \\
0 & p \cdot I_{20} & 0 \\
0 & -Y^T & B
\end{pmatrix}
$$

Al aplicar el algoritmo de reducción de bases **LLL (Lenstra–Lenstra–Lovász)** implementado en C a través de la librería `python-flint` (`fmpz_mat.lll()`), el vector solución:
$$v = (c_0 B, c_1 B, \dots, c_{29} B, 0, \dots, 0, B)$$
es revelado como el vector más corto del retículo.

---

## 🚀 Solución y Extracción de la Bandera

### Ejecución del Solver:
```bash
python challenges/15_lattice_crypto/solve.py
```

### Salida:
```text
[*] Reduciendo retículo 51x51 con C-FLINT LLL...
[+] LLL completado exitosamente.
============================================================
FLAG: academy{MSS_Advance_but_we_brought_it_back_and_made_it_harder!!!}
============================================================
```

---

## 🛡️ Lecciones y Mitigaciones
1. **Insuficiencia de Grado vs Información:** Proveer 20 evaluaciones en un polinomio con coeficientes de 256 bits sobre $\mathbb{F}_{1024}$ filtra más de $20 \times (1024 - 256) = 15360$ bits de información, permitiendo a LLL recuperar todos los coeficientes unívocamente.
2. **Defensa:** Para ocultar polinomios secretos mediante evaluaciones públicas, los coeficientes deben ser seleccionados uniformemente al azar en el rango completo $[0, p-1]$.
