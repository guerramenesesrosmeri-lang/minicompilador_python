# sintactico.py - Analisis sintactico (OE2)
# Valida que las instrucciones tengan la estructura correcta
# Regla esperada: IDENTIFICADOR = VALOR [OPERADOR VALOR ...]

VALORES_VALIDOS    = {'NUMERO', 'CADENA', 'BOOLEANO', 'IDENTIFICADOR'}
OPERADORES_VALIDOS = {'SUMA', 'RESTA', 'MULT', 'DIV'}


def analizar_sintactico(tokens):
    errores = []

    if not tokens:
        errores.append("Instruccion vacia")
        return errores

    if len(tokens) < 3:
        errores.append("Instruccion incompleta, se necesita: VARIABLE = VALOR")
        return errores

    # El primer token debe ser una variable
    if tokens[0][0] != 'IDENTIFICADOR':
        errores.append(f"Se esperaba una variable al inicio, se encontro: '{tokens[0][1]}'")

    # El segundo token debe ser el signo igual
    if tokens[1][0] != 'ASIGNACION':
        errores.append(f"Se esperaba '=', se encontro: '{tokens[1][1]}'")

    # El tercer token debe ser un valor valido
    if tokens[2][0] not in VALORES_VALIDOS:
        errores.append(f"Valor invalido despues de '=': '{tokens[2][1]}'")

    # Si hay mas tokens, deben seguir el patron: OPERADOR VALOR
    i = 3
    while i < len(tokens):
        if tokens[i][0] not in OPERADORES_VALIDOS:
            errores.append(f"Operador invalido: '{tokens[i][1]}'")
            break
        i += 1
        if i >= len(tokens):
            errores.append("Falta un valor despues del operador")
            break
        if tokens[i][0] not in VALORES_VALIDOS:
            errores.append(f"Se esperaba un valor, se encontro: '{tokens[i][1]}'")
        i += 1

    return errores


# Prueba del modulo
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

    print("\n--- ANALISIS SINTACTICO (OE2) ---\n")

    ok = 0
    err = 0
    for i, codigo in enumerate(ejemplos, 1):
        tokens, err_lex = analizar_lexico(codigo)
        print(f"{i}. Instruccion: {codigo}")
        if err_lex:
            print(f"   Error lexico: {err_lex[0]}")
            err += 1
        else:
            errores = analizar_sintactico(tokens)
            if errores:
                for e in errores:
                    print(f"   Error sintactico: {e}")
                err += 1
            else:
                print(f"   Estado: OK")
                ok += 1
        print()

    print(f"Total: {len(ejemplos)} | Correctas: {ok} | Con errores: {err}\n")