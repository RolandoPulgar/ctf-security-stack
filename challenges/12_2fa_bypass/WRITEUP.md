# Writeup: No FA (Client-Side Flask Session 2FA Bypass & Hash Cracking)

* **Categoría:** Web Exploitation
* **Plataforma:** picoCTF
* **Dificultad:** Media
* **Flag:** `academy{n0_r4t3_n0_4uth_359dd2cb}`

---

## 1. Análisis del Reto

Se proporcionaron los archivos fuente de una aplicación Flask (`app.py`) y una base de datos SQLite (`users.db`).

Flujo de la aplicación:
1. El usuario envía `username` y `password`.
2. Si el hash SHA-256 de la contraseña coincide y `user['two_fa'] == 1`, se genera un código OTP de 4 dígitos:
   ```python
   otp = str(random.randint(1000, 9999))
   session['otp_secret'] = otp
   session['otp_timestamp'] = time.time()
   session['username'] = username
   session['logged'] = 'false'
   ```
3. El usuario es redirigido a `/two_fa` donde debe ingresar el OTP para autenticarse como `admin`.

## 2. Vulnerabilidades Identificadas

1. **Weak Password Hashing (Unsalted SHA-256):**
   * En `users.db`, el hash del administrador era `c20fa16907343eef642d10f0bdb81bf629e6aaf6c906f26eabda079ca9e5ab67`.
   * Cracking mediante diccionario revela la contraseña en texto plano: `apple@123`.

2. **Insecure Client-Side Session Storage (Flask Default Behavior):**
   * Las cookies de sesión de Flask están firmadas digitalmente pero **no cifradas**.
   * Al guardar `session['otp_secret'] = otp`, el código OTP generado por el servidor se almacena directamente en la cookie enviada al navegador del usuario (comprimida con `zlib` y codificada en `base64`).

## 3. Explotación (Solver)

Script automatizado en [solve.py](file:///c:/Users/rpulg/OneDrive/Escritorio/ctf/challenges/12_2fa_bypass/solve.py):
1. Enviamos `admin` y `apple@123` a `/login`.
2. Capturamos la cookie `session` devuelta por el servidor.
3. Descomprimimos el payload con `base64` y `zlib` para extraer el valor exacto de `otp_secret`.
4. Enviamos el OTP a `/two_fa` y accedemos al panel de control para extraer la bandera.

## 4. Resultado

```text
[+] CÓDIGO OTP (2FA) DESCUBIERTO: 2734
[+] FLAG: academy{n0_r4t3_n0_4uth_359dd2cb}
```
