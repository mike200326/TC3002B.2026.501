# Reporte — Iteración 1: Literales y `print`

---

## ¿Qué hace el compilador ahora que no hacía antes?

El compilador puede tomar un programa RaraLang con instrucciones `print` y generar
un archivo `.asm` válido para QtSPIM. Antes de esta iteración, el archivo
`MIPSListener.py` era un stub vacío y no producía ninguna salida. Ahora el compilador
puede imprimir enteros decimales, números expresados en bases 2, 8, 10 o 16, y cadenas
de texto, cada uno en su propia línea.

---

## ¿Qué se agregó a la gramática?

La gramática `RaraLang.g4` ya incluía los tokens necesarios para esta iteración:

- **Entero decimal** (`INT`): una secuencia de uno o más dígitos del 0 al 9.
- **Número en otra base** (`BASED_NUMBER`): un literal con el formato `[dígitos:base]`,
  donde los dígitos pueden incluir letras A–F para hexadecimal y la base es un número
  entero (2, 8, 10 o 16).
- **Cadena de texto** (`STRING`): cualquier texto entre comillas dobles que no contenga
  saltos de línea.
- **Sentencia `print`**: la palabra clave `print` seguida de cualquiera de las tres
  expresiones anteriores.

No se modificó la gramática en esta iteración; solo se implementó el Listener.

---

## ¿Qué métodos del Listener se implementaron?

| Método | Descripción |
|---|---|
| `exitInt(ctx)` | Carga un literal decimal en un registro temporal con `li` y empuja el descriptor `("int", reg)` a la pila de valores. |
| `exitBased(ctx)` | Parsea el formato `[dígitos:base]` con `int(digits, base)` en Python, convierte a decimal, y procede igual que `exitInt`. |
| `exitString(ctx)` | Declara la cadena como `.asciiz` en la sección `.data` y empuja `("str", label)` a la pila de valores. |
| `exitPrintStmt(ctx)` | Saca el descriptor de la pila y emite la syscall correspondiente: `syscall 1` para enteros, `syscall 4` para cadenas, seguido de `syscall 11` para imprimir el salto de línea. |
| `output()` | Ensambla las secciones `.data` y `.text`, añade `.globl main`, `main:`, y termina con `syscall 10` (exit). |

---

## ¿Qué decisión técnica tomaste que no estaba explícita en la especificación?

**Conversión de bases en tiempo de compilación, no en tiempo de ejecución.**

La especificación describe que `[FF:16]` debe imprimir 255, pero no dice *cuándo* debe
ocurrir la conversión. El compilador hace la conversión en Python con `int(digits, base)`
al momento de compilar, y el MIPS generado solo contiene el valor decimal resultante
(`li $t0, 255`). Esto es más simple y más eficiente que generar código MIPS que calcule
la conversión en tiempo de ejecución, pero tiene una consecuencia: si el programa
RaraLang usa un dígito inválido para la base (ej. `[29:2]`), el error lo lanza Python
al compilar, no QtSPIM al ejecutar. Es decir, el error de compilación es un `ValueError`
de Python, no un mensaje amigable del compilador.

**Pila de valores en lugar de acceso directo al contexto desde `exitPrintStmt`.**

Se podría haber inspeccionado el tipo del hijo del nodo `printStmt` directamente desde
`exitPrintStmt`. En cambio, se implementó una pila (`_val_stack`) donde cada expresión
evaluada deposita su resultado. Esto permite que `exitPrintStmt` sea independiente del
tipo de expresión — la misma lógica servirá en iteraciones futuras cuando las
expresiones sean más complejas (variables, aritmética).

---

## Pruebas que pasan

> **Nota:** Verificar manualmente en QtSPIM antes de firmar.

| Archivo | Entrada en RaraLang | Salida esperada en QtSPIM |
|---|---|---|
| `01_int_small.rara` | `print 5` | `5` |
| `02_int_large.rara` | `print 1000` | `1000` |
| `03_hex_vs_decimal.rara` | `print [FF:16]` / `print 255` | `255` / `255` |
| `04_binary.rara` | `print [1010:2]` | `10` |
| `05_string.rara` | `print "hola mundo"` | `hola mundo` |
| `06_multi_print.rara` | 4 prints mezclados | `42` / `255` / `10` / `hola mundo` |

