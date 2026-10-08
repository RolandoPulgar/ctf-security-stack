# Writeup: Secure Dot Product (SHA-512 Length Extension Attack & Linear System Solver)

* **Categoría:** Criptografía
* **Plataforma:** picoCTF
* **Dificultad:** Difícil (Hard)
* **Flag:** `academy{n0t_so_s3cure_.x_w1th_sh@512_41e4af34}`

---

## 1. Análisis del Reto

El servidor implementa un servicio de "Producto Punto Seguro" que calcula $\vec{v} \cdot \vec{k}$ donde $\vec{k}$ es la clave secreta de 32 bytes utilizada para cifrar la bandera mediante AES-256-CBC.

Para evitar que el usuario filtre la clave enviando la base canónica ($[1,0,\dots]$), el servidor solo acepta vectores que coincidan con un hash firmado con una sal secreta:
$$\text{hash} = \text{SHA-512}(\text{salt} \parallel \text{vector\_encoding})$$
donde $\text{SALT\_SIZE} = 256$ bytes.

El servidor entrega 5 pares iniciales $(\vec{v}_i, \text{hash}_i)$ que él considera "confiables".

## 2. Vulnerabilidad

1. **SHA-512 Length Extension Attack:**
   * La función de hash SHA-512 utiliza la construcción Merkle-Damgård.
   * Al conocer el tamaño de la sal ($256$ bytes), el mensaje original y su hash $\text{SHA-512}(\text{salt} \parallel \text{orig})$, es posible forjar un hash válido para cualquier extensión $\text{ext}$ sin conocer la sal secreta:
     $$\text{new\_hash} = \text{SHA-512}(\text{salt} \parallel \text{orig} \parallel \text{padding} \parallel \text{ext})$$
2. **Discrepancia entre Validación y Sanitización:**
   * El validador calcula el hash sobre el string completo con padding.
   * El parser (`ast.literal_eval`) descarta los bytes no numéricos del padding y construye una lista válida con los números extendidos.

## 3. Explotación (Solver)

Script implementado en [solve_full.py](file:///c:/Users/rpulg/OneDrive/Escritorio/ctf/challenges/14/solve_full.py) y [sha512_ext.py](file:///c:/Users/rpulg/OneDrive/Escritorio/ctf/challenges/14/sha512_ext.py):
1. Conectamos al socket remoto y recolectamos el $\text{IV}$, $\text{Ciphertext}$ y los 5 vectores base.
2. Mediante el ataque de extensión de longitud sobre SHA-512, enviamos múltiples vectores forjados con coeficientes variados para obtener 32 ecuaciones lineales independientes:
   $$M \cdot \vec{k} = \vec{y}$$
3. Resolvemos el sistema lineal por mínimos cuadrados exactos para recuperar la clave AES de 32 bytes:
   $$\vec{k} = \text{0x7ad26c0694820e44900f41d09f103103591cecc44b049da3e4b648fb029fe2b8}$$
4. Desciframos el texto con AES-256-CBC y obtenemos la bandera.

## 4. Resultado

```text
[+] RANGO COMPLETO 32 ALCANZADO (Intento #2)
[+] CLAVE AES (HEX): 7ad26c0694820e44900f41d09f103103591cecc44b049da3e4b648fb029fe2b8
[+] FLAG: academy{n0t_so_s3cure_.x_w1th_sh@512_41e4af34}
```
