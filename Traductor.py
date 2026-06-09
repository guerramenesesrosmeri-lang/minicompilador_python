# traductor.py - Traduccion a codigo Python (OE5)
# Convierte instrucciones validas del lenguaje de asignaciones
# en codigo Python ejecutable

from lexico     import analizar_lexico
from sintactico import analizar_sintactico
from semantico  import analizar_semantico, resetear_tabla, tabla_simbolos


def traducir_a_python(tokens):
    # Une los valores de los tokens para formar una linea Python
    return ' '.join(val for _, val in tokens)


def compilar(instrucciones):
    resetear_tabla()
    lineas_python = []
    reporte = []

    for i, instruccion in enumerate(instrucciones, 1):
        entrada = instruccion.strip()
        if not entrada:
            continue

        info = {
            'numero':     i,
            'instruccion': entrada,
            'estado':     '',
            'python':     '',
            'error':      ''
        }

        # Fase 1: analisis lexico
        tokens, err_lex = analizar_lexico(entrada)
        if err_lex:
            info['estado'] = 'ERROR_LEXICO'
            info['error']  = err_lex[0]
            reporte.append(info)
            continue

        # Fase 2: analisis sintactico
        err_sint = analizar_sintactico(tokens)
        if err_sint:
            info['estado'] = 'ERROR_SINTACTICO'
            info['error']  = err_sint[0]
            reporte.append(info)
            continue

        # Fase 3: analisis semantico
        err_sem = analizar_semantico(tokens)
        if err_sem:
            info['estado'] = 'ERROR_SEMANTICO'
            info['error']  = err_sem[0]
            reporte.append(info)
            continue

        # Si paso todas las fases, se traduce
        linea = traducir_a_python(tokens)
        lineas_python.append(linea)
        info['estado'] = 'OK'
        info['python'] = linea
        reporte.append(info)

    return '\n'.join(lineas_python), reporte


# Prueba del modulo
if __name__ == "__main__":
    instrucciones = [
        'x = 10',
        'nombre = "Carlos"',
        'activo = True',
        'pi = 3.14',
        'total = x + 3',
        'doble = pi + pi',
        '= 10',
        'resultado = y',
        'area = pi * 2',
        'precio = 9.99',
    ]

    codigo_generado, reporte = compilar(instrucciones)

    print("\n--- TRADUCCION A PYTHON (OE5) ---\n")
    print(f"{'#':<4} {'Instruccion':<28} {'Estado':<16} {'Python generado'}")
    print("-" * 65)

    ok = 0
    err = 0
    for item in reporte:
        if item['estado'] == 'OK':
            print(f"{item['numero']:<4} {item['instruccion']:<28} OK               {item['python']}")
            ok += 1
        else:
            tipo = item['estado'].replace('ERROR_', '').capitalize()
            print(f"{item['numero']:<4} {item['instruccion']:<28} Error {tipo}")
            print(f"       -> {item['error']}")
            err += 1

    print("-" * 65)
    print(f"Total: {len(reporte)} | Traducidas: {ok} | Con errores: {err}\n")

    if codigo_generado:
        print("--- CODIGO PYTHON GENERADO ---\n")
        print(codigo_generado)
        print()

        print("--- RESULTADO DE EJECUCION ---\n")
        try:
            exec(codigo_generado)
            print("Codigo ejecutado correctamente")
            print(f"Variables finales: {tabla_simbolos}")
        except Exception as e:
            print(f"Error al ejecutar: {e}")
        print()