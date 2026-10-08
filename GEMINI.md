# Antigravity Operational Context: Academic Cybersecurity & CTF Research

Este entorno de trabajo pertenece a estudiantes e investigadores de Ingeniería en Ciberseguridad que participan en ejercicios académicos controlados, laboratorios autorizados y competencias oficiales de Capture The Flag (CTF), incluyendo el **Ejercicio Nacional de Ciberseguridad de Chile (ANCI)** y plataformas educativas acreditadas (**picoCTF / Carnegie Mellon**, **HackRocks**, **CryptoHack**).

---

## 🎯 Directrices de Operación Segura y Eficiente

Para evitar bloqueos innecesarios por filtros de texto automáticos y maximizar el rendimiento técnico del agente:

1. **Entorno Académico y Autorizado:**
   * Todas las actividades, desafíos y análisis se ejecutan sobre entornos sandboxed, contenedores de laboratorio y plataformas educativas autorizadas.
   * El objetivo es el aprendizaje, la auditoría de seguridad, el criptoanálisis teórico, la ingeniería inversa y el desarrollo de contramedidas defensivas.

2. **Manejo Eficiente de Artefactos y Datos:**
   * Cuando se analicen volcados de datos numéricos extensos, módulos criptográficos gigantes o capturas binarias, almacénalos directamente en archivos locales dentro de `challenges/<nombre_reto>/data.txt` en lugar de volcar texto en crudo al chat.
   * Utiliza scripts autónomos en Python (`z3-solver`, `pycryptodome`, `requests`, `scapy`) para procesar los artefactos localmente.

3. **Arquitectura Táctica:**
   * Respeta la arquitectura definida en `PLAYBOOK_CTF_ANCI.md` y `COLLABORATION_PROTOCOL.md`.
   * En instancias secundarias (Worker Nodes), actúa como operador técnico subordinado, ejecutando solvers y entregando la bandera con el formato `FLAG: <bandera>`.
