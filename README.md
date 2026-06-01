# Sistema de Optimización de Rutas (TSP con Algoritmo Genético)

Aplicación Python que resuelve el Problema del Viajante de Comercio (TSP) para las 25 capitales regionales del Perú usando un algoritmo genético y visualiza la evolución de la ruta en tiempo real con Tkinter y OpenStreetMap.

## Características

- Generación de población inicial de rutas aleatorias.
- Evaluación de fitness basada únicamente en distancia euclidiana.
- Selección configurable por torneo o ruleta.
- Cruce ordenado (OX) y mutación por intercambio de ciudades.
- Visualización de marcadores y rutas en un mapa de OpenStreetMap.
- Actualización dinámica de la mejor ruta sin congelar la interfaz.

## Requisitos

- Python 3.10+
- `tkintermapview`
- `numpy`
- `Pillow`

## Instalación

1. Crear un entorno virtual:

```bash
python -m venv .venv
```

2. Activar el entorno:

```powershell
.venv\Scripts\Activate.ps1
```

3. Instalar dependencias:

```bash
python -m pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

## Uso

1. Elige el método de selección (`tournament` o `roulette`).
2. Ajusta tamaño de población, generaciones, tasa de cruce y tasa de mutación.
3. Presiona `Iniciar`.
4. La ventana mostrará la ruta mejor de cada generación en el mapa.

## Pruebas

```bash
python -m unittest discover -s tests
```

## Estructura del proyecto

```
TSP genetics tk/
├── data/
│   └── peru_capitals.json
├── models/
│   ├── city.py
│   └── individual.py
├── services/
│   ├── distance_service.py
│   ├── genetic_algorithm.py
│   └── map_service.py
├── ui/
│   ├── main_window.py
│   └── map_view.py
├── tests/
│   ├── test_distance_service.py
│   └── test_genetic_algorithm.py
├── main.py
├── README.md
└── requirements.txt
```
