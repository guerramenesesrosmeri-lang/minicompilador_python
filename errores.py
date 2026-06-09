# errores.py - Reporte de errores (OE4)
# Ejecuta los tres analizadores y muestra un reporte consolidado

from lexico     import analizar_lexico
from sintactico import analizar_sintactico
from semantico  import analizar_semantico, resetear_tabla


def analizar_errores(codigo):
    # Estructura del reporte para una instruccion
    reporte = {
        'codigo':              codigo,
        'errores_lexicos':     [],
        'errores_sintacticos': [],
        'errores_semanticos':  [],
        'total_errores':       0,
    }

    # Primero se analiza el lexico
    tokens, err_lex = analizar_lexico(codigo)
    reporte['errores_lexicos'] = err_lex
    if err_lex:
        reporte['total_errores'] = len(err_lex)
        return reporte

    # Si paso el lexico, se analiza el sintactico
    err_sint = analizar_sintactico(tokens)
    reporte['errores_sintacticos'] = err_sint
    if err_sint:
        reporte['total_errores'] = len(err_sint)
        return reporte

    # Si paso el sintactico, se analiza el semantico
    err_sem = analizar_semantico(tokens)
    reporte['errores_semanticos'] = err_sem
    reporte['total_errores'] = len(err_sem)
    return reporte


# Prueba del modulo
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

    print("\n--- REPORTE DE ERRORES (OE4) ---\n")
    print(f"{'#':<4} {'Instruccion':<30} {'Estado'}")
    print("-" * 55)

    sin_errores = 0
    con_errores = 0

    for i, codigo in enumerate(ejemplos, 1):
        reporte = analizar_errores(codigo)

        if reporte['total_errores'] == 0:
            print(f"{i:<4} {codigo:<30} OK")
            sin_errores += 1
        else:
            if reporte['errores_lexicos']:
                tipo    = "Lexico"
                detalle = reporte['errores_lexicos'][0]
            elif reporte['errores_sintacticos']:
                tipo    = "Sintactico"
                detalle = reporte['errores_sintacticos'][0]
            else:
                tipo    = "Semantico"
                detalle = reporte['errores_semanticos'][0]
            print(f"{i:<4} {codigo:<30} Error {tipo}")
            print(f"       -> {detalle}")
            con_errores += 1

    print("-" * 55)
    print(f"Total: {len(ejemplos)} | Correctas: {sin_errores} | Con errores: {con_errores}\n")