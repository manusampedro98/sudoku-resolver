import pygame

from src.solver import (
    TABLERO_INICIAL,
    casilla_tiene_conflicto,
    resolver,
)

# Configuración general de la ventana.
ANCHO = 900
ALTO = 700
FPS = 60

# Colores utilizados en la interfaz.
COLOR_FONDO = (15, 23, 42)
COLOR_TABLERO = (30, 41, 59)
COLOR_LINEA = (100, 116, 139)
COLOR_SELECCION = (51, 90, 140)
COLOR_NUMERO_INICIAL = (226, 232, 240)
COLOR_NUMERO_USUARIO = (96, 165, 250)
COLOR_ERROR = (248, 113, 113)
COLOR_MENSAJE = (148, 163, 184)
COLOR_EXITO = (74, 222, 128)
COLOR_BOTON_PRINCIPAL = (59, 130, 246)
COLOR_BOTON_SECUNDARIO = (51, 65, 85)
COLOR_TEXTO_BOTON = (248, 250, 252)

# El tablero mide 540 píxeles, por lo que cada casilla mide 60.
TAMANO_TABLERO = 540
TAMANO_CASILLA = TAMANO_TABLERO // 9

# Coordenadas desde las que empieza a dibujarse el tablero.
ORIGEN_X = (ANCHO - TAMANO_TABLERO) // 2
ORIGEN_Y = 80

# Posición y tamaño de los tres botones.
BOTON_RESOLVER = pygame.Rect(180, 640, 170, 44)
BOTON_REINICIAR = pygame.Rect(365, 640, 170, 44)
BOTON_LIMPIAR = pygame.Rect(550, 640, 170, 44)


def dibujar_boton(
    ventana,
    rectangulo,
    texto,
    fuente,
    color,
):
    """Dibuja un botón con el texto centrado."""

    pygame.draw.rect(
        ventana,
        color,
        rectangulo,
        border_radius=8,
    )

    texto_renderizado = fuente.render(
        texto,
        True,
        COLOR_TEXTO_BOTON,
    )
    rectangulo_texto = texto_renderizado.get_rect(
        center=rectangulo.center
    )

    ventana.blit(
        texto_renderizado,
        rectangulo_texto,
    )


