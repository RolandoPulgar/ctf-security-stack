# 🤖 Protocolo de Operación Multi-Agente (Master-Worker Architecture)

Este documento define las reglas de sincronización, comandos de acople y el rol operativo para cualquier instancia secundaria de **Antigravity** que se una al equipo de competencia o auditoría.

---

## 👑 Arquitectura de Mando

```mermaid
flowchart TD
    subgraph Master Node [Nodo Maestro - Rolando + Antigravity Master]
        M1[Triage General de Retos]
        M2[Asignación de Objetivos y Prioridades]
        M3[Consolidación de Flags y Repositorio Oficial]
    end

    subgraph Worker Nodes [Nodos Operadores - Compañero + Antigravity Worker]
        W1[Foco: Web Exploitation / Fuzzing]
        W2[Foco: Reversing & Descompilación Binaria]
        W3[Foco: Criptoanálisis & Z3 Solvers]
    end

    M1 -->|Asigna Retos / Vectores| Worker Nodes
    Worker Nodes -->|Reportan Banderas & Solvers| M3
```

* **Nodo Maestro (Tú + Antigravity Maestro):**
  * Define la estrategia, realiza el triage de los 12 desafíos y asigna las tareas.
  * Mantiene el control del repositorio principal (`main`), aprueba los PRs/commits y valida las banderas en la plataforma del CTF.
* **Nodo Trabajador / Operador (Compañero + Antigravity Secundario):**
  * Ejecuta tareas técnicas específicas delegadas por el Maestro (ej: "Analiza el binario X", "Escribe un solver en Z3 para esta función", "Fuzzea este endpoint").
  * Trabaja en ramas dedicadas (`feat/reto-XX`) y reporta inmediatamente los resultados y la bandera al Maestro.

---

## ⚡ Comandos de Acople Rápido para el Compañero

Tu compañero solo debe abrir su terminal (PowerShell, Bash o CMD) y ejecutar:

```bash
# 1. Clonar el stack oficial
git clone https://github.com/RolandoPulgar/ctf-security-stack.git
cd ctf-security-stack

# 2. Instalar el arsenal de herramientas
pip install -r requirements.txt

# 3. Crear su rama de trabajo para el reto asignado
git checkout -b worker-solver
```

---

## 📋 Instrucción Inicial (Prompt de Acople para el Antigravity Secundario)

Tu compañero debe copiar y pegar este prompt exacto al iniciar su chat en Antigravity:

> ```markdown
> Actúa como un agente operador técnico subordinado al Nodo Maestro en el repositorio `ctf-security-stack`.
> 
> Lee atentamente los archivos `PLAYBOOK_CTF_ANCI.md` y `COLLABORATION_PROTOCOL.md` antes de actuar.
> 
> Tus reglas operativas son:
> 1. Tu objetivo exclusivo es resolver las tareas técnicas específicas que se te asignen (Reversing, Cripto, Forense o Web).
> 2. Utiliza las herramientas existentes en `tools/` y los solvers en `templates/`.
> 3. Todo script que desarrolles debe guardarse dentro de `challenges/<nombre_reto>/` junto con su `WRITEUP.md`.
> 4. Cuando encuentres una bandera o soluciones el reto, formatéala claramente como `FLAG: <bandera>` para que el operador la transmita al Nodo Maestro.
> 5. No toques la rama `main` directamente; genera scripts reproducibles y concisos.
> ```

---

## 🔄 Protocolo de Sincronización Durante el Evento

1. **Recepción de Tarea:** El Nodo Maestro le indica al Trabajador: *"Trabaja en el reto 03 (Forense PCAP). Extrae el stream HTTP del puerto 8080."*
2. **Ejecución Técnica:** El agente trabajador procesa el fichero con `scapy` o `tshark` y genera el solver.
3. **Reporte:** El trabajador entrega la bandera y el script.
4. **Subida y Merge:** Se hace commit y push para que el repositorio quede actualizado en tiempo real.
