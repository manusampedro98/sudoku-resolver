# Resolutor de Sudoku

Aplicación desarrollada en Python que permite introducir y resolver sudokus mediante el algoritmo de **backtracking**.

El objetivo del proyecto ha sido aprender a dividir un problema en funciones pequeñas, aplicar recursividad, validar los datos de entrada, escribir pruebas automáticas y separar la lógica de la interfaz gráfica.

## Funcionalidades

- Tablero interactivo de 9 × 9.
- Introducción y eliminación de números con el teclado.
- Protección de las casillas iniciales.
- Detección visual de conflictos en filas, columnas y bloques de 3 × 3.
- Resolución automática mediante backtracking.
- Validación del tablero antes de intentar resolverlo.
- Botones para resolver, reiniciar y limpiar el tablero.
- Mensajes de estado para informar al usuario.
- Pruebas automáticas de la lógica del resolutor.
- Notebook explicativo del algoritmo.

## Cómo funciona el algoritmo

Las casillas vacías se representan mediante el número `0`. El resolutor busca la primera casilla vacía y prueba los números del `1` al `9`.

Antes de colocar un número comprueba que no esté repetido en:

- La misma fila.
- La misma columna.
- El mismo bloque de 3 × 3.

Cuando encuentra un número válido, lo coloca y continúa con la siguiente casilla vacía. Si más adelante llega a una posición sin opciones válidas, borra la última elección y prueba otra posibilidad. Este proceso se conoce como **backtracking**.

## Estructura del proyecto

```text
Sudoku_Resolver/
├── app.py
├── environment-conda.yml
├── notebooks/
│   └── 01_explicacion_backtracking.ipynb
├── src/
│   ├── __init__.py
│   └── solver.py
├── tests/
│   └── test_solver.py
├── requirements.txt
└── requirements-dev.txt
```

- `src/solver.py`: contiene la validación y el algoritmo de resolución.
- `app.py`: contiene la interfaz gráfica creada con Pygame.
- `tests/test_solver.py`: comprueba el comportamiento de la lógica.
- `notebooks/01_explicacion_backtracking.ipynb`: explica el algoritmo paso a paso utilizando las funciones reales del proyecto.

## Instalación con Conda

Desde la carpeta del proyecto:

```bash
conda env create -f environment-conda.yml
conda activate sudoku-resolver
```

Si el entorno ya está creado, puede actualizarse con:

```bash
conda env update -f environment-conda.yml --prune
```

## Ejecutar la aplicación

```bash
python app.py
```

### Controles

1. Selecciona una casilla con el ratón.
2. Pulsa un número del `1` al `9` para introducirlo.
3. Utiliza `0`, `Retroceso` o `Suprimir` para borrar una casilla editable.
4. Pulsa **Resolver** para completar el Sudoku.
5. Pulsa **Reiniciar** para recuperar el tablero de ejemplo.
6. Pulsa **Limpiar** para crear un tablero vacío.

## Ejecutar las pruebas

```bash
python -m pytest
```

## Comprobar el estilo del código

```bash
python -m ruff check .
```

## Tecnologías utilizadas

- Python 3.12
- Pygame CE
- Pytest
- Ruff
- Jupyter e IPykernel
- Conda
