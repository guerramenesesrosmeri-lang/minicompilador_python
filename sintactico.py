# Análisis sintáctico - OE2
# Valida que las instrucciones tengan la estructura correcta

def analizar_sintactico(tokens):
    errores = []
    
    if len(tokens) < 3:
        errores.append("Instrucción incompleta")
        return errores
    
    # Regla: IDENTIFICADOR = VALOR
    if tokens[0][0] != 'IDENTIFICADOR':
        errores.append(f"Se esperaba una variable, se encontró: {tokens[0][1]}")
    
    if tokens[1][0] != 'ASIGNACION':
        errores.append(f"Se esperaba '=', se encontró: {tokens[1][1]}")
    
    valores_validos = ['NUMERO', 'CADENA', 'BOOLEANO', 'IDENTIFICADOR']
    if tokens[2][0] not in valores_validos:
        errores.append(f"Valor inválido: {tokens[2][1]}")
    
    return errores


# Prueba
if __name__ == "__main__":
    from lexico import analizar_lexico

    ejemplos = [
        'x = 10',
        'nombre = "Carlos"',
        '= 10',           # error: falta variable
        'x 10',           # error: falta =
        'total = x + 3',
    ]

    for codigo in ejemplos:
        print(f"\nCódigo: {codigo}")
        tokens, errores_lexico = analizar_lexico(codigo)
        if errores_lexico:
            print(f"Error léxico: {errores_lexico}")
        else:
            errores_sint = analizar_sintactico(tokens)
            if errores_sint:
                print(f"Error sintáctico: {errores_sint}")
            else:
                print("Sintaxis correcta ✅")