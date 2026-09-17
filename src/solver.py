# El número 0 representa una casilla que todavía está vacía.
TABLERO_INICIAL = [
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


def buscar_casilla_vacia(tablero):
    """Devuelve la posición de la primera casilla vacía."""

    # Recorremos el tablero por filas, de izquierda a derecha.
    for fila in range(9):
        for columna in range(9):
            if tablero[fila][columna] == 0:
                return (fila, columna)

    # Si no encontramos ningún cero, el tablero está completo.
    return None


def grupo_sin_repetidos(valores):
    """Comprueba que un grupo no contenga números repetidos."""

    # Un set permite guardar los números que ya hemos encontrado.
    numeros_vistos = set()

    for valor in valores:
        # Los ceros son casillas vacías y no cuentan como repetidos.
        if valor == 0:
            continue

        if valor in numeros_vistos:
            return False

        numeros_vistos.add(valor)

    return True


def tablero_es_valido(tablero):
    """Comprueba la estructura y las reglas del tablero."""

    # Un Sudoku siempre debe tener nueve filas.
    if len(tablero) != 9:
        return False

    # Comprobamos el tamaño, los valores y los repetidos de cada fila.
    for fila in tablero:
        if len(fila) != 9:
            return False

        for valor in fila:
            if not isinstance(valor, int):
                return False

            if valor < 0 or valor > 9:
                return False

        if not grupo_sin_repetidos(fila):
            return False

    # Construimos cada columna para comprobarla como un grupo.
    for columna in range(9):
        valores_columna = [
            tablero[fila][columna]
            for fila in range(9)
        ]

        if not grupo_sin_repetidos(valores_columna):
            return False

    # Los bloques comienzan en las posiciones 0, 3 y 6.
    for inicio_fila in range(0, 9, 3):
        for inicio_columna in range(0, 9, 3):
            valores_bloque = []

            for fila in range(inicio_fila, inicio_fila + 3):
                for columna in range(
                    inicio_columna,
                    inicio_columna + 3,
                ):
                    valores_bloque.append(
                        tablero[fila][columna]
                    )

            if not grupo_sin_repetidos(valores_bloque):
                return False

    return True


def numero_valido_en_fila(tablero, numero, fila):
    """Comprueba que un número no esté repetido en una fila."""

    for columna in range(9):
        if tablero[fila][columna] == numero:
            return False

    return True


def numero_valido_en_columna(tablero, numero, columna):
    """Comprueba que un número no esté repetido en una columna."""

    # Recorre las nueve filas
    for fila in range(9):
        if tablero[fila][columna] == numero:
            return False

    return True


def numero_valido_en_bloque(tablero, numero, fila, columna):
    """Comprueba que un número no esté repetido en su bloque 3x3."""

    # La división entera permite encontrar el inicio del bloque.
    inicio_fila = (fila // 3) * 3
    inicio_columna = (columna // 3) * 3

    for f in range(inicio_fila, inicio_fila + 3):
        for c in range(inicio_columna, inicio_columna + 3):
            if tablero[f][c] == numero:
                return False

    return True


def numero_es_valido(tablero, numero, fila, columna):
    """Comprueba si un número puede colocarse en una posición."""

    valida_fila = numero_valido_en_fila(tablero, numero, fila)
    valida_columna = numero_valido_en_columna(
        tablero,
        numero,
        columna,
    )
    valida_bloque = numero_valido_en_bloque(
        tablero,
        numero,
        fila,
        columna,
    )

    # El número debe cumplir las tres reglas al mismo tiempo.
    return valida_fila and valida_columna and valida_bloque


def casilla_tiene_conflicto(tablero, fila, columna):
    """Comprueba si el valor de una casilla incumple alguna regla."""

    numero = tablero[fila][columna]

    if numero == 0:
        return False

    # Vaciamos la casilla temporalmente para que no se compare consigo misma.
    tablero[fila][columna] = 0

    es_valido = numero_es_valido(
        tablero,
        numero,
        fila,
        columna,
    )

    tablero[fila][columna] = numero

    return not es_valido


def _resolver_con_backtracking(tablero):
    """Resuelve el tablero utilizando backtracking."""

    # Empezamos siempre por la primera casilla que esté vacía.
    posicion = buscar_casilla_vacia(tablero)

    # Caso base: si no quedan casillas vacías, hemos terminado.
    if posicion is None:
        return True

    fila, columna = posicion

    # Probamos todos los números posibles en la casilla.
    for numero in range(1, 10):
        if numero_es_valido(tablero, numero, fila, columna):
            tablero[fila][columna] = numero

            # Intentamos resolver el resto del tablero con este número.
            if _resolver_con_backtracking(tablero):
                return True

            # Si no funciona, deshacemos el cambio y probamos otro número.
            tablero[fila][columna] = 0

    # Ningún número es válido, por lo que volvemos a la casilla anterior.
    return False


def resolver(tablero):
    """Valida y resuelve un tablero de Sudoku."""

    # No intentamos resolver un tablero que ya incumple las reglas.
    if not tablero_es_valido(tablero):
        return False

    return _resolver_con_backtracking(tablero)


def mostrar_tablero(tablero):
    """Muestra el tablero dividido en bloques de 3x3."""

    for fila in range(9):
        if fila == 3 or fila == 6:
            print("-" * 21)

        for columna in range(9):
            valor = tablero[fila][columna]

            # Muestra un punto si el valor es 0.
            # En caso contrario, muestra el número.
            simbolo = "." if valor == 0 else str(valor)

            if columna == 2 or columna == 5:
                print(simbolo, end=" | ")
            else:
                print(simbolo, end=" ")

        print()


if __name__ == "__main__":
    tablero = [
        fila.copy()
        for fila in TABLERO_INICIAL
    ]

    print("Sudoku original:")
    mostrar_tablero(tablero)

    if resolver(tablero):
        print("\nSudoku resuelto:")
        mostrar_tablero(tablero)
    else:
        print("\nEl Sudoku no tiene solución.")
