
"""
semantico.py — Análisis semántico (OE3)
Verifica que las variables estén declaradas antes de usarse.
Mantiene una tabla de símbolos con nombre → tipo.
"""
 
# ── Colores ANSI ──────────────────────────────────────────────────────────────
RESET    = "\033[0m"
BOLD     = "\033[1m"
VERDE    = "\033[92m"
ROJO     = "\033[91m"
CYAN     = "\033[96m"
GRIS     = "\033[90m"
AMARILLO = "\033[93m"
MAGENTA  = "\033[95m"
 
tabla_simbolos = {}   # { nombre_variable: tipo }
 
 
def analizar_semantico(tokens):
    errores = []
 
    if len(tokens) < 3:
        return errores
    if tokens[0][0] != 'IDENTIFICADOR' or tokens[1][0] != 'ASIGNACION':
        return errores
 
    variable_destino = tokens[0][1]
 
    # Verificar que todos los identificadores del lado derecho estén declarados
    for tok_tipo, tok_val in tokens[2:]:
        if tok_tipo == 'IDENTIFICADOR' and tok_val not in tabla_simbolos:
            errores.append(f"Variable '{tok_val}' usada sin declarar")
 
    # Si no hay errores, registrar la variable
    if not errores:
        tipo = tokens[2][0]
        tabla_simbolos[variable_destino] = tipo
 
    return errores
 
 
def resetear_tabla():
    tabla_simbolos.clear()
 
 
# ── Ejecución directa ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    from lexico    import analizar_lexico
    from sintactico import analizar_sintactico
 
    ejemplos = [
        'x = 10',
        'pi = 3.14',
        'total = x + 3',
        'resultado = y',
        'nombre = "Carlos"',
        'activo = True',
        'doble = pi + pi',
    ]
 
    resetear_tabla()
    ancho = 55
    print(f"\n{BOLD}{CYAN}  ╔{'═' * ancho}╗")
    print(f"  ║{'  🧠  ANÁLISIS SEMÁNTICO — OE3':^{ancho}}║")
    print(f"  ╚{'═' * ancho}╝{RESET}\n")
 
    ok = err = 0
    for i, codigo in enumerate(ejemplos, 1):
        tokens, err_lex = analizar_lexico(codigo)
        print(f"  {BOLD}{i:>2}.{RESET} {AMARILLO}{codigo:<32}{RESET}", end="  ")
        if err_lex:
            print(f"{ROJO}❌ Error léxico: {err_lex[0]}{RESET}")
            err += 1; continue
        err_sint = analizar_sintactico(tokens)
        if err_sint:
            print(f"{ROJO}❌ Error sintáctico: {err_sint[0]}{RESET}")
            err += 1; continue
        err_sem = analizar_semantico(tokens)
        if err_sem:
            print(f"{ROJO}❌ Error semántico{RESET}")
            for e in err_sem:
                print(f"      {ROJO}↳ {e}{RESET}")
            err += 1
        else:
            print(f"{VERDE}✅ Semántica correcta{RESET}")
            print(f"      {GRIS}Tabla: {tabla_simbolos}{RESET}")
            ok += 1
 
    print(f"\n  {GRIS}{'─' * ancho}")
    print(f"  Total: {len(ejemplos)} | ✅ {ok} correctas | ❌ {err} con errores{RESET}\n")