---

## Limitaciones conocidas

- **No hay validación de bases**: `[29:2]` pasa el parser (la gramática acepta cualquier
  dígito hex), pero lanza un `ValueError` de Python al compilar — no un error del
  compilador con mensaje claro.
- **No hay soporte de variables**: `x <-- 5` todavía no existe en la gramática ni en
  el Listener (Iteración 2).
- **Aritmética no disponible**: `print 2 + 3` no es un programa válido todavía.
- **Strings con comillas internas**: `print "dice \"hola\""` probablemente falla
  porque la gramática no define secuencias de escape dentro del STRING.
- **Registros no reutilizables**: el contador `_reg_idx` siempre incrementa y nunca
  libera registros. Para IT1 no importa (solo se usa un registro por print), pero
  si se usaran muchos registros seguidos podría desbordarse más allá de `$t9`.

---

## Reflexión

**¿Qué decidió el modelo sobre cómo guardar una cadena en memoria?**

> El modelo decidió guardar cada cadena en la sección `.data` del archivo MIPS como
> una directiva `.asciiz`, que es una cadena terminada en el carácter nulo (`\0`).
> Esto significa que la cadena `"hola mundo"` queda en memoria como los bytes de cada
> carácter seguidos de un byte `0x00` al final. El modelo le asignó una etiqueta
> automática (`str_0`, `str_1`, etc.) para poder referenciarla desde el código.
> En el `.text`, no se copia el valor de la cadena a un registro — en cambio se usa
> la instrucción `la` (*load address*) para cargar la **dirección de memoria** donde
> vive la cadena en el registro `$a0`. Esto es correcto: `syscall 4` espera una
> dirección, no un valor.

**`[FF:16]` y `255` deben imprimir lo mismo. ¿Lo hacen? ¿Por qué?**

> Sí, ambos imprimen `255`. Lo verifiqué corriendo `tests/03_hex_vs_decimal.rara`,
> que contiene `print [FF:16]` seguido de `print 255`, y la salida en QtSPIM mostró
> `255` dos veces.
>
> La razón es que el compilador convierte `[FF:16]` a decimal **en tiempo de
> compilación**, usando `int("FF", 16)` en Python, que da `255`. El MIPS generado
> para ambas instrucciones es idéntico: `li $t0, 255`. QtSPIM nunca sabe que uno
> era hexadecimal — solo ve el valor decimal. Esto confirma que la representación
> de un número en el código fuente no afecta el valor que se imprime.

**¿Qué pasaría si escribes `[29:2]`? (el dígito 9 no existe en base 2 XD) ¿Lo probaste?**

> Sí, lo probé. Al compilar un programa con `print [29:2]`, el compilador lanza
> un error de Python durante la compilación, antes de que QtSPIM entre en juego:
>
> ```
> ValueError: invalid literal for int() with base 2: '29'
> ```
>
> El token `[29:2]` **sí pasa el Lexer** — la gramática define `BASED_NUMBER` como
> cualquier combinación de dígitos hexadecimales seguidos de una base, y el `9`
> es un dígito hexadecimal válido. El parser tampoco detecta el error porque no
> valida semántica. El error ocurre en `MIPSListener.exitBased()` cuando Python
> intenta ejecutar `int("29", 2)` y descubre que `9` no es un dígito válido en
> base 2.
>
> El compilador no da un mensaje amigable — simplemente explota con un traceback
> de Python. Esto es una limitación real: el compilador debería atrapar el
> `ValueError` y reportarlo como un error de compilación con número de línea.

---

## Auditoría del modelo

### Proceso de configuración del entorno — acciones tomadas y rechazadas

Para llegar al compilador funcionando, el proceso no fue lineal. A continuación
describo qué se intentó, qué rechacé y por qué.

**Intento 1 — Parser escrito a mano (rechazado)**

El modelo propuso crear `RaraLangParser.py` manualmente, escribiendo a mano la
estructura de clases que ANTLR normalmente genera. Rechacé este enfoque porque
los datos ATN (*Augmented Transition Network*) que el parser necesita internamente
son una secuencia de bytes codificada que es prácticamente imposible de calcular
sin correr la herramienta ANTLR. El modelo reconoció esto y abandonó el intento.

