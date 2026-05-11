---
iteracion: 1
tema: Literales enteros, números en otras bases, strings, y print
tiempo_estimado: 30 min
---

# Iteración 1 — Literales y print

## Meta

Al terminar esta iteración, tu compilador puede tomar un programa con instrucciones
`print` y convertirlo en un archivo `.asm` que, al correr en QtSPIM, imprime los
valores correctos en pantalla.

Ejemplo de lo que debe funcionar al terminar:

```
print 42
print 255
print [FF:16]
print [1010:2]
print "hola mundo"
```

## Lo que se añade a la gramática

Partimos de una gramática mínima que solo reconoce `print` seguido de un número entero.
En esta iteración ampliamos para que también reconozca:

- **Números en otras bases**: un literal con el formato `[dígitos:base]`, donde la base puede
  ser 2, 8, 10 o 16. Por ejemplo, `[FF:16]` es 255 en hexadecimal, `[1010:2]` es 10 en binario.
  Los dígitos pueden incluir letras A–F para hexadecimal.
- **Cadenas de texto**: cualquier texto entre comillas dobles, como `"hola mundo"`.
- Todos estos pueden aparecer después de `print`.

## Pruebas de aceptación

Genera tus propios programas de prueba con el LLM y córrelos en QtSPIM.
Tu suite debe cubrir al menos estos casos:

- Un entero pequeño (ej. `print 5`) — verificar que imprime exactamente ese número
- Un entero grande (ej. `print 1000`)
- Un número en base 16 y su equivalente decimal — deben imprimir lo mismo
- Un número en base 2 — verificar la conversión manualmente
- Una cadena de texto — verificar que imprime el texto sin basura extra
- Un programa con varios `print` seguidos — verificar que cada valor aparece en su propia línea

## Prompt de ejemplo para el LLM

Ajusta según lo que ya tengas. Úsalo como punto de partida, no copiar/pegar ciego.

---

> Tengo un proyecto de compilador en Python usando ANTLR4. El compilador toma
> programas escritos en RaraLang y genera código MIPS para el simulador QtSPIM.
>
> La gramática ya reconoce `print` seguido de un entero (`INT`). Necesito que el
> `MIPSListener.py` haga lo siguiente:
>
> **Para `print 42`:**
> Cargar el número 42 en un registro temporal. Luego imprimirlo como entero usando
> la llamada al sistema de SPIM para print_int (syscall 1), seguida de una nueva
> línea (syscall 11 con el carácter 10).
>
> **Para `print [FF:16]`:**
> El token tiene el formato `[dígitos:base]`. Convertir los dígitos a decimal en Python
> con la función `int(digits, base)` y cargar el resultado igual que un entero normal.
>
> **Para `print "hola"`:**
> Guardar el texto en la sección `.data` como una cadena terminada en cero (`.asciiz`).
> Cargar su dirección en un registro y usar la syscall de print_string (syscall 4).
>
---

## Reflexión (llenar después de terminar esta iteración)

**¿Qué decidió el modelo sobre cómo guardar una cadena en memoria?**

> _

**`[FF:16]` y `255` deben imprimir lo mismo. ¿Lo hacen? ¿Por qué?**

> _

**¿Qué pasaría si escribes `[29:2]`? (el dígito 9 no existe en base 2 XD) ¿Lo probaste?**

> _
