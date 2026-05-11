---
iteracion: 2
tema: Variables enteras y asignación
tiempo_estimado: 30 min
---

# Iteración 2 — Variables

## Meta

Tu compilador puede ahora guardar valores en variables con nombre y recuperarlos.
Un programa como este debe funcionar:

```
x <-- 10
y <-- 3
print x
print y
```

## Lo que se añade a la gramática

- **Nombres de variable**: una secuencia de letras, números y guiones bajos que empieza
  con letra. Por ejemplo: `x`, `contador`, `valor_final`.
- **Sentencia de asignación**: la forma `nombre <-- expresión` guarda un valor en la variable.
  El operador es `<--` (dos guiones, no uno).
- **Variable como expresión**: escribir el nombre de una variable donde va una expresión
  significa "leer el valor de esa variable".

## Pruebas de aceptación

Genera tus propios programas de prueba y córrelos en QtSPIM.
Tu suite debe cubrir:

- Asignar un valor a una variable e imprimirla
- Asignar dos variables distintas, imprimir ambas en orden
- Reasignar una variable y verificar que `print` muestra el nuevo valor
- Una variable cuyo nombre sea una instrucción de MIPS (ej: `add`, `sub`, `div`) — este caso suele romper compiladores ingenuos; verifica que el tuyo lo maneja

**Trampa silenciosa** — pídele al LLM que genere un programa que lea una variable
sin haberla asignado. ¿Qué hace tu compilador? ¿Debería ser un error?

## Prompt de ejemplo para el LLM

---

> Mi compilador ya genera código para `print` con literales. Ahora necesito variables.
>
> En MIPS, las variables enteras se guardan en la sección `.data` como palabras de 32 bits.
> Cuando se asigna un valor a una variable, hay que almacenarlo en esa dirección de memoria.
> Cuando se lee una variable, hay que cargarla desde esa dirección a un registro.
>
> Necesito que el compilador haga esto automáticamente la primera vez que ve cada variable:
> reservar espacio en `.data` con un valor inicial de 0.

---

## Reflexión (llenar después de terminar esta iteración)

**¿Cómo decidió el modelo reservar espacio para la variable? ¿Dónde queda en el archivo `.asm`?**

> _

**Prueba b <-- 5 ¿Qué se genera, qué hace QtSpim? 

> _

**¿Qué pasa si asignas una variable dos veces? 

> _
