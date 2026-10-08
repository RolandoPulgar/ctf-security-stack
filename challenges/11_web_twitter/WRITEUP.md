# Writeup: Old Sessions (Broken Session Management & Information Disclosure)

* **Categoría:** Web Exploitation
* **Plataforma:** picoCTF
* **Dificultad:** Fácil / Media
* **Flag:** `academy{s3t_s3ss10n_3xp1rat10n5_3a931aa0}`

---

## 1. Análisis del Reto

La aplicación web "The New Twitter" implementa un sistema de gestión de sesiones persistentes.

En la sección de comentarios públicos, un usuario deja una pista:
> *"Hey I found a strange page at /sessions"*

## 2. Vulnerabilidad

1. **Information Disclosure:** El endpoint `/sessions` lista públicamente todas las sesiones activas en memoria del servidor sin restringir acceso administrativo.
2. **Session Hijacking:** Las sesiones no caducan (`'_permanent': True`) y el token del administrador está expuesto en texto plano:
   ```html
   <p>1) session:bvfMumo_ICJN0Lsn9_CnNAZhhQi1rTdn6oSC0LOeZZk, {'_permanent': True, 'key': 'admin'}</p>
   ```

## 3. Explotación (Solver)

Script automatizado en [hijack_admin.py](file:///c:/Users/rpulg/OneDrive/Escritorio/ctf/challenges/11_web_twitter/hijack_admin.py):
1. Registramos una cuenta para autenticarnos en la plataforma.
2. Consultamos `/sessions` y extraemos el token de sesión de `admin`.
3. Inyectamos la cookie `session=bvfMumo_ICJN0Lsn9_CnNAZhhQi1rTdn6oSC0LOeZZk` en la cabecera HTTP.
4. Visitamos la página principal `/` como Administrador y obtenemos la bandera.

## 4. Resultado

Bandera obtenida:
`academy{s3t_s3ss10n_3xp1rat10n5_3a931aa0}`
