"""
MIPSListener.py — Compilador RaraLang → MIPS (QtSPIM)
Iteración 1: Literales enteros, números en otras bases, strings, y print.
"""

from antlr4 import *
# pyrefly: ignore [missing-import]
from antlr.RaraLangListener import RaraLangListener


class MIPSListener(RaraLangListener):
    """
    Genera código ensamblador MIPS a partir del árbol de parseo de RaraLang.

    Estrategia de generación:
    - Sección .data: almacena las cadenas de texto (.asciiz).
    - Sección .text: instrucciones generadas en orden de visita del árbol.
    - Pila de valores (_val_stack): cada expresión evaluada deja un
      descriptor (tipo, valor) en la pila para que la sentencia padre
      sepa qué imprimir.
    """

    def __init__(self):
        self._data_lines: list[str] = []   # líneas para la sección .data
        self._text_lines: list[str] = []   # instrucciones MIPS
        self._val_stack: list[tuple] = []  # pila de descriptores de valor
        self._reg_idx: int = 0             # índice de registro temporal
        self._str_idx: int = 0             # índice de etiqueta de string
        self._variables: set[str] = set()  # nombres de variables usadas
        self._var_types: dict[str, str] = {}  # tipos de variables (int, str)

    # ─── Utilidades privadas ─────────────────────────────────────────────────

    def _alloc_reg(self) -> str:
        """Devuelve el siguiente registro temporal disponible ($t0–$t9)."""
        reg = f"$t{self._reg_idx % 10}"
        self._reg_idx += 1
        return reg

    def _emit(self, *lines: str) -> None:
        """Agrega instrucciones con indentación a la sección .text."""
        for line in lines:
            self._text_lines.append(f"    {line}")

    def _emit_comment(self, comment: str) -> None:
        self._text_lines.append(f"    # {comment}")

    def _emit_print_int(self, reg: str) -> None:
        """Emite syscalls para imprimir un entero y luego un salto de línea."""
        self._emit(
            f"move $a0, {reg}",
            "li   $v0, 1",          # syscall 1 = print_int
            "syscall",
            "li   $a0, 10",         # ASCII '\n'
            "li   $v0, 11",         # syscall 11 = print_char
            "syscall",
        )

    def _emit_print_string(self, label: str) -> None:
        """Emite syscalls para imprimir una cadena y luego un salto de línea."""
        self._emit(
            f"la   $a0, {label}",
            "li   $v0, 4",          # syscall 4 = print_string
            "syscall",
            "li   $a0, 10",         # ASCII '\n'
            "li   $v0, 11",
            "syscall",
        )

    def _emit_print_string_ref(self, reg: str) -> None:
        """Emite syscalls para imprimir una cadena referenciada por dirección en un registro y luego un salto de línea."""
        self._emit(
            f"move $a0, {reg}",
            "li   $v0, 4",          # syscall 4 = print_string
            "syscall",
            "li   $a0, 10",         # ASCII '\n'
            "li   $v0, 11",
            "syscall",
        )

    # ─── Expresiones ─────────────────────────────────────────────────────────

    def exitInt(self, ctx) -> None:
        """Literal entero decimal, ej: 42  →  li $t0, 42"""
        value = int(ctx.INT().getText())
        reg = self._alloc_reg()
        self._emit_comment(f"int literal {value}")
        self._emit(f"li   {reg}, {value}")
        self._val_stack.append(("int", reg))

    def exitBased(self, ctx) -> None:
        """
        Número en otra base, ej: [FF:16] o [1010:2].
        Decisión de implementación: la conversión a decimal se hace en
        Python con int(digits, base) en tiempo de compilación. El MIPS
        generado solo ve el valor decimal — es equivalente a un INT literal.
        """
        raw = ctx.BASED_NUMBER().getText()  # ej: "[FF:16]"
        inner = raw[1:-1]                   # "FF:16"
        digits, base_str = inner.rsplit(":", 1)
        base = int(base_str)
        value = int(digits, base)
        reg = self._alloc_reg()
        self._emit_comment(f"based literal {raw} = {value}")
        self._emit(f"li   {reg}, {value}")
        self._val_stack.append(("int", reg))

    def exitString(self, ctx) -> None:
        """
        Cadena de texto, ej: "hola mundo".
        La cadena se declara en .data como .asciiz (terminada en null).
        En .text solo se emite la dirección (la); el print lo hace exitPrintStmt.
        """
        raw = ctx.STRING().getText()        # incluye comillas
        content = raw[1:-1]                 # sin comillas
        label = f"str_{self._str_idx}"
        self._str_idx += 1
        self._data_lines.append(f"    {label}: .asciiz \"{content}\"")
        self._val_stack.append(("str", label))

    # ─── Sentencias ──────────────────────────────────────────────────────────

    def exitPrintStmt(self, ctx) -> None:
        """
        Instrucción print.
        Al llegar aquí, el hijo (expr) ya fue evaluado y dejó un descriptor
        en la pila. Se consulta el tipo y se emite la syscall correspondiente.
        """
        kind, val = self._val_stack.pop()
        self._emit_comment(f"print ({kind})")
        if kind == "int":
            self._emit_print_int(val)
        elif kind == "str":
            self._emit_print_string(val)
        elif kind == "str_ref":
            self._emit_print_string_ref(val)

    def exitAssignStmt(self, ctx) -> None:
        """
        Sentencia de asignación, ej: x <-- 10
        El valor de la expresión está en la pila de valores.
        """
        var_name = ctx.ID().getText()
        kind, val = self._val_stack.pop()
        self._variables.add(var_name)
        self._var_types[var_name] = kind

        self._emit_comment(f"assign {var_name} <-- {val}")
        if kind == "int":
            self._emit(f"sw   {val}, var_{var_name}")
        elif kind == "str":
            reg = self._alloc_reg()
            self._emit(f"la   {reg}, {val}")
            self._emit(f"sw   {reg}, var_{var_name}")
        elif kind == "str_ref":
            self._emit(f"sw   {val}, var_{var_name}")

    def exitVarExpr(self, ctx) -> None:
        """
        Variable como expresión: ID
        Recupera el valor almacenado en la variable y lo deja en un registro.
        """
        var_name = ctx.ID().getText()
        self._variables.add(var_name)

        kind = self._var_types.get(var_name, "int")
        reg = self._alloc_reg()

        self._emit_comment(f"read var {var_name}")
        self._emit(f"lw   {reg}, var_{var_name}")

        if kind == "str" or kind == "str_ref":
            self._val_stack.append(("str_ref", reg))
        else:
            self._val_stack.append(("int", reg))

    # ─── Salida ──────────────────────────────────────────────────────────────

    def output(self) -> str:
        """
        Ensambla el código MIPS completo:
          .data  → variables y strings declaradas
          .text  → instrucciones generadas + exit al final
        """
        lines: list[str] = []

        # Sección de datos
        lines.append(".data")
        for var in sorted(self._variables):
            lines.append(f"    var_{var}: .word 0")
        if self._data_lines:
            lines.extend(self._data_lines)
        lines.append("")

        # Sección de código
        lines.append(".text")
        lines.append(".globl main")
        lines.append("main:")
        lines.extend(self._text_lines)

        # Salida limpia del programa
        lines.append("    li   $v0, 10")   # syscall 10 = exit
        lines.append("    syscall")

        return "\n".join(lines) + "\n"