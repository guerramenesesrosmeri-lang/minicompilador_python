"""
traductor.py — Traducción a código Python (OE5)
Convierte instrucciones válidas del lenguaje de asignaciones
en código Python ejecutable.
"""
 
from lexico     import analizar_lexico
from sintactico import analizar_sintactico
from semantico  import analizar_semantico, resetear_tabla, tabla_simbolos
 
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
 
 
def traducir_a_python(tokens):
    """Convierte tokens válidos a una línea de código Python."""
    return ' '.join(val for _, val in tokens)
 
 
def compilar(instrucciones):
    """
    Valida y traduce una lista de instrucciones.
    Retorna (codigo_python_str, lista_de_reportes).
    """
    resetear_tabla()
    lineas_python = []
    reporte = []
 
    for i, instruccion in enumerate(instrucciones, 1):
        entrada = instruccion.strip()
        if not entrada:
            continue
 
        info = {'numero': i, 'instruccion': entrada, 'estado': '', 'python': '', 'error': ''}
 
        tokens, err_lex = analizar_lexico(entrada)
        if err_lex:
            info['estado'] = 'ERROR_LEXICO'
            info['error']  = err_lex[0]
            reporte.append(info); continue
 
        err_sint = analizar_sintactico(tokens)
        if err_sint:
            info['estado'] = 'ERROR_SINTACTICO'
            info['error']  = err_sint[0]
            reporte.append(info); continue
 
        err_sem = analizar_semantico(tokens)
        if err_sem:
            info['estado'] = 'ERROR_SEMANTICO'
            info['error']  = err_sem[0]
            reporte.append(info); continue
 
        linea = traducir_a_python(tokens)
        lineas_python.append(linea)
        info['estado'] = 'OK'
        info['python'] = linea
        reporte.append(info)
 
    return '\n'.join(lineas_python), reporte
 
 
# ── Ejecución directa ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    instrucciones = [
        'x = 10',
        'nombre = "Carlos"',
        'activo = True',
        'pi = 3.14',
        'total = x + 3',
        'doble = pi + pi',
        '= 10',
        'resultado = y',
        'area = pi * 2',
        'precio = 9.99',
    ]
 
    codigo_generado, reporte = compilar(instrucciones)
 
    ancho = 68
    print(f"\n{BOLD}{CYAN}  ╔{'═' * ancho}╗")
    print(f"  ║{'  🐍  MINICOMPILADOR — TRADUCCIÓN A PYTHON — OE5':^{ancho}}║")
    print(f"  ╠{'═' * ancho}╣")
    print(f"  ║  {'#':<4} {'Instrucción':<28} {'Estado':<14} {'Python generado':<20}║")
    print(f"  ╠{'═' * ancho}╣{RESET}")
 
    ok = err = 0
    for item in reporte:
        n   = item['numero']
        src = item['instruccion']
        if item['estado'] == 'OK':
            py  = item['python']
            print(f"  {BOLD}║{RESET}  {AMARILLO}{n:<4}{RESET} {src:<28} {VERDE}✅ OK{RESET:<14}         {AZUL}{py:<20}{RESET}{BOLD}║{RESET}")
            ok += 1
        else:
            tipo = item['estado'].replace('ERROR_', '').capitalize()
            print(f"  {BOLD}║{RESET}  {AMARILLO}{n:<4}{RESET} {src:<28} {ROJO}❌ {tipo:<11}{RESET}                     {BOLD}║{RESET}")
            print(f"  {BOLD}║{RESET}       {GRIS}↳ {item['error']}{RESET}")
            err += 1
 
    print(f"{BOLD}{CYAN}  ╠{'═' * ancho}╣")
    print(f"  ║  Total: {len(reporte)}  │  ✅ {ok} traducidas  │  ❌ {err} con errores{'':<21}║")
    print(f"  ╚{'═' * ancho}╝{RESET}\n")
 
    if codigo_generado:
        print(f"{BOLD}{MAGENTA}  ┌{'─' * ancho}┐")
        print(f"  │{'  📄  CÓDIGO PYTHON GENERADO':^{ancho}}│")
        print(f"  ├{'─' * ancho}┤{RESET}")
        for linea in codigo_generado.splitlines():
            print(f"  {BOLD}{MAGENTA}│{RESET}  {AZUL}{linea:<{ancho-2}}{RESET}{BOLD}{MAGENTA}│{RESET}")
        print(f"{BOLD}{MAGENTA}  └{'─' * ancho}┘{RESET}\n")
 
        print(f"{BOLD}{VERDE}  ┌{'─' * ancho}┐")
        print(f"  │{'  ▶   EJECUCIÓN DEL CÓDIGO GENERADO':^{ancho}}│")
        print(f"  ├{'─' * ancho}┤{RESET}")
        try:
            exec(codigo_generado)
            print(f"  {VERDE}  Código ejecutado correctamente ✅{RESET}")
            print(f"  {GRIS}  Variables: {tabla_simbolos}{RESET}")
        except Exception as e:
            print(f"  {ROJO}  Error al ejecutar: {e}{RESET}")
        print(f"{BOLD}{VERDE}  └{'─' * ancho}┘{RESET}\n")