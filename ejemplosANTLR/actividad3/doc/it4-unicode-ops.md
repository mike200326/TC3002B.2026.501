---
iteracion: 4
tema: Operadores enteros Unicode (⊞ ⊠ ≈ ±)
tiempo_estimado: 30 min
---

# Iteración 4 — Operadores Unicode

## Meta

Tu compilador entiende cuatro operadores adicionales que usan símbolos tipográficos.
Esto debe funcionar:

```
print 10 ⊞ 3
print 4 ⊠ 5
print 7 ≈ 3
print ±8
```

## Lo que se añade a la gramática

- **`⊞`** (módulo): `a ⊞ b` da el residuo de dividir `a` entre `b`. Es el "%" de RaraLang.
- **`⊠`** (doble más): `a ⊠ b` da `2a + b`. No es multiplicación estándar — es una operación
  deliberadamente no estándar de RaraLang.
- **`≈`** (promedio entero): `a ≈ b` da el piso de `(a + b) / 2`. Para negativos,
  "piso" significa redondear hacia menos infinito (no hacia cero).
- **`±`** (negación unaria): `±x` da `-x`. Es un operador que va antes de la expresión,
  no entre dos operandos.

Estos cuatro operadores se agregan como alternativas adicionales en la regla de expresión
de la gramática. Su precedencia relativa entre sí y respecto a `+`, `-`, `×`, `÷` queda
determinada por el orden en que aparecen en la gramática — ese orden puede ser sorpresivo.

## Pruebas de aceptación

Genera tus propios programas y calcula el resultado esperado a mano antes de correr.
Tu suite debe cubrir:

- `⊞`: prueba con valores donde conozcas el residuo exacto (ej. `10 ⊞ 3` = 1)
- `⊠`: verifica con un par de valores (ej. `4 ⊠ 5` = 2×4+5 = 13)
- `≈`: prueba con positivos y con negativos — el resultado con negativos es el que más frecuentemente falla
- `±`: prueba doble negación (`± ±x`) — debe dar el valor original
- Una expresión que mezcle un operador Unicode con uno aritmético — observa qué precedencia asignó tu gramática y verifica si es la que esperabas

## Prompt de ejemplo para el LLM

---

> Necesito agregar cuatro operadores enteros a mi compilador RaraLang → MIPS.
>
> **`⊞` (módulo)**: en MIPS, la instrucción de división deja el residuo en un registro
> especial separado del cociente. Para módulo, hay que hacer la división y tomar el
> residuo en lugar del cociente.
>
> **`⊠` (doble más)**: `a ⊠ b` equivale a `2*a + b`. Multiplicar por 2 en binario es
> equivalente a desplazar los bits un lugar a la izquierda, que es una operación muy
> eficiente en MIPS.
>
> **`≈` (promedio entero)**: `a ≈ b` equivale a `(a + b) / 2` redondeando hacia abajo.
> Para enteros negativos, la división aritmética por 2 (desplazamiento aritmético a la
> derecha) da el resultado correcto de "piso", a diferencia de la división entera normal
> que trunca hacia cero.
>
> **`±` (negación)**: es un operador unario — va antes de un solo operando. `±x` equivale
> a `0 - x`. En el Listener, el método correspondiente recibe el valor ya evaluado en
> el tope de la pila y lo modifica en su lugar.
>
> La gramática necesita añadir estos como alternativas en la regla de expresión. Los
> operadores binarios siguen el mismo patrón que `+` y `-`. El unario `±` va como una
> alternativa de la forma `± expr`.
>


---

## Reflexión (llenar después de terminar esta iteración)

**`a ≈ b` con `a = -3` y `b = -1`: ¿qué resultado da tu compilador? ¿Es el esperado si "piso" significa redondear hacia menos infinito?**

> _

**La especificación de `⊠` dice `2a + b`, no `a × b`. ¿En qué caso daría el mismo resultado que la multiplicación? ¿En cuáles no?**

> _

**`± ±5` debería dar 5. ¿Lo da? ¿Cómo implementó el modelo la doble negación?**

> _
