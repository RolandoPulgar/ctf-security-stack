# 🛡️ AI-Augmented Cybersecurity & CTF Acceleration Framework

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Security Framework](https://img.shields.io/badge/Security-Industry%20Standard-green.svg)]()
[![Platform](https://img.shields.io/badge/Target-CTF%20%7C%20HackTheBox%20%7C%20HackRocks-orange.svg)]()
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

> **Framework de respuesta rápida, triage forense, ingeniería inversa y resolución de retos de ciberseguridad asistido por Inteligencia Artificial colaborativa (Human-in-the-Loop).**

---

## 🎯 Visión y Propósito

Este repositorio documenta el stack técnico, las metodologías de triage automatizado y los solvers utilizados para **competencias de CTF (Capture The Flag) y auditorías de seguridad práctica**.

Más allá del ámbito competitivo, este proyecto demuestra cómo la integración de **modelos avanzados de IA como copilotos de seguridad** acelera drásticamente las capacidades operativas de un equipo (Blue Team / Red Team / CSIRT), permitiendo:
1. **Reducción del MTTR (Mean Time to Respond):** De horas a minutos mediante scripting y desofuscación inmediata.
2. **Triage y Clasificación Forense:** Análisis automatizado de artefactos, firmas de binarios y capturas de tráfico.
3. **Gobernanza y Trazabilidad:** Generación de bitácoras técnicas reproducibles alineadas con los requerimientos de la **Ley Marco de Ciberseguridad N° 21.663** e **ISO 27001**.

---

## 📂 Estructura del Repositorio

```text
ctf/
├── 📄 PLAYBOOK_CTF_ANCI.md       # Metodología táctica, tiempos de rotación y patrones
├── 📄 requirements.txt           # Dependencias del stack analítico
├── 📁 tools/                     # Herramientas de triage automatizado
│   └── 🐍 triage.py              # Extractor de metadatos, magic bytes y flag hunter
├── 📁 templates/                 # Plantillas de scripts de explotación y solvers
│   ├── 🐍 tcp_solver_template.py # Interacción remota TCP / pwntools
│   └── 🐍 crypto_solvers.py      # Solvers de RSA (Fermat/Wiener), XOR y PRNG
└── 📁 challenges/                # Pruebas de concepto y writeups reproducibles
    └── 📁 01_crackme/            # Reversing y resolución matemática con Z3 Theorem Prover
```

---

## 🚀 Arsenal Técnico

| Dominio | Herramientas & Librerías | Aplicación Táctica |
| :--- | :--- | :--- |
| **Ingeniería Inversa** | `z3-solver`, Ghidra, radare2 | Modelado de restricciones algebraicas y desensamblado rápido |
| **Criptoanálisis** | `pycryptodome`, `sympy`, `factordb` | Factorización de módulos débiles, oráculos de padding y PRNGs |
| **Forense & Redes** | `scapy`, `tshark`, `binwalk` | Disección de protocolos, reconstrucción de streams y carving |
| **Seguridad Web** | `requests`, `httpx`, `beautifulsoup4` | Fuzzing dirigido, validación de IDORs y manipulación de JWT |

---

## ⚡ Flujo Operativo Asistido por IA

```mermaid
flowchart LR
    A[Ingesta del Artefacto] --> B[Triage & Signatures]
    B --> C[Modelado & Scripting IA]
    C --> D[Extracción de Flag]
    D --> E[Writeup & Bitácora Auditable]
```

1. **Ingesta & Triage:** Inspección rápida con `triage.py` para descartar falsas pistas y clasificar el vector.
2. **Modelado Asistido:** Formulación matemática del problema (ej. teorema de restricciones Z3 o explotación de oráculo).
3. **Ejecución y Extracción:** Ejecución del solver en microsegundos contra el entorno de pruebas.
4. **Documentación:** Generación de writeup con pasos reproducibles y recomendaciones de mitigación.

---

## 🛠️ Instalación y Uso Rápido

```bash
# Clonar repositorio
git clone <URL_DEL_REPOSITORIO>
cd ctf

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar herramienta de triage
python tools/triage.py <ruta_del_archivo>

# Probar solver de ejemplo (Z3 Crackme)
python challenges/01_crackme/solve_crackme.py
```

---

## 👥 Equipo y Colaboración
Desarrollado y preparado para el **Ejercicio Nacional de Ciberseguridad ANCI 2026**.
* Operadores técnicos en tándem con **Antigravity (Google DeepMind)**.
