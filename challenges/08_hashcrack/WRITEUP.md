# Writeup: Hashcrack (MD5, SHA-1, SHA-256 Multi-round Cracking)

* **Categoría:** Criptografía
* **Plataforma:** picoCTF
* **Dificultad:** Fácil
* **Flag:** `academy{UseStr0nG_h@shEs_&PaSswDs!_062c2b77}`

---

## 1. Análisis del Reto

El servidor interactivo nos presenta 3 rondas consecutivas de autenticación basada en hashes débiles sin salting (salt):

1. **Ronda 1 (MD5 - 32 caracteres hex):**
   * Hash: `482c811da5d5b4bc6d497ffa98491e38`
   * Texto plano: `password123`
2. **Ronda 2 (SHA-1 - 40 caracteres hex):**
   * Hash: `b7a875fc1ea228b9061041b7cec4bd3c52ab3ce3`
   * Texto plano: `letmein`
3. **Ronda 3 (SHA-256 - 64 caracteres hex):**
   * Hash: `916e8c4f79b25028c9e467f1eb8eee6d6bbdff965f9928310ad30a8d88697745`
   * Texto plano: `qwerty098`

## 2. Explotación (Solver Automatizado)

Conectamos un socket TCP automatizado con [solve_hashcrack.py](file:///c:/Users/rpulg/OneDrive/Escritorio/ctf/challenges/08_hashcrack/solve_hashcrack.py) que identifica la longitud de cada hash y envía la contraseña correspondiente en tiempo real:

```python
s.connect((HOST, PORT))
# Ronda 1 -> Envía "password123"
# Ronda 2 -> Envía "letmein"
# Ronda 3 -> Envía "qwerty098"
```

## 3. Resultado

```text
Correct! You've cracked the SHA-256 hash with a secret found. 
The flag is: academy{UseStr0nG_h@shEs_&PaSswDs!_062c2b77}
```
