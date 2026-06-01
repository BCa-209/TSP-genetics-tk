from __future__ import annotations

import threading
from tkinter import Button, Frame, Label, StringVar, Tk, ttk
from threading import Event

from models.city import City
from models.individual import Individual
from services.genetic_algorithm import GeneticAlgorithm
from ui.map_view import MapView


class MainWindow:
    def __init__(self, root: Tk, cities: list[City]) -> None:
        self.root = root
        self.cities = cities
        self.root.title("Optimización de Rutas TSP - Perú")
        self.root.geometry("1100x720")

        self.best_distance_var = StringVar(value="Distancia: N/A")
        self.best_fitness_var = StringVar(value="Fitness: N/A")
        self.generation_var = StringVar(value="Generación: 0")
        self.status_var = StringVar(value="Listo")

        self.selection_method_var = StringVar(value="tournament")
        self.population_size_var = StringVar(value="100")
        self.generations_var = StringVar(value="200")
        self.crossover_rate_var = StringVar(value="0.9")
        self.mutation_rate_var = StringVar(value="0.02")

        self.stop_event = Event()
        self.worker_thread: threading.Thread | None = None
        self.genetic_algorithm: GeneticAlgorithm | None = None

        self._build_ui()

    def _build_ui(self) -> None:
        control_frame = Frame(self.root, padx=10, pady=10)
        control_frame.pack(side="left", fill="y")

        Button(control_frame, text="Iniciar", command=self.start_evolution, width=20).pack(pady=6)
        Button(control_frame, text="Detener", command=self.stop_evolution, width=20).pack(pady=6)

        Label(control_frame, text="Método de selección").pack(anchor="w", pady=(16, 2))
        ttk.Combobox(
            control_frame,
            textvariable=self.selection_method_var,
            values=["tournament", "roulette"],
            state="readonly",
            width=18,
        ).pack(pady=2)

        Label(control_frame, text="Tamaño de población").pack(anchor="w", pady=(16, 2))
        self.population_entry = ttk.Entry(control_frame, textvariable=self.population_size_var, width=20)
        self.population_entry.pack(pady=2)

        Label(control_frame, text="Generaciones").pack(anchor="w", pady=(16, 2))
        self.generations_entry = ttk.Entry(control_frame, textvariable=self.generations_var, width=20)
        self.generations_entry.pack(pady=2)

        Label(control_frame, text="Tasa de cruce").pack(anchor="w", pady=(16, 2))
        self.crossover_entry = ttk.Entry(control_frame, textvariable=self.crossover_rate_var, width=20)
        self.crossover_entry.pack(pady=2)

        Label(control_frame, text="Tasa de mutación").pack(anchor="w", pady=(16, 2))
        self.mutation_entry = ttk.Entry(control_frame, textvariable=self.mutation_rate_var, width=20)
        self.mutation_entry.pack(pady=2)

        Label(control_frame, textvariable=self.generation_var, font=("Segoe UI", 11, "bold")).pack(pady=(30, 2), anchor="w")
        Label(control_frame, textvariable=self.best_distance_var, font=("Segoe UI", 11)).pack(pady=2, anchor="w")
        Label(control_frame, textvariable=self.best_fitness_var, font=("Segoe UI", 11)).pack(pady=2, anchor="w")
        Label(control_frame, textvariable=self.status_var, font=("Segoe UI", 10, "italic")).pack(pady=(20, 2), anchor="w")

        map_frame = Frame(self.root)
        map_frame.pack(side="right", fill="both", expand=True)

        self.map_view = MapView(map_frame, self.cities)
        self.map_view.pack(fill="both", expand=True)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _create_algorithm(self) -> None:
        population_size = int(self.population_size_var.get())
        generations = int(self.generations_var.get())
        crossover_rate = float(self.crossover_rate_var.get())
        mutation_rate = float(self.mutation_rate_var.get())
        selection_method = self.selection_method_var.get()

        self.genetic_algorithm = GeneticAlgorithm(
            cities=self.cities,
            population_size=population_size,
            crossover_rate=crossover_rate,
            mutation_rate=mutation_rate,
            selection_method=selection_method,
        )
        self.generation_var.set("Generación: 0")
        self.status_var.set(f"Listo para {generations} generaciones")

    def start_evolution(self) -> None:
        if self.worker_thread and self.worker_thread.is_alive():
            self.status_var.set("Evolución ya en ejecución")
            return

        try:
            self._create_algorithm()
        except ValueError as error:
            self.status_var.set(f"Error: {error}")
            return

        self.stop_event.clear()
        self.worker_thread = threading.Thread(target=self._run_evolution, daemon=True)
        self.worker_thread.start()
        self.status_var.set("Ejecución en progreso...")

    def stop_evolution(self) -> None:
        if self.worker_thread and self.worker_thread.is_alive():
            self.stop_event.set()
            self.status_var.set("Deteniendo ejecución...")

    def _run_evolution(self) -> None:
        assert self.genetic_algorithm is not None
        generations = int(self.generations_var.get())

        def callback(best_individual: Individual, generation: int) -> None:
            self.root.after(0, self._update_ui, best_individual, generation)

        self.genetic_algorithm.evolve(generations=generations, callback=callback, stop_event=self.stop_event)
        self.root.after(0, self._finalize_execution)

    def _update_ui(self, best_individual: "models.individual.Individual", generation: int) -> None:
        self.generation_var.set(f"Generación: {generation}")
        self.best_distance_var.set(f"Distancia: {best_individual.distance:.4f}")
        self.best_fitness_var.set(f"Fitness: {best_individual.fitness:.8f}")
        self.map_view.draw_route(best_individual.tour)

    def _finalize_execution(self) -> None:
        if self.stop_event.is_set():
            self.status_var.set("Ejecución detenida")
        else:
            self.status_var.set("Ejecución completada")

    def on_close(self) -> None:
        self.stop_evolution()
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=2.0)
        self.root.destroy()
