---
created: 2026-05-11
tema: Rúbrica Act 03 — RaraLang Compiler
peso_total: 45% del bloque de compiladores
---

# Rúbrica — Act 03: RaraLang Compiler

## Pesos por criterio

| Criterio | Peso |
|----------|------|
| Escalera de iteraciones | 20% |
| Implementación funcional | 20% |
| Auditoría del modelo | 25% |
| Reflexión escrita | 25% |
| Comprensión del MIPS generado | 10% |

---

## 1. Escalera de iteraciones (20%)

Mide hasta dónde llegó el alumno. Cada iteración completada suma puntos.
Una iteración está "completada" si los programas de prueba generados por el alumno
corren correctamente en QtSPIM y producen el resultado esperado.

| Iteraciones completadas | Puntos |
|-------------------------|--------|
| 1–2 (literales, variables) | 5 |
| + It 3 (aritmética) | 9 |
| + It 4 (Unicode ops) | 12 |
| + It 5 (if/else) | 15 |
| + It 6 (while/bloques) | 17 |
| + It 7 (funciones) | 19 |
| + It 8 (error handling) | 20 |

---

## 2. Implementación funcional (20%)

Evalúa la calidad del código generado, no solo si pasa las pruebas básicas.

| Nivel | Puntos | Descripción |
|-------|--------|-------------|
| Insuficiente | 0–5 | El código tiene errores frecuentes o no compila |
| Básico | 6–12 | Pasa los casos simples pero falla en casos borde |
| Completo | 13–17 | Pasa casos simples y borde; casos de error razonables |
| Sobresaliente | 18–20 | Robusto, maneja casos inesperados, código limpio |

Casos borde que se consideran:
- Variable con nombre reservado en MIPS
- Función que llama a otra función (bug de `$ra`)
- Expresiones anidadas profundas
- Condición de while que es falsa desde el inicio

---

## 3. Auditoría del modelo (25%)

Evalúa si el alumno revisó críticamente lo que generó el modelo, no si lo copió.
Se evalúa a través de las secciones de auditoría del reporte de iteración.

| Nivel | Puntos | Descripción |
|-------|--------|-------------|
| Sin auditoría | 0–5 | El reporte está en blanco o repite lo que dijo el modelo |
| Superficial | 6–12 | El alumno confirmó que funciona pero no explicó por qué |
| Crítica | 13–20 | El alumno identificó al menos una decisión implícita del modelo, la cuestionó y la explicó |
| Profunda | 21–25 | El alumno identificó decisiones implícitas, las corrigió o mejoró, y documentó el razonamiento |

Lo que se busca específicamente:
- ¿Detectó el alumno alguna decisión que el modelo tomó sin declararla?
- ¿Encontró algún caso donde el modelo se equivocó (resultado incorrecto, código inválido)?
- ¿La firma al final del reporte refleja correcciones reales o dice "ninguna" sin haberlas buscado?

---

## 4. Reflexión escrita (25%)

Evalúa la calidad del análisis en las secciones de reflexión por iteración.

| Nivel | Puntos | Descripción |
|-------|--------|-------------|
| Ausente | 0–5 | Las reflexiones están en blanco o son de una sola palabra |
| Descriptiva | 6–12 | El alumno describe lo que pasó pero no analiza por qué |
| Analítica | 13–20 | El alumno explica causas, conecta conceptos, hace preguntas propias |
| Original | 21–25 | El alumno encontró algo que no estaba en la guía, propone una extensión, o identifica una limitación no documentada |

Se valora especialmente:
- Respuestas a las preguntas sobre ambigüedad de la especificación
- Identificación de limitaciones del compilador (no solo las que se mencionan en la guía)
- Conexión entre las decisiones del compilador y conceptos vistos en clase (Listener, árbol sintáctico, etc.)

---

## 5. Comprensión del MIPS generado (10%)

Evalúa si el alumno puede explicar el código ensamblador que produce su compilador,
no si sabe escribir MIPS a mano.

| Nivel | Puntos | Descripción |
|-------|--------|-------------|
| Sin comprensión | 0–2 | No puede explicar ninguna instrucción del `.asm` generado |
| Parcial | 3–5 | Puede explicar las instrucciones básicas (li, sw, lw) pero no los saltos o llamadas |
| Funcional | 6–8 | Puede explicar el flujo completo de al menos un programa no trivial |
| Completa | 9–10 | Puede explicar por qué cada instrucción está donde está, incluyendo etiquetas y convenciones |

Se evalúa con una pregunta oral o escrita sobre el `.asm` de un programa específico
del alumno, elegido por el profesor.

---

## Entregables

- `MIPSListener.py` — el compilador implementado
- `main.py` — si fue modificado
- Carpeta con los programas `.rara` de prueba generados por el alumno (al menos 3 por iteración completada)
- Reporte de iteraciones con secciones de auditoría y reflexión completadas
- Los archivos `.asm` generados para al menos una prueba por iteración

**Fecha de entrega:** Semana 10 (1 jun 501 / 3 jun 502)

---

## Nota sobre el uso del LLM

El uso del modelo es parte del ejercicio, no una trampa. Lo que se evalúa no es si
el alumno usó el modelo, sino si lo auditó. Un reporte que dice "el modelo lo hizo
todo y todo está bien" sin evidencia de revisión crítica obtiene 0 en auditoría y
reflexión, independientemente de si el compilador funciona.
