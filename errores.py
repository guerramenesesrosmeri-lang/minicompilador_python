"""
errores.py — Reporte integrado de errores (OE4)
Ejecuta los tres analizadores y muestra un reporte consolidado.
"""

from lexico     import analizar_lexico
from sintactico import analizar_sintactico
from semantico  import analizar_semantico, resetear_tabla

# ── Colores ANSI ──────────────────────────────────────────────────────────────
RESET    = "\033[0m"
BOLD     = "\033[1m"
VERDE    = "\033[92m"
ROJO     = "\033[91m"
CYAN     = "\033[96m"
GRIS     = "\033[90m"
AMARILLO = "\033[93m"
AZUL     = "\033[94m"
MAGENTA  = "\033[95m"


def analizar_errores(codigo):
    reporte = {
        'codigo':              codigo,
        'errores_lexicos':     [],
        'errores_sintacticos': [],
        'errores_semanticos':  [],
        'total_errores':       0,
    }

    tokens, err_lex = analizar_lexico(codigo)
    reporte['errores_lexicos'] = err_lex
    if err_lex:
        reporte['total_errores'] = len(err_lex)
        return reporte

    err_sint = analizar_sintactico(tokens)
    reporte['errores_sintacticos'] = err_sint
    if err_sint:
        reporte['total_errores'] = len(err_sint)
        return reporte

    err_sem = analizar_semantico(tokens)
    reporte['errores_semanticos'] = err_sem
    reporte['total_errores'] = len(err_sem)
    return reporte


# ── Ejecución directa ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    resetear_tabla()

    ejemplos = [
        'x = 10',
        'nombre = "Carlos"',
        'activo = True',
        'pi = 3.14',
        'total = x + 3',
        'doble = pi + pi',
        '= 10',
        'x 10',
        'resultado = y',
        'area = pi * 2',
    ]

    ancho = 62
    print(f"\n{BOLD}{CYAN}  ╔{'═' * ancho}╗")
    print(f"  ║{'  ⚠️   MINICOMPILADOR — REPORTE DE ERRORES — OE4':^{ancho}}║")
    print(f"  ╠{'═' * ancho}╣")
    print(f"  ║  {'#':<4} {'Instrucción':<32} {'Estado':<24}║")
    print(f"  ╠{'═' * ancho}╣{RESET}")

    sin_errores = 0
    con_errores = 0

    for i, codigo in enumerate(ejemplos, 1):
        reporte = analizar_errores(codigo)
        if reporte['total_errores'] == 0:
            estado = f"{VERDE}✅ OK{RESET}"
            detalle = ""
            sin_errores += 1
        else:
            if reporte['errores_lexicos']:
                tipo = "Léxico"
                detalle = reporte['errores_lexicos'][0]
            elif reporte['errores_sintacticos']:
                tipo = "Sintáctico"
                detalle = reporte['errores_sintacticos'][0]
            else:
                tipo = "Semántico"
                detalle = reporte['errores_semanticos'][0]
            estado = f"{ROJO}❌ Error {tipo}{RESET}"
            con_errores += 1

        print(f"  {BOLD}║{RESET}  {AMARILLO}{i:<4}{RESET} {codigo:<32} {estado:<33}{BOLD}║{RESET}")
        if detalle:
            print(f"  {BOLD}║{RESET}       {GRIS}↳ {detalle}{RESET}")

    print(f"{BOLD}{CYAN}  ╠{'═' * ancho}╣")
    print(f"  ║  Total: {len(ejemplos)}  │  ✅ {sin_errores} correctas  │  ❌ {con_errores} con errores{'':<14}║")
    print(f"  ╚{'═' * ancho}╝{RESET}\n")