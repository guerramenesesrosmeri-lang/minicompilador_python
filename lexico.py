# lexico.py - Analisis lexico (OE1)
# Reconoce los tokens del lenguaje de asignaciones

import re

# Definicion de los tipos de tokens que acepta el lenguaje
TOKENS = [
    ('NUMERO',        r'\d+(\.\d+)?'),
    ('CADENA',        r'"[^"]*"'),
    ('BOOLEANO',      r'\b(True|False)\b'),
    ('ASIGNACION',    r'='),
    ('SUMA',          r'\+'),
    ('RESTA',         r'-'),
    ('MULT',          r'\*'),
    ('DIV',           r'/'),
    ('LPAREN',        r'\('),
    ('RPAREN',        r'\)'),
    ('IDENTIFICADOR', r'[a-zA-Z_]\w*'),
    ('ESPACIO',       r'\s+'),
    ('DESCONOCIDO',   r'.'),
]


def analizar_lexico(codigo):
    tokens_encontrados = []
    errores = []
    posicion = 0

    while posicion < len(codigo):
        match = None
        for tipo, patron in TOKENS:
            m = re.compile(patron).match(codigo, posicion)
            if m:
                valor = m.group(0)
                if tipo == 'ESPACIO':
                    pass  # los espacios se ignoran
                elif tipo == 'DESCONOCIDO':
                    errores.append(f"Token desconocido: '{valor}' en posicion {posicion}")
                else:
                    tokens_encontrados.append((tipo, valor))
                posicion = m.end()
                match = m
                break
        if not match:
            errores.append(f"Error en posicion {posicion}")
            posicion += 1

    return tokens_encontrados, errores


# Prueba del modulo
if __name__ == "__main__":
    ejemplos = [
        'x = 10',
        'nombre = "Alejandro"',
        'total = x + 3',
        'resultado = (x + 5) * 2',
        'activo = True',
        'precio = 9.99',
        'dato = @invalido',
    ]

    print("\n--- ANALISIS LEXICO (OE1) ---\n")

    for i, codigo in enumerate(ejemplos, 1):
        tokens, errores = analizar_lexico(codigo)
        print(f"{i}. Instruccion: {codigo}")
        print(f"   Tokens: {tokens}")
        if errores:
            for e in errores:
                print(f"   Error: {e}")
        else:
            print(f"   Estado: OK")
        print()