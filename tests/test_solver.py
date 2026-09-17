"""Pruebas automáticas de la lógica del resolutor de Sudoku."""

from src.solver import (
    buscar_casilla_vacia,
    casilla_tiene_conflicto,
    grupo_sin_repetidos,
    numero_es_valido,
    numero_valido_en_bloque,
    numero_valido_en_columna,
    numero_valido_en_fila,
    resolver,
    tablero_es_valido,
)


def crear_tablero_prueba():
    """Crea un Sudoku incompleto para las pruebas."""

    # Utilizamos el mismo ejemplo en varias pruebas para no repetirlo.
    return [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]


def test_buscar_primera_casilla_vacia():
    tablero = crear_tablero_prueba()

    resultado = buscar_casilla_vacia(tablero)

    assert resultado == (0, 2)


def test_tablero_completo_no_tiene_casilla_vacia():
    tablero_completo = [
        [1 for _ in range(9)]
        for _ in range(9)
    ]

    resultado = buscar_casilla_vacia(tablero_completo)

    assert resultado is None


def test_numero_valido_en_fila():
    tablero = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
    ] + [
        [0] * 9
        for _ in range(8)
    ]

    assert not numero_valido_en_fila(tablero, 5, 0)
    assert numero_valido_en_fila(tablero, 4, 0)


def test_numero_valido_en_columna():
    tablero = [
        [0] * 9
        for _ in range(9)
    ]
    tablero[0][2] = 8

    assert not numero_valido_en_columna(tablero, 8, 2)
    assert numero_valido_en_columna(tablero, 4, 2)


def test_numero_valido_en_bloque():
    tablero = [
        [0] * 9
        for _ in range(9)
    ]
    tablero[1][1] = 9

    assert not numero_valido_en_bloque(tablero, 9, 2, 2)
    assert numero_valido_en_bloque(tablero, 4, 2, 2)


def test_numero_es_valido_combina_las_tres_reglas():
    tablero = [
        [0] * 9
        for _ in range(9)
    ]

    tablero[0][5] = 4  # Misma fila que (0, 0).
    tablero[5][0] = 5  # Misma columna que (0, 0).
    tablero[1][1] = 6  # Mismo bloque que (0, 0).

    assert not numero_es_valido(tablero, 4, 0, 0)
    assert not numero_es_valido(tablero, 5, 0, 0)
    assert not numero_es_valido(tablero, 6, 0, 0)
    assert numero_es_valido(tablero, 7, 0, 0)


def test_resolver_completa_sudoku():
    tablero = crear_tablero_prueba()

    # Esta es la solución que debe producir el algoritmo.
    solucion_esperada = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]

    resultado = resolver(tablero)

    assert resultado is True
    assert tablero == solucion_esperada


def test_resolver_devuelve_false_si_no_hay_solucion():
    # La primera fila necesita un 9, pero la última columna ya contiene uno.
    tablero = [
        [1, 2, 3, 4, 5, 6, 7, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 9],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    # Guardamos una copia para comprobar que los intentos se deshacen.
    tablero_original = [
        fila.copy()
        for fila in tablero
    ]

    resultado = resolver(tablero)

    assert resultado is False
    assert tablero == tablero_original


def test_grupo_sin_repetidos_ignora_ceros():
    grupo_valido = [5, 3, 0, 0, 7, 0, 0, 0, 0]
    grupo_repetido = [5, 3, 0, 5, 7, 0, 0, 0, 0]

    assert grupo_sin_repetidos(grupo_valido)
    assert not grupo_sin_repetidos(grupo_repetido)


def test_tablero_es_valido_comprueba_estructura_y_filas():
    tablero_valido = crear_tablero_prueba()

    # Modificamos una cosa diferente en cada copia del tablero.
    tablero_con_repetido = crear_tablero_prueba()
    tablero_con_repetido[0][2] = 5

    tablero_con_valor_incorrecto = crear_tablero_prueba()
    tablero_con_valor_incorrecto[0][2] = 10

    tablero_con_ocho_filas = crear_tablero_prueba()[:8]

    assert tablero_es_valido(tablero_valido)
    assert not tablero_es_valido(tablero_con_repetido)
    assert not tablero_es_valido(tablero_con_valor_incorrecto)
    assert not tablero_es_valido(tablero_con_ocho_filas)


def test_tablero_es_valido_comprueba_columnas_y_bloques():
    tablero_con_repetido_en_columna = crear_tablero_prueba()
    tablero_con_repetido_en_columna[6][0] = 5

    tablero_con_repetido_en_bloque = crear_tablero_prueba()
    tablero_con_repetido_en_bloque[1][1] = 8

    assert not tablero_es_valido(
        tablero_con_repetido_en_columna
    )
    assert not tablero_es_valido(
        tablero_con_repetido_en_bloque
    )


def test_resolver_rechaza_un_tablero_completo_invalido():
    tablero_invalido = [
        [3, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]

    resultado = resolver(tablero_invalido)

    assert resultado is False


def test_casilla_tiene_conflicto():
    tablero = crear_tablero_prueba()

    tablero[0][2] = 5

    assert casilla_tiene_conflicto(tablero, 0, 2)
    assert tablero[0][2] == 5

    tablero[0][2] = 4

    assert not casilla_tiene_conflicto(tablero, 0, 2)
    assert tablero[0][2] == 4
