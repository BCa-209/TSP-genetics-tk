import unittest

from models.city import City
from services.distance_service import calculate_euclidean_distance, calculate_route_distance


class DistanceServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.city_a = City(nombre="A", lat=-10.0, lon=-76.0)
        self.city_b = City(nombre="B", lat=-10.5, lon=-76.5)
        self.city_c = City(nombre="C", lat=-11.0, lon=-77.0)

    def test_euclidean_distance(self) -> None:
        distance = calculate_euclidean_distance(self.city_a, self.city_b)
        expected = ((-76.5 + 76.0) ** 2 + (-10.5 + 10.0) ** 2) ** 0.5
        self.assertAlmostEqual(distance, expected, places=8)

    def test_route_distance_closed_loop(self) -> None:
        route = [self.city_a, self.city_b, self.city_c]
        distance = calculate_route_distance(route)
        expected = (
            calculate_euclidean_distance(self.city_a, self.city_b)
            + calculate_euclidean_distance(self.city_b, self.city_c)
            + calculate_euclidean_distance(self.city_c, self.city_a)
        )
        self.assertAlmostEqual(distance, expected, places=8)

    def test_empty_route_distance(self) -> None:
        self.assertEqual(calculate_route_distance([]), 0.0)


if __name__ == "__main__":
    unittest.main()
