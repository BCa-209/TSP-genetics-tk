from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class City:
    nombre: str
    lat: float
    lon: float

    def coordinates(self) -> tuple[float, float]:
        return self.lat, self.lon

    def position(self) -> tuple[float, float]:
        return self.lat, self.lon
