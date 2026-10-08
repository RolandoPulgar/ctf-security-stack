# Writeup: RSA Key Extraction from Image Metadata & Decryption

* **Categoría:** Criptografía & Forense
* **Plataforma:** picoCTF
* **Dificultad:** Fácil / Media
* **Flag:** `academy{rs4_k3y_1n_1mg_9db27b2c}`

---

## 1. Análisis del Reto

Se proporcionaron dos archivos:
1. `image (1).jpg`: Imagen en formato JPEG.
2. `flag (1).enc`: Archivo binario de 256 bytes (correspondiente a un bloque cifrado con RSA de 2048 bits).

Pistas:
* *Metadata can tell you more than you expect.*
* *Hex can be turned back into a key file.*

## 2. Detección y Extracción

Al inspeccionar las cadenas y metadatos de `image (1).jpg` con nuestro script de triage, descubrimos un bloque de texto hexadecimal extenso que comienza con `2d2d2d2d2d424547494e2050524956415445204b4559...`.

Al convertir esa cadena hexadecimal a texto ASCII:
* `2d 2d 2d 2d 2d` = `-----`
* `42 45 47 49 4e 20 50 52 49 56 41 54 45 20 4b 45 59` = `BEGIN PRIVATE KEY`

Se recuperó íntegramente la **clave privada RSA PEM** de 2048 bits.

## 3. Explotación (Solver)

Con la clave privada RSA recuperada, utilizamos `PKCS1_v1_5` de `pycryptodome` para descifrar `flag (1).enc`:

```python
key = RSA.import_key(pem_key)
cipher = PKCS1_v1_5.new(key)
flag = cipher.decrypt(enc_data, None).decode().strip()
```

## 4. Resultado

Bandera descifrada en **0.02 segundos**:
`academy{rs4_k3y_1n_1mg_9db27b2c}`