def dibujar_mensaje(
    ventana,
    mensaje,
    fuente,
    color,
):
    """Muestra un mensaje centrado sobre el tablero."""

    texto = fuente.render(
        mensaje,
        True,
        color,
    )
    rectangulo = texto.get_rect(
        center=(ANCHO // 2, 40)
    )

    ventana.blit(texto, rectangulo)


def dibujar_tablero(
    ventana,
    tablero,
    tablero_inicial,
    fuente,
    casilla_seleccionada,
):
    """Dibuja el fondo y las líneas del tablero."""

    # Dibujamos primero el fondo completo del tablero.
    pygame.draw.rect(
        ventana,
        COLOR_TABLERO,
        (
            ORIGEN_X,
            ORIGEN_Y,
            TAMANO_TABLERO,
            TAMANO_TABLERO,
        ),
    )

    # La casilla seleccionada se muestra con un color diferente.
    if casilla_seleccionada is not None:
        fila, columna = casilla_seleccionada

        pygame.draw.rect(
            ventana,
            COLOR_SELECCION,
            (
                ORIGEN_X + columna * TAMANO_CASILLA,
                ORIGEN_Y + fila * TAMANO_CASILLA,
                TAMANO_CASILLA,
                TAMANO_CASILLA,
            ),
        )

    # Se necesitan diez líneas para separar las nueve filas y columnas.
    for indice in range(10):
        desplazamiento = indice * TAMANO_CASILLA

        # Las líneas que separan los bloques de 3x3 son más gruesas.
        if indice % 3 == 0:
            grosor = 4
        else:
            grosor = 1

        pygame.draw.line(
            ventana,
            COLOR_LINEA,
            (ORIGEN_X + desplazamiento, ORIGEN_Y),
            (
                ORIGEN_X + desplazamiento,
                ORIGEN_Y + TAMANO_TABLERO,
            ),
            grosor,
        )

        pygame.draw.line(
            ventana,
            COLOR_LINEA,
            (ORIGEN_X, ORIGEN_Y + desplazamiento),
            (
                ORIGEN_X + TAMANO_TABLERO,
                ORIGEN_Y + desplazamiento,
            ),
            grosor,
        )
    # Finalmente recorremos las casillas para dibujar sus números.
    for fila in range(9):
        for columna in range(9):
            valor = tablero[fila][columna]

            if valor == 0:
                continue

            # Cada tipo de número utiliza un color diferente.
            if casilla_tiene_conflicto(
                tablero,
                fila,
                columna,
            ):
                color_numero = COLOR_ERROR

            elif tablero_inicial[fila][columna] != 0:
                color_numero = COLOR_NUMERO_INICIAL

            else:
                color_numero = COLOR_NUMERO_USUARIO

            texto = fuente.render(
                str(valor),
                True,
                color_numero,
            )

            centro_x = (
                ORIGEN_X
                + columna * TAMANO_CASILLA
                + TAMANO_CASILLA // 2
            )
            centro_y = (
                ORIGEN_Y
                + fila * TAMANO_CASILLA
                + TAMANO_CASILLA // 2
            )

            rectangulo_texto = texto.get_rect(
                center=(centro_x, centro_y)
            )
            ventana.blit(texto, rectangulo_texto)


def copiar_tablero(tablero):
    """Crea una copia independiente de un tablero."""

    return [fila.copy() for fila in tablero]


def crear_tablero_vacio():
    """Crea un tablero 9x9 sin números."""

    return [[0] * 9 for _ in range(9)]


def ejecutar():
    """Inicia y mantiene abierta la aplicación."""

    pygame.init()

    fuente = pygame.font.SysFont(
        "segoeui",
        32,
        bold=True,
    )
    fuente_boton = pygame.font.SysFont(
        "segoeui",
        18,
        bold=True,
    )
    fuente_mensaje = pygame.font.SysFont(
        "segoeui",
        17,
    )

    # Guardamos por separado las pistas iniciales y el tablero editable.
    tablero_inicial = copiar_tablero(TABLERO_INICIAL)
    tablero_actual = copiar_tablero(tablero_inicial)

    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Resolutor de Sudoku")

    reloj = pygame.time.Clock()
    ejecutando = True
    casilla_seleccionada = None
    mensaje_estado = "Selecciona una casilla y escribe un número."
    color_estado = COLOR_MENSAJE

    while ejecutando:
        # Pygame guarda los clics y las pulsaciones en una cola de eventos.
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                raton_x, raton_y = evento.pos

                # Comprobamos primero si el usuario ha pulsado un botón.
                if BOTON_RESOLVER.collidepoint(evento.pos):
                    if resolver(tablero_actual):
                        casilla_seleccionada = None
                        mensaje_estado = "Sudoku resuelto correctamente."
                        color_estado = COLOR_EXITO
                    else:
                        mensaje_estado = (
                            "El tablero contiene errores o no tiene solución."
                        )
                        color_estado = COLOR_ERROR

                elif BOTON_REINICIAR.collidepoint(evento.pos):
                    tablero_inicial = copiar_tablero(TABLERO_INICIAL)
                    tablero_actual = copiar_tablero(tablero_inicial)
                    casilla_seleccionada = None
                    mensaje_estado = "Sudoku reiniciado."
                    color_estado = COLOR_MENSAJE

                elif BOTON_LIMPIAR.collidepoint(evento.pos):
                    tablero_inicial = crear_tablero_vacio()
                    tablero_actual = crear_tablero_vacio()
                    casilla_seleccionada = None
                    mensaje_estado = "Tablero vacío: introduce un Sudoku."
                    color_estado = COLOR_MENSAJE

                else:
                    # Si no pulsó un botón, comprobamos si pulsó el tablero.
                    dentro_horizontal = (
                        ORIGEN_X
                        <= raton_x
                        < ORIGEN_X + TAMANO_TABLERO
                    )
                    dentro_vertical = (
                        ORIGEN_Y
                        <= raton_y
                        < ORIGEN_Y + TAMANO_TABLERO
                    )

                    if dentro_horizontal and dentro_vertical:
                        # Convertimos los píxeles del clic en fila y columna.
                        columna = (
                            raton_x - ORIGEN_X
                        ) // TAMANO_CASILLA
                        fila = (
                            raton_y - ORIGEN_Y
                        ) // TAMANO_CASILLA

                        casilla_seleccionada = (
                            fila,
                            columna,
                        )

            elif (
                evento.type == pygame.KEYDOWN
                and casilla_seleccionada is not None
            ):
                fila, columna = casilla_seleccionada

                # Las pistas del Sudoku original no se pueden modificar.
                casilla_editable = (
                    tablero_inicial[fila][columna] == 0
                )

                if casilla_editable:
                    # Las teclas del 1 al 9 introducen un número.
                    if pygame.K_1 <= evento.key <= pygame.K_9:
                        numero = evento.key - pygame.K_0
                        tablero_actual[fila][columna] = numero

                        if casilla_tiene_conflicto(
                            tablero_actual,
                            fila,
                            columna,
                        ):
                            mensaje_estado = (
                                "Ese número genera un conflicto."
                            )
                            color_estado = COLOR_ERROR
                        else:
                            mensaje_estado = "Número añadido."
                            color_estado = COLOR_MENSAJE

                    # El 0, Retroceso y Suprimir vacían la casilla.
                    elif evento.key in (
                        pygame.K_0,
                        pygame.K_BACKSPACE,
                        pygame.K_DELETE,
                    ):
                        tablero_actual[fila][columna] = 0
                        mensaje_estado = "Casilla borrada."
                        color_estado = COLOR_MENSAJE

        # En cada vuelta se vuelve a dibujar la ventana completa.
        ventana.fill(COLOR_FONDO)
        dibujar_mensaje(
            ventana,
            mensaje_estado,
            fuente_mensaje,
            color_estado,
        )
        dibujar_tablero(
            ventana,
            tablero_actual,
            tablero_inicial,
            fuente,
            casilla_seleccionada,
        )
        dibujar_boton(
            ventana,
            BOTON_RESOLVER,
            "Resolver",
            fuente_boton,
            COLOR_BOTON_PRINCIPAL,
        )
        dibujar_boton(
            ventana,
            BOTON_REINICIAR,
            "Reiniciar",
            fuente_boton,
            COLOR_BOTON_SECUNDARIO,
        )
        dibujar_boton(
            ventana,
            BOTON_LIMPIAR,
            "Limpiar",
            fuente_boton,
            COLOR_BOTON_SECUNDARIO,
        )

        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    ejecutar()
