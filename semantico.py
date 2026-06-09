# semantico.py - Analisis semantico (OE3)
# Verifica que las variables se declaren antes de usarse
# Usa una tabla de simbolos para guardar: nombre -> tipo

tabla_simbolos = {}


def analizar_semantico(tokens):
    errores = []

    # Se necesitan al menos 3 tokens: variable = valor
    if len(tokens) < 3:
        return errores

    # El patron esperado es: IDENTIFICADOR = ...
    if tokens[0][0] != 'IDENTIFICADOR' or tokens[1][0] != 'ASIGNACION':
        return errores

    variable_destino = tokens[0][1]

    # Revisar que los identificadores del lado derecho ya esten declarados
    for tok_tipo, tok_val in tokens[2:]:
        if tok_tipo == 'IDENTIFICADOR' and tok_val not in tabla_simbolos:
            errores.append(f"Variable '{tok_val}' usada sin declarar")

    # Si no hubo errores, se registra la variable en la tabla
    if not errores:
        tipo = tokens[2][0]
        tabla_simbolos[variable_destino] = tipo

    return errores


def resetear_tabla():
    tabla_simbolos.clear()


# Prueba del modulo
if __name__ == "__main__":
    from lexico import analizar_lexico
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
    print("\n--- ANALISIS SEMANTICO (OE3) ---\n")

    ok = 0
    err = 0
    for i, codigo in enumerate(ejemplos, 1):
        tokens, err_lex = analizar_lexico(codigo)
        print(f"{i}. Instruccion: {codigo}")
        if err_lex:
            print(f"   Error lexico: {err_lex[0]}")
            err += 1
            continue
        err_sint = analizar_sintactico(tokens)
        if err_sint:
            print(f"   Error sintactico: {err_sint[0]}")
            err += 1
            continue
        err_sem = analizar_semantico(tokens)
        if err_sem:
            for e in err_sem:
                print(f"   Error semantico: {e}")
            err += 1
        else:
            print(f"   Estado: OK")
            print(f"   Tabla actual: {tabla_simbolos}")
            ok += 1
        print()

    print(f"Total: {len(ejemplos)} | Correctas: {ok} | Con errores: {err}\n")