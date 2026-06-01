from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from models.city import City

DistanceFunction = Callable[[City, City], float]

@dataclass
class Individual:
    tour: list[City]
    distance: float = field(default=0.0)
    fitness: float = field(default=0.0)

    def evaluate(self, distance_function: DistanceFunction) -> None:
        self.distance = 0.0
        for index in range(len(self.tour)):
            current_city = self.tour[index]
            next_city = self.tour[(index + 1) % len(self.tour)]
            self.distance += distance_function(current_city, next_city)
        self.fitness = 1.0 / self.distance if self.distance > 0 else 0.0

    def copy(self) -> Individual:
        return Individual(self.tour.copy(), self.distance, self.fitness)
