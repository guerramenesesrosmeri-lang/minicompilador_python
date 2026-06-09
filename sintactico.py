"""
sintactico.py — Análisis sintáctico (OE2)
Valida que las instrucciones tengan la estructura correcta.
Regla: IDENTIFICADOR = VALOR [OPERADOR VALOR ...]
"""

# ── Colores ANSI ──────────────────────────────────────────────────────────────
RESET    = "\033[0m"
BOLD     = "\033[1m"
VERDE    = "\033[92m"
ROJO     = "\033[91m"
CYAN     = "\033[96m"
GRIS     = "\033[90m"
AMARILLO = "\033[93m"

VALORES_VALIDOS   = {'NUMERO', 'CADENA', 'BOOLEANO', 'IDENTIFICADOR'}
OPERADORES_VALIDOS = {'SUMA', 'RESTA', 'MULT', 'DIV'}


def analizar_sintactico(tokens):
    errores = []

    if not tokens:
        errores.append("Instrucción vacía")
        return errores

    if len(tokens) < 3:
        errores.append("Instrucción incompleta: se necesita VARIABLE = VALOR")
        return errores

    if tokens[0][0] != 'IDENTIFICADOR':
        errores.append(f"Se esperaba una variable al inicio, se encontró: '{tokens[0][1]}'")

    if tokens[1][0] != 'ASIGNACION':
        errores.append(f"Se esperaba '=', se encontró: '{tokens[1][1]}'")

    if tokens[2][0] not in VALORES_VALIDOS:
        errores.append(f"Valor inválido tras '=': '{tokens[2][1]}'")

    i = 3
    while i < len(tokens):
        if tokens[i][0] not in OPERADORES_VALIDOS:
            errores.append(f"Operador inválido: '{tokens[i][1]}'")
            break
        i += 1
        if i >= len(tokens):
            errores.append("Falta un valor después del operador")
            break
        if tokens[i][0] not in VALORES_VALIDOS:
            errores.append(f"Se esperaba un valor, se encontró: '{tokens[i][1]}'")
        i += 1

    return errores


# ── Ejecución directa ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    from lexico import analizar_lexico

    ejemplos = [
        'x = 10',
        'nombre = "Carlos"',
        'pi = 3.14',
        'total = x + 3',
        '= 10',
        'x 10',
        'resultado = y',
    ]

    ancho = 55
    print(f"\n{BOLD}{CYAN}  ╔{'═' * ancho}╗")
    print(f"  ║{'  📐  ANÁLISIS SINTÁCTICO — OE2':^{ancho}}║")
    print(f"  ╚{'═' * ancho}╝{RESET}\n")

    ok = err = 0
    for i, codigo in enumerate(ejemplos, 1):
        tokens, err_lex = analizar_lexico(codigo)
        print(f"  {BOLD}{i:>2}.{RESET} {AMARILLO}{codigo:<32}{RESET}", end="  ")
        if err_lex:
            print(f"{ROJO}❌ Error léxico: {err_lex[0]}{RESET}")
            err += 1
        else:
            errores = analizar_sintactico(tokens)
            if errores:
                print(f"{ROJO}❌ Error sintáctico{RESET}")
                for e in errores:
                    print(f"      {ROJO}↳ {e}{RESET}")
                err += 1
            else:
                print(f"{VERDE}✅ Sintaxis correcta{RESET}")
                ok += 1

    print(f"\n  {GRIS}{'─' * ancho}")
    print(f"  Total: {len(ejemplos)} | ✅ {ok} correctas | ❌ {err} con errores{RESET}\n")