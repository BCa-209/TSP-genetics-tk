import unittest

from models.city import City
from services.genetic_algorithm import GeneticAlgorithm
from services.distance_service import calculate_euclidean_distance


class GeneticAlgorithmTest(unittest.TestCase):
    def setUp(self) -> None:
        self.cities = [
            City(nombre="A", lat=0.0, lon=0.0),
            City(nombre="B", lat=0.0, lon=1.0),
            City(nombre="C", lat=1.0, lon=1.0),
            City(nombre="D", lat=1.0, lon=0.0),
        ]

    def test_initial_population(self) -> None:
        ga = GeneticAlgorithm(self.cities, population_size=10, random_seed=42)
        self.assertEqual(len(ga.population), 10)
        for individual in ga.population:
            self.assertEqual(len(individual.tour), len(self.cities))
            self.assertGreater(individual.distance, 0.0)
            self.assertGreater(individual.fitness, 0.0)

    def test_selection_methods(self) -> None:
        ga_tournament = GeneticAlgorithm(self.cities, population_size=10, selection_method="tournament", random_seed=42)
        parent = ga_tournament._select_parent()
        self.assertEqual(len(parent.tour), len(self.cities))

        ga_roulette = GeneticAlgorithm(self.cities, population_size=10, selection_method="roulette", random_seed=42)
        parent = ga_roulette._select_parent()
        self.assertEqual(len(parent.tour), len(self.cities))

    def test_ordered_crossover_preserves_cities(self) -> None:
        ga = GeneticAlgorithm(self.cities, population_size=10, random_seed=42)
        parent_a = ga.population[0]
        parent_b = ga.population[1]
        child = ga._ordered_crossover(parent_a, parent_b)
        self.assertCountEqual(child.tour, self.cities)

    def test_mutation_swaps_two_cities(self) -> None:
        ga = GeneticAlgorithm(self.cities, population_size=10, random_seed=42)
        individual = ga.population[0].copy()
        original_tour = individual.tour.copy()
        ga._mutate_swap(individual)
        self.assertEqual(set(individual.tour), set(original_tour))
        self.assertEqual(len(individual.tour), len(original_tour))

    def test_run_generation_improves_or_maintains_best(self) -> None:
        ga = GeneticAlgorithm(self.cities, population_size=10, random_seed=42)
        initial_best = ga.best_individual.distance
        best = ga.run_generation()
        self.assertLessEqual(best.distance, initial_best)
        self.assertGreater(best.fitness, 0.0)

    def test_evolve_callback(self) -> None:
        ga = GeneticAlgorithm(self.cities, population_size=10, random_seed=42)
        captured = []

        def callback(best, generation):
            captured.append((generation, best.distance))

        ga.evolve(3, callback=callback)
        self.assertEqual(len(captured), 3)
        self.assertEqual(captured[0][0], 1)
        self.assertEqual(captured[-1][0], 3)


if __name__ == "__main__":
    unittest.main()
