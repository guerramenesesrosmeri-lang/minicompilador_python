import re

# Definición de tokens del lenguaje de asignaciones
TOKENS = [
    ('NUMERO',    r'\d+(\.\d+)?'),        # 1, 2.5, 100
    ('CADENA',    r'"[^"]*"'),            # "hola", "Gina"
    ('BOOLEANO',  r'\b(True|False)\b'),   # True, False
    ('ASIGNACION',r'='),                  # =
    ('SUMA',      r'\+'),                 # +
    ('RESTA',     r'-'),                  # -
    ('MULT',      r'\*'),                 # *
    ('DIV',       r'/'),                  # /
    ('LPAREN',    r'\('),                 # (
    ('RPAREN',    r'\)'),                 # )
    ('IDENTIFICADOR', r'[a-zA-Z_]\w*'),  # variables: x, total, nombre
    ('ESPACIO',   r'\s+'),               # espacios (se ignoran)
    ('DESCONOCIDO', r'.'),              # cualquier otro caracter
]

def analizar_lexico(codigo):
    tokens_encontrados = []
    errores = []
    posicion = 0

    while posicion < len(codigo):
        match = None
        for tipo, patron in TOKENS:
            regex = re.compile(patron)
            match = regex.match(codigo, posicion)
            if match:
                valor = match.group(0)
                if tipo == 'ESPACIO':
                    pass  # ignorar espacios
                elif tipo == 'DESCONOCIDO':
                    errores.append(f"Token desconocido: '{valor}' en posición {posicion}")
                else:
                    tokens_encontrados.append((tipo, valor))
                posicion = match.end()
                break

        if not match:
            errores.append(f"Error en posición {posicion}")
            posicion += 1

    return tokens_encontrados, errores


# Prueba del analizador léxico
if __name__ == "__main__":
    ejemplos = [
        'x = 10',
        'nombre = "Gina"',
        'total = x + 3',
        'resultado = (x + 5) * 2',
        'activo = True',
    ]

    for codigo in ejemplos:
        print(f"\nCódigo: {codigo}")
        tokens, errores = analizar_lexico(codigo)
        print(f"Tokens encontrados: {tokens}")
        if errores:
            print(f"Errores: {errores}")
        else:
            print("Sin errores ✅")