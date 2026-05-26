# Reporte — Iteración 2: Variables

---

## ¿Qué hace el compilador ahora que no hacía antes?

El compilador ahora soporta la declaración, asignación y lectura de variables enteras y cadenas de texto. Específicamente:
- Permite asignar valores a variables usando el operador `<--` (por ejemplo, `x <-- 42` o `mensaje <-- "hola"`).
- Permite usar variables dentro de expresiones y en la sentencia `print` (por ejemplo, `print x`).
- Genera código MIPS que reserva de forma automática espacio en la sección `.data` para cada variable identificada, con un valor inicial de 0.
- Traduce las asignaciones en instrucciones `sw` (store word) para persistir los valores en memoria, y las lecturas en instrucciones `lw` (load word) para cargar los valores de memoria a registros temporales.

---

## ¿Qué se agregó a la gramática?

Se añadieron reglas sintácticas y tokens para dar soporte a identificadores (`ID`) y sentencias de asignación en `antlr/RaraLang.g4`:

- **Identificador (`ID`)**: Un token definido mediante `[a-zA-Z][a-zA-Z0-9_]*` para nombrar variables.
- **Sentencia de asignación (`assignStmt`)**: Una regla en `stmt` de la forma `ID '<--' expr`.
- **Expresión de variable (`varExpr`)**: Una alternativa en `expr` de la forma `ID` para poder leer variables dentro de expresiones.

---

## ¿Qué métodos del Listener se implementaron?

| Método | Descripción |
|---|---|
| `exitAssignStmt(ctx)` | Obtiene el nombre de la variable y saca el valor/tipo de la pila. Registra la variable en `self._variables` para su declaración en `.data`. Emite una instrucción `sw` para almacenar el registro que contiene el valor en la dirección de memoria `var_<nombre>`. |
| `exitVarExpr(ctx)` | Obtiene el nombre de la variable y la registra en `self._variables`. Asigna un registro temporal disponible, emite la instrucción `lw` para cargar el valor desde `var_<nombre>` al registro temporal, y empuja el descriptor `("int" | "str_ref", reg)` a la pila de valores. |
| `output()` | Modificado para recorrer todas las variables registradas en `self._variables` y generar de forma ordenada las directivas `var_<nombre>: .word 0` en la sección `.data`. |

---

## ¿Qué decisión técnica tomaste que no estaba explícita en la especificación?

**Prefijo de nombres de variables en MIPS.**

Para evitar colisiones de nombres entre las variables definidas en el código RaraLang y las instrucciones reservadas o registros de MIPS (por ejemplo, si el usuario define una variable llamada `add`, `sub`, o `div`), el compilador renombra internamente las variables agregando el prefijo `var_` (por ejemplo, `var_add`, `var_sub`). Esto garantiza que la sección `.data` del archivo ensamblador sea siempre válida y no cause conflictos en el ensamblador QtSPIM.

**Tipado implícito al momento de la lectura.**

Dado que RaraLang no cuenta con declaraciones de tipos explícitas, el compilador infiere el tipo de la variable a partir de la última asignación registrada en el diccionario `self._var_types`. Si una variable es leída sin haber sido asignada previamente, se asume por defecto que es de tipo `"int"`.

---

## Pruebas que pasan

| Archivo | Entrada en RaraLang | Salida esperada en QtSPIM |
|---|---|---|
| `07_assign_print.rara` | Asignación simple e impresión de variable | `42` |
| `08_two_vars.rara` | Asignación y lectura de dos variables en orden | `10` <br> `3` |
| `09_reassign.rara` | Reasignación de una variable y verificación del nuevo valor | `100` <br> `200` |
| `10_mips_keyword_var.rara` | Uso de nombres de variables que son palabras clave en MIPS (`add`, `sub`, `div`) | `50` <br> `20` <br> `10` |

---

## Limitaciones conocidas

- **Falta de análisis de variables no definidas**: El compilador no genera un error de compilación si una variable se lee antes de asignarse; en su lugar, QtSPIM cargará el valor por defecto de `0` almacenado en `.data`.
- **Sin soporte para variables en operaciones aritméticas complejas**: Las variables solo se pueden imprimir o asignar directamente, ya que la aritmética aún no está soportada (Iteración 3).
- **Registros no reutilizables**: El índice de registros temporales continúa incrementándose sin liberarse, limitando la cantidad total de expresiones evaluadas secuencialmente a los registros físicos disponibles.

---

## Reflexión

