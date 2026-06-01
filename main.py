from __future__ import annotations

import json
from pathlib import Path
from tkinter import Tk

from models.city import City
from ui.main_window import MainWindow


def load_cities(data_path: Path) -> list[City]:
    with data_path.open("r", encoding="utf-8") as file:
        raw_data = json.load(file)
    return [City(nombre=item["nombre"], lat=float(item["lat"]), lon=float(item["lon"])) for item in raw_data]


def main() -> None:
    project_root = Path(__file__).resolve().parent
    data_file = project_root / "data" / "peru_capitals.json"
    cities = load_cities(data_file)

    root = Tk()
    MainWindow(root, cities)
    root.mainloop()


if __name__ == "__main__":
    main()
