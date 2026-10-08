# Writeup: Secretos compartidos (Diffie-Hellman Key Exchange Leak)

* **Categoría:** Criptografía
* **Plataforma:** picoCTF
* **Dificultad:** Fácil
* **Flag:** `academy{dh_s3cr3t_5d9c8fbe}`

---

## 1. Análisis del Reto

En el archivo `encryption.py` se observa la implementación estándar del protocolo de intercambio de claves **Diffie-Hellman**:
* Parámetros públicos: $g = 2$, $p$ (número primo de 1048 bits).
* Clave pública del servidor: $A = g^a \pmod p$ (donde $a$ es la clave privada del servidor).
* Clave pública del cliente: $B = g^b \pmod p$ (donde $b$ es la clave privada del cliente).
* Secreto compartido: $S = A^b \pmod p = (g^a)^b \pmod p = g^{ab} \pmod p$.

El mensaje se cifró mediante una operación XOR byte a byte utilizando como máscara el valor de `shared % 256`.

## 2. Vulnerabilidad

El archivo de fuga `message.txt` expuso directamente:
* El módulo primo $p$.
* La clave pública del servidor $A$.
* **La clave privada del cliente $b$** (fuga crítica de credencial/secreto).

Conocidos $A$, $b$ y $p$, cualquier observador puede calcular directamente el secreto compartido sin necesidad de resolver el problema del logaritmo discreto:
$$S = A^b \pmod p$$

## 3. Explotación (Solver)

Ejecutamos el script [solve.py](file:///c:/Users/rpulg/OneDrive/Escritorio/ctf/challenges/02_secretos_compartidos/solve.py):

```python
shared = pow(A, b, p)
key_byte = shared % 256
enc_bytes = bytes.fromhex(enc_hex)
flag = bytes([x ^ key_byte for x in enc_bytes]).decode()
```

## 4. Resultado

Bandera extraída en **0.01 segundos**:
`academy{dh_s3cr3t_5d9c8fbe}`
