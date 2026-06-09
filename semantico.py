# Análisis semántico - OE3
# Gestiona variables: verifica que estén declaradas antes de usarse

tabla_simbolos = {}  # diccionario de variables declaradas

def analizar_semantico(tokens):
    errores = []
    
    if len(tokens) < 3:
        return errores
    
    variable = tokens[1][1] if tokens[1][0] == 'ASIGNACION' else None
    valor_token = tokens[2] if len(tokens) > 2 else None

    # Verificar que el valor no sea una variable no declarada
    if valor_token and valor_token[0] == 'IDENTIFICADOR':
        if valor_token[1] not in tabla_simbolos:
            errores.append(f"Variable '{valor_token[1]}' usada sin declarar")

    # Registrar la variable en la tabla de símbolos
    if tokens[0][0] == 'IDENTIFICADOR' and tokens[1][0] == 'ASIGNACION':
        variable = tokens[0][1]
        tipo = valor_token[0] if valor_token else 'DESCONOCIDO'
        tabla_simbolos[variable] = tipo
    
    return errores


# Prueba
if __name__ == "__main__":
    from lexico import analizar_lexico
    from sintactico import analizar_sintactico

    ejemplos = [
        'x = 10',
        'total = x + 3',     # x ya fue declarada arriba
        'resultado = y',     # error: y no fue declarada
        'nombre = "Carlos"',
        'activo = True',
    ]

    for codigo in ejemplos:
        print(f"\nCódigo: {codigo}")
        tokens, errores_lexico = analizar_lexico(codigo)
        if errores_lexico:
            print(f"Error léxico: {errores_lexico}")
            continue
        errores_sint = analizar_sintactico(tokens)
        if errores_sint:
            print(f"Error sintáctico: {errores_sint}")
            continue
        errores_sem = analizar_semantico(tokens)
        if errores_sem:
            print(f"Error semántico: {errores_sem}")
        else:
            print(f"Semántica correcta ✅ | Tabla de símbolos: {tabla_simbolos}")