Para almacenar las variables del programa en la sección `.data`, la cual queda ubicada al principio del archivo `.asm`, decidí registrarlas en un conjunto único durante la fase de análisis sintáctico. Al generar el código final, recorro este conjunto para declarar cada variable con el prefijo `var_`, asignándoles por defecto el valor de `.word 0`, lo cual inicializa la memoria reservada con un valor de 0 (un entero de 32 bits). Por ejemplo, para la asignación `b <-- 5`, mi compilador reserva el espacio mediante la directiva `var_b: .word 0` y genera en la sección `.text` las instrucciones `li $t0, 5` y `sw $t0, var_b`. En QtSpim, al cargar y ejecutar el programa, se reserva la dirección de memoria correspondiente inicializada en cero, se coloca el valor inmediato `5` en el registro temporal `$t0` y finalmente la instrucción `sw` copia ese valor de `5` a la memoria física reservada para `var_b` en la RAM simulada.

Cuando una variable se asigna dos veces consecutivas, a nivel de memoria la sección `.data` se mantiene intacta, ya que solo se reserva un único espacio de memoria para ella independientemente de cuántas veces aparezca. En cambio, a nivel de ejecución y registros, el compilador emite instrucciones secuenciales para cargar cada nuevo valor en un registro temporal y realizar la correspondiente operación `sw` hacia la dirección de la variable. De este modo, la segunda operación de almacenamiento simplemente sobrescribe el valor previo en memoria, quedando únicamente el último valor asignado en el estado final del programa.

En caso de que el código intente leer una variable que no ha sido inicializada previamente, el compilador no genera un error sintáctico ni interrumpe la compilación, sino que asume de forma implícita que es de tipo entero. Al ejecutarse en QtSpim, dado que todas las variables declaradas en la sección `.data` se inicializan por defecto en cero (`.word 0`), el programa cargará este valor de cero de manera segura a través de una instrucción `lw` sin causar fallos de segmento ni errores en tiempo de ejecución, aunque a nivel lógico represente un error de diseño por parte del programador.


---

## Auditoría del modelo

### Proceso de configuración del entorno — acciones tomadas y rechazadas

Para esta iteración, no se requirió reinstalar ANTLR4 ni el JDK ya que el entorno de desarrollo estaba listo desde la Iteración 1. Se verificó la generación del parser corriendo las pruebas directamente sobre los archivos modificados.

### Cómo funciona el compilador — razonamiento del modelo

El compilador mantiene el flujo basado en el Listener de ANTLR y extiende la estructura agregando control sobre las variables:
1. El compilador rastrea todas las variables vistas en un `set` único (`self._variables`). Esto asegura que, sin importar cuántas veces aparezca una variable en el código, solo se asigne una única directiva `.word 0` en `.data`.
2. Las asignaciones actualizan la memoria de forma inmediata mediante `sw`. No mantenemos estados de variables en registros persistentes entre líneas, lo cual simplifica la lógica del compilador y evita problemas de sincronización de registros.
3. El uso de prefijos `var_` previene colisiones con instrucciones de MIPS, lo cual fue probado con éxito en el caso `10_mips_keyword_var.rara`.

### Auditoría de respuestas del modelo 
Trampa silenciosa — pídele al LLM que genere un programa que lea una variable sin haberla asignado. ¿Qué hace tu compilador? ¿Debería ser un error?
Viewed 11_uninitialized_var.rara:1-5

Sí, es correcto el modelo llm de respuesta, ya que desde la perspectiva de las buenas prácticas y la semántica de la programación, **es un error de lógica del programador** (o un error semántico), ya que se está intentando usar un dato que técnicamente no existe o no ha sido definido con un valor consentido.

Sin embargo, para **nuestro compilador** actual:
1. **No es un error de compilación**: El parser lo acepta porque sintácticamente es correcto (`print ID`).
2. **No genera un error en tiempo de ejecución (runtime)**: En lugar de dejar basura en memoria o tirar un fallo de segmento, MIPS inicializa por defecto las palabras en `.data` a `0`. Por lo tanto, el programa simplemente corre y muestra `0`.

Así que sí, es un error de lógica/diseño en el código fuente del usuario, pero el compilador decide "salvarlo" dándole el valor por defecto de `0` en lugar de lanzar una alerta.
*Revisado por Miguel Ángel Ogando. Correcciones: se agregó la auditoría completa del proceso de configuración y del razonamiento del modelo; se completó la sección de reflexión sobre la reserva y comportamiento de variables en MIPS y QtSpim.*

