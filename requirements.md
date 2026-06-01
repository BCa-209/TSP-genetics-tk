# Sistema de Optimización de Rutas (TSP con Algoritmo Genético)

## 1. Descripción General

El sistema tiene como objetivo resolver el problema del viajante de comercio (TSP) utilizando un algoritmo genético, optimizando rutas entre las 25 capitales regionales del Perú.

La aplicación contará con una interfaz gráfica desarrollada en Tkinter, integrando un mapa basado en OpenStreetMap para la visualización de las ciudades y las rutas generadas.

---

## 2. Alcance

El sistema permitirá:

- Resolver el TSP mediante algoritmo genético.
- Optimizar rutas entre capitales regionales del Perú.
- Visualizar las ciudades en un mapa interactivo.
- Representar rutas en tiempo real sobre el mapa.
- Calcular distancias entre ciudades mediante distancia euclidiana.

El sistema deberá:

- Representar geográficamente las ciudades utilizando OpenStreetMap dentro de una interfaz Tkinter.
- Mostrar el territorio del Perú mediante teselas (tiles) de OpenStreetMap embebidas en la aplicación.
- Dibujar las rutas del TSP sobre el mapa interactivo.

---

## 3. Requisitos Funcionales

### RF-01: Generación de población inicial

El sistema deberá generar una población inicial de rutas aleatorias entre las 25 capitales regionales del Perú.

---

### RF-02: Visualización geográfica mediante OpenStreetMap y Tkinter

El sistema deberá mostrar:

- Mapa base de OpenStreetMap centrado en Perú dentro de una ventana Tkinter.
- Ubicación de cada capital regional.
- Etiqueta con nombre de ciudad.
- Zoom y desplazamiento básico.
- Ruta actual generada por el algoritmo genético.
- Mejor ruta encontrada.

La visualización deberá actualizarse en tiempo real durante la evolución del algoritmo.

Tecnología utilizada:

- Tkinter
- tkintermapview
- OpenStreetMap

---

### RF-03: Operadores genéticos

El sistema deberá implementar:

- Selección de individuos (ruleta o torneo).
- Cruce (crossover) tipo ordenado (OX).
- Mutación por intercambio de ciudades.

---

### RF-04: Evaluación de aptitud

La aptitud se calculará mediante:

Fitness = 1 / DistanciaTotal

Donde:

DistanciaTotal =
Σ distancia(ciudad_i, ciudad_i+1)

La distancia entre ciudades se calculará exclusivamente mediante distancia euclidiana:

d = √((x2 - x1)² + (y2 - y1)²)

Uso de coordenadas:

- longitud -> x
- latitud -> y

Restricciones:

- No se utilizará la fórmula de Haversine.
- No se utilizarán distancias geodésicas.
- Todas las evaluaciones deben usar distancia euclidiana.

---

### RF-05: Visualización de evolución

El sistema deberá mostrar en tiempo real:

- Mejor individuo de cada generación.
- Evolución del fitness.
- Ruta actual en el mapa.

---

## 4. Requisitos No Funcionales

- Interfaz gráfica en Tkinter.
- Actualización fluida del mapa sin congelar la UI.
- Código modular y mantenible.
- Ejecución en Python 3.10+.

---

## 5. Datos del Problema

El sistema utilizará las 25 capitales regionales del Perú con sus coordenadas geográficas:

- Nombre de la ciudad
- Latitud
- Longitud

Ejemplo:
```json
{
  "nombre": "Cusco",
  "lat": -13.53195,
  "lon": -71.967462
}
```
---

## 6. Visualización del Mapa con OpenStreetMap en Tkinter

### Motor de visualización

El sistema integrará un mapa interactivo embebido en Tkinter utilizando:

- Tkinter
- tkintermapview
- OpenStreetMap tiles

---

### Componentes de interfaz
```text
Tkinter.Tk
 └── tkintermapview.MapWidget
```
---

### Funcionalidades del mapa

El mapa deberá permitir:

- Zoom interactivo.
- Desplazamiento libre (pan).
- Visualización de 25 capitales regionales.
- Mostrar nombres de ciudades.
- Dibujar rutas entre ciudades.
- Actualización dinámica de la mejor solución.

---

### Marcadores

Cada ciudad se mostrará como:

- Marcador en el mapa
- Etiqueta con nombre

---

### Ruta actual

La mejor ruta se mostrará como:

- Línea roja
- Grosor visual destacado

---

### Actualización dinámica

En cada generación:

1. Se elimina la ruta anterior.
2. Se dibuja la nueva mejor ruta.
3. Se mantienen los marcadores.
4. Se actualizan métricas en pantalla.

---

### Conversión de coordenadas

No se requiere transformación manual:

latitud, longitud

son usados directamente por el mapa basado en OpenStreetMap.

---

## 7. Arquitectura del Proyecto
```text
project/

├── main.py
├── ui/
│   ├── main_window.py
│   ├── map_view.py
│
├── services/
│   ├── genetic_algorithm.py
│   ├── map_service.py
│   ├── distance_service.py
│
├── data/
│   ├── peru_capitals.json
│
├── models/
│   ├── city.py
│   ├── individual.py
```
---

## 8. Dependencias
```text
tkintermapview
Pillow (opcional)
numpy
```
---

## 9. Criterios de Aceptación

1. Mostrar OpenStreetMap dentro de Tkinter.
2. Mostrar las 25 capitales regionales del Perú.
3. Dibujar rutas del algoritmo genético en el mapa.
4. Usar únicamente distancia euclidiana.
5. Actualizar la mejor ruta en tiempo real.
6. La interfaz no debe congelarse durante la ejecución.