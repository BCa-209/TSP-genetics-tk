from __future__ import annotations

from typing import Iterable

from models.city import City


class MapService:
    def __init__(self, map_widget: "MapWidget") -> None:  # type: ignore[name-defined]
        self.map_widget = map_widget
        self.route_lines: list[object] = []
        self.city_markers: list[object] = []

    def set_center(self, latitude: float, longitude: float, zoom: int = 6) -> None:
        self.map_widget.set_position(latitude, longitude)
        self.map_widget.set_zoom(zoom)

    def add_markers(self, cities: Iterable[City]) -> None:
        for city in cities:
            marker = self.map_widget.set_marker(city.lat, city.lon, text=city.nombre)
            self.city_markers.append(marker)

    def clear_route(self) -> None:
        while self.route_lines:
            line = self.route_lines.pop()
            if hasattr(line, "delete"):
                try:
                    line.delete()
                except Exception:
                    pass
            elif hasattr(self.map_widget, "delete"):
                try:
                    self.map_widget.delete(line)
                except Exception:
                    pass

    def draw_route(self, route: Iterable[City], color: str = "red", width: int = 4) -> None:
        self.clear_route()
        path = [(city.lat, city.lon) for city in route]
        if not path:
            return
        line = self.map_widget.set_path(path, color=color, width=width)
        self.route_lines.append(line)
