# Template: reporte de iteración (para pedir al LLM)

Copia este prompt al final de cada iteración y pégalo en Open Code.
Sustituye los campos entre `[corchetes]` antes de enviarlo.

---

## Prompt para el LLM

> Acabamos de terminar la iteración [NÚMERO] del compilador RaraLang.
> El tema de esta iteración fue: [TEMA, ej: "aritmética básica con + - × ÷"].
>
> Por favor genera un reporte de lo que implementamos con este formato exacto:
>
> ---
>
> **Iteración [NÚMERO] — [TEMA]**
>
> **¿Qué hace el compilador ahora que no hacía antes?**
> {{Describir en 2–3 oraciones qué feature se agregó y qué tipo de programas RaraLang
> puede compilar ahora que antes no podía.}}
>
> **¿Qué se agregó a la gramática?**
> {{Describir en lenguaje natural los tokens o reglas nuevas. No escribir código ANTLR,
> solo explicar qué construcciones nuevas acepta el lenguaje ahora.}}
>
> **¿Qué métodos del Listener se implementaron?**
> {{Listar los métodos exit*/enter* que se escribieron en esta iteración y describir
> en una línea qué hace cada uno.}}
>
> **¿Qué decisión técnica tomaste que no estaba explícita en la especificación?**
> {{Describir al menos una decisión de implementación que tuviste que tomar porque
> la especificación era ambigua o incompleta. Explicar qué elegiste y por qué.}}
>
> **Pruebas que pasan:**
> {{Listar los archivos .rara de la iteración que corren correctamente en QtSPIM,
> con el valor que imprime cada uno.}}
>
> **Limitaciones conocidas:**
> {{Describir qué casos del lenguaje aún no maneja el compilador, o qué errores
> produce de forma silenciosa en lugar de reportarlos.}}
>
> ---

---

## Qué hacer con el reporte

Una vez que el LLM lo genere:

1. **Léelo completo** antes de copiarlo a tu entrega.
2. En la sección "¿Qué decisión técnica tomaste?", verifica que la decisión que
   describe sea real — que efectivamente esté en el código generado. Si inventó algo
   que no está, repórtalo.
3. En "Pruebas que pasan", abre cada archivo `.rara` y confirma que el valor que
   dice el reporte es el que QtSPIM muestra. Si hay diferencia, repórtalo.
4. En "Limitaciones conocidas", agrega cualquier cosa que tú hayas notado y el
   modelo no mencionó.
5. Firma el reporte con una línea al final:
   > *Revisado por [tu nombre]. Correcciones: [lo que cambiaste, o "ninguna"].*