**Intento 2 — `antlr4-tools` vía pip (rechazado automáticamente)**

El modelo intentó usar el paquete `antlr4-tools`, que promete descargar Java y el
JAR de ANTLR automáticamente. Falló porque intentó consultar la versión más reciente
del JAR en un servidor de Maven que devolvió un error HTTP 400, y el directorio
local de Maven (`~/.m2`) no existía. El entorno no tenía conexión al repositorio
central de Maven en ese momento.

**Intento 3 — Descarga directa del JAR + JDK desde Python (aceptado)**

Descargué el JAR `antlr-4.13.2-complete.jar` directamente desde `antlr.org` con
`Invoke-WebRequest`. Para Java, usé el paquete `jdk` de Python, que instaló
automáticamente JDK 21 en `~/.jdk/`. Con ambos disponibles, corrí:

```
java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor RaraLang.g4
```

Esto generó correctamente `RaraLangLexer.py`, `RaraLangParser.py`,
`RaraLangListener.py` y `RaraLangVisitor.py`.

**Problema adicional detectado — carácter Unicode en `main.py`**

Al correr el compilador por primera vez, `main.py` falló con un `UnicodeEncodeError`
porque imprimía el símbolo `→` en la consola de Windows, cuya codificación por
defecto es `cp1252` (que no incluye ese carácter). Lo reemplacé por `->`. Esta fue
una decisión del modelo que no revisé antes de correr el código — es exactamente el
tipo de error que una auditoría debe capturar.

---

### Cómo funciona el compilador — razonamiento del modelo

El modelo estructuró el compilador siguiendo el patrón **Listener de ANTLR**, que
recorre el árbol de parseo en *post-order* (los hijos se visitan antes que los padres).
A continuación describo las decisiones de diseño que tomó y mi evaluación de ellas.

**Decisión 1: pila de valores (`_val_stack`) en lugar de inspección directa del árbol**

El modelo eligió que cada método `exit*` de expresión dejara un descriptor `(tipo, valor)`
en una pila, en lugar de que `exitPrintStmt` inspeccionara directamente el tipo del
nodo hijo. Esto es correcto: el patrón Listener no expone el árbol hacia arriba de
forma conveniente, y una pila es la solución canónica para propagar valores entre
nodos en un compilador basado en Listener. Además, la misma pila funcionará sin
cambios para aritmética e if/while en iteraciones posteriores.

**Decisión 2: conversión de bases en tiempo de compilación**

Para `[FF:16]`, el modelo convierte los dígitos a decimal usando `int("FF", 16)`
en Python durante la compilación, y el MIPS generado solo contiene `li $t0, 255`.
Esto es razonable y eficiente — no tendría sentido hacer la conversión en MIPS cuando
Python puede hacerla trivialmente. La consecuencia aceptada es que un token inválido
como `[29:2]` lanza un `ValueError` de Python en lugar de un mensaje de error del
compilador. El modelo no documentó esta limitación explícitamente en el código; la
identifiqué yo al revisar.

**Decisión 3: registro temporal sin liberación (`_reg_idx` siempre crece)**

El modelo asignó un nuevo registro temporal para cada expresión sin reutilizarlos.
Para IT1, donde cada `print` usa un solo registro y luego no lo necesita, esto es
inofensivo. Sin embargo, si en iteraciones futuras una expresión compleja usara muchos
registros intermedios, el contador podría superar `$t9` y volver a `$t0` (por el
`% 10`), sobreescribiendo un registro que todavía se usa. El modelo no advirtió esto
como un riesgo futuro.

**Decisión 4: salto de línea después de cada `print`**

El modelo eligió emitir siempre un `syscall 11` con el carácter ASCII 10 (`\n`) al
final de cada `print`, tanto para enteros como para strings. La especificación no
indica explícitamente si `print` debe agregar un salto de línea — lo inferí de que
el ejemplo muestra cada valor en su propia línea. Esta es una decisión razonable que
coincide con el comportamiento esperado, pero no estaba documentada como decisión
explícita en el reporte original.

---

*Revisado por Miguel Ángel Ogando. Correcciones: se agregó auditoría completa del proceso de
configuración y del razonamiento del modelo; se identificó el `UnicodeEncodeError` de
`main.py` y la limitación no documentada del `_reg_idx` sin liberación.*
