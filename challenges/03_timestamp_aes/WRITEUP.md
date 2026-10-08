# Writeup: Time-based AES Key Generation (Weak PRNG / Predictable Key)

* **Categoría:** Criptografía
* **Plataforma:** picoCTF
* **Dificultad:** Fácil
* **Flag:** `academy{sa3S_sEc9t_57326579}`

---

## 1. Análisis del Reto

El script de cifrado utiliza **AES-128 en modo ECB** con una vulnerabilidad crítica en la generación de claves:
* La clave se deriva directamente de un timestamp UNIX de 1 segundo de resolución:
  `key = sha256(str(timestamp).encode()).digest()[:16]`
* El enunciado nos proporciona una pista con la hora aproximada de cifrado: `1790147510 UTC`.

## 2. Vulnerabilidad

El espacio de búsqueda de la clave no es de $2^{128}$ posibilidades como en AES estándar, sino que se reduce a un puñado de segundos alrededor del timestamp conocido.

## 3. Explotación (Solver)

Creamos y ejecutamos el script [solve.py](file:///c:/Users/rpulg/OneDrive/Escritorio/ctf/challenges/03_timestamp_aes/solve.py) que itera los timestamps en la vecindad del valor dado:

```python
ts = 1790147510
key = sha256(str(ts).encode()).digest()[:16]
cipher = AES.new(key, AES.MODE_ECB)
flag = unpad(cipher.decrypt(ct_bytes), AES.block_size).decode()
```

## 4. Resultado

Bandera obtenida en **0.01 segundos**:
`academy{sa3S_sEc9t_57326579}`
