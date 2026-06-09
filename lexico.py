"""
lexico.py — Análisis léxico (OE1)
Reconoce tokens del lenguaje de asignaciones.
"""

import re

# ── Colores ANSI ──────────────────────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
VERDE  = "\033[92m"
ROJO   = "\033[91m"
CYAN   = "\033[96m"
GRIS   = "\033[90m"
AMARILLO = "\033[93m"

# ── Definición de tokens ──────────────────────────────────────────────────────
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
                    pass
                elif tipo == 'DESCONOCIDO':
                    errores.append(f"Token desconocido: '{valor}' en posición {posicion}")
                else:
                    tokens_encontrados.append((tipo, valor))
                posicion = m.end()
                match = m
                break
        if not match:
            errores.append(f"Error en posición {posicion}")
            posicion += 1

    return tokens_encontrados, errores


# ── Ejecución directa ─────────────────────────────────────────────────────────
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

    ancho = 55
    print(f"\n{BOLD}{CYAN}  ╔{'═' * ancho}╗")
    print(f"  ║{'  🔍  ANÁLISIS LÉXICO — OE1':^{ancho}}║")
    print(f"  ╚{'═' * ancho}╝{RESET}\n")

    for i, codigo in enumerate(ejemplos, 1):
        tokens, errores = analizar_lexico(codigo)
        estado = f"{VERDE}✅ OK{RESET}" if not errores else f"{ROJO}❌ ERROR{RESET}"
        print(f"  {BOLD}{i:>2}.{RESET} {AMARILLO}{codigo:<32}{RESET} {estado}")
        print(f"      {GRIS}Tokens: {tokens}{RESET}")
        if errores:
            for e in errores:
                print(f"      {ROJO}↳ {e}{RESET}")
        print()

    print(f"  {GRIS}{'─' * ancho}{RESET}\n")