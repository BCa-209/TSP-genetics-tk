from __future__ import annotations

import random
from threading import Event
from typing import Callable, Iterable, List

from models.city import City
from models.individual import Individual
from services.distance_service import calculate_euclidean_distance

SelectionMethod = str


class GeneticAlgorithm:
    def __init__(
        self,
        cities: list[City],
        population_size: int = 100,
        crossover_rate: float = 0.9,
        mutation_rate: float = 0.02,
        tournament_size: int = 5,
        selection_method: SelectionMethod = "tournament",
        random_seed: int | None = None,
    ) -> None:
        if population_size < 2:
            raise ValueError("population_size must be at least 2")
        if not 0 <= crossover_rate <= 1:
            raise ValueError("crossover_rate must be between 0 and 1")
        if not 0 <= mutation_rate <= 1:
            raise ValueError("mutation_rate must be between 0 and 1")

        self.cities = cities.copy()
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.tournament_size = max(2, tournament_size)
        self.selection_method = selection_method
        self.random = random.Random(random_seed)

        self.population: list[Individual] = []
        self.best_individual: Individual | None = None
        self.generation: int = 0
        self._initialize_population()

    def _initialize_population(self) -> None:
        self.population = []
        for _ in range(self.population_size):
            tour = self.cities.copy()
            self.random.shuffle(tour)
            individual = Individual(tour)
            individual.evaluate(calculate_euclidean_distance)
            self.population.append(individual)
        self._update_best()

    def _update_best(self) -> None:
        self.best_individual = min(self.population, key=lambda individual: individual.distance)

    def _select_parent(self) -> Individual:
        if self.selection_method == "roulette":
            return self._roulette_selection()
        return self._tournament_selection()

    def _roulette_selection(self) -> Individual:
        total_fitness = sum(individual.fitness for individual in self.population)
        if total_fitness <= 0:
            return self.random.choice(self.population).copy()

        target = self.random.random() * total_fitness
        running = 0.0
        for individual in self.population:
            running += individual.fitness
            if running >= target:
                return individual.copy()
        return self.population[-1].copy()

    def _tournament_selection(self) -> Individual:
        participants = self.random.sample(self.population, min(self.tournament_size, len(self.population)))
        winner = max(participants, key=lambda individual: individual.fitness)
        return winner.copy()

    def _ordered_crossover(self, parent_a: Individual, parent_b: Individual) -> Individual:
        tour_size = len(parent_a.tour)
        if tour_size < 2:
            return parent_a.copy()

        start = self.random.randrange(tour_size)
        end = self.random.randrange(start + 1, tour_size + 1)

        child_tour: list[City | None] = [None] * tour_size
        child_tour[start:end] = parent_a.tour[start:end]

        insert_position = end % tour_size
        for city in parent_b.tour:
            if city in child_tour:
                continue
            child_tour[insert_position] = city
            insert_position = (insert_position + 1) % tour_size

        return Individual([city for city in child_tour if city is not None])

    def _mutate_swap(self, individual: Individual) -> None:
        tour = individual.tour
        if len(tour) < 2:
            return
        index_a, index_b = self.random.sample(range(len(tour)), 2)
        tour[index_a], tour[index_b] = tour[index_b], tour[index_a]

    def _create_next_generation(self) -> None:
        next_population: list[Individual] = []
        elite = min(self.population, key=lambda individual: individual.distance).copy()
        next_population.append(elite)

        while len(next_population) < self.population_size:
            parent_a = self._select_parent()
            parent_b = self._select_parent()

            if self.random.random() < self.crossover_rate:
                child = self._ordered_crossover(parent_a, parent_b)
            else:
                child = parent_a.copy()

            if self.random.random() < self.mutation_rate:
                self._mutate_swap(child)

            child.evaluate(calculate_euclidean_distance)
            next_population.append(child)

        self.population = next_population

    def run_generation(self) -> Individual:
        self._create_next_generation()
        self.generation += 1
        self._update_best()
        assert self.best_individual is not None
        return self.best_individual.copy()

    def evolve(
        self,
        generations: int,
        callback: Callable[[Individual, int], None] | None = None,
        stop_event: Event | None = None,
    ) -> None:
        for generation in range(1, generations + 1):
            if stop_event is not None and stop_event.is_set():
                break
            best = self.run_generation()
            if callback is not None:
                callback(best, generation)
