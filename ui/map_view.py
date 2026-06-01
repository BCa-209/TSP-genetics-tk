from __future__ import annotations

from tkinter import Frame
from tkintermapview import TkinterMapView

from models.city import City
from services.map_service import MapService


class MapView(Frame):
    def __init__(self, master: Frame, cities: list[City]) -> None:
        super().__init__(master)
        self.map_widget = TkinterMapView(self, width=800, height=600, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True)
        self.service = MapService(self.map_widget)
        self.cities = cities
        self._configure_map()

    def _configure_map(self) -> None:
        peru_center = (-10.0, -76.5)
        self.service.set_center(*peru_center, zoom=6)
        self.service.add_markers(self.cities)

    def draw_route(self, route: list[City]) -> None:
        self.service.draw_route(route)
