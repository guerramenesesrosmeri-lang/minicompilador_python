# Análisis de errores - OE4
from lexico import analizar_lexico
from sintactico import analizar_sintactico
from semantico import analizar_semantico

def analizar_errores(codigo):
    reporte = {
        'codigo': codigo,
        'errores_lexicos': [],
        'errores_sintacticos': [],
        'errores_semanticos': [],
        'total_errores': 0
    }

    tokens, errores_lexicos = analizar_lexico(codigo)
    reporte['errores_lexicos'] = errores_lexicos
    if errores_lexicos:
        reporte['total_errores'] = len(errores_lexicos)
        return reporte

    errores_sint = analizar_sintactico(tokens)
    reporte['errores_sintacticos'] = errores_sint
    if errores_sint:
        reporte['total_errores'] = len(errores_sint)
        return reporte

    errores_sem = analizar_semantico(tokens)
    reporte['errores_semanticos'] = errores_sem
    reporte['total_errores'] = len(errores_sem)
    return reporte


if __name__ == "__main__":
    ejemplos = [
        'x = 10',
        'nombre = "Carlos"',
        '= 10',
        'x 10',
        'resultado = y',
        'total = x + 3',
    ]

    print("\n  MINICOMPILADOR — REPORTE DE ERRORES")
    print("  " + "─" * 45)

    sin_errores = 0
    con_errores = 0

    for i, codigo in enumerate(ejemplos, 1):
        reporte = analizar_errores(codigo)
        if reporte['total_errores'] == 0:
            print(f"  {i}. {codigo:<30} ✅ OK")
            sin_errores += 1
        else:
            if reporte['errores_lexicos']:
                print(f"  {i}. {codigo:<30} ❌ Error léxico")
            elif reporte['errores_sintacticos']:
                print(f"  {i}. {codigo:<30} ❌ Error sintáctico")
            elif reporte['errores_semanticos']:
                print(f"  {i}. {codigo:<30} ❌ Error semántico")
            con_errores += 1

    print("  " + "─" * 45)
    print(f"  Total: {len(ejemplos)} | ✅ {sin_errores} correctas | ❌ {con_errores} con errores\n")