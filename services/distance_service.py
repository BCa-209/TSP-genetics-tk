from __future__ import annotations

import math
from typing import Iterable

from models.city import City


def calculate_euclidean_distance(city_a: City, city_b: City) -> float:
    x1, y1 = city_a.lon, city_a.lat
    x2, y2 = city_b.lon, city_b.lat
    return math.hypot(x2 - x1, y2 - y1)


def calculate_route_distance(route: Iterable[City]) -> float:
    route_list = list(route)
    if len(route_list) < 2:
        return 0.0

    total_distance = 0.0
    for index in range(len(route_list)):
        current_city = route_list[index]
        next_city = route_list[(index + 1) % len(route_list)]
        total_distance += calculate_euclidean_distance(current_city, next_city)
    return total_distance
