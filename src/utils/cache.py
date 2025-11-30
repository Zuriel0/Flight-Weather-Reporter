# src/utils/cache.py
import json
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import date
from models import Weather

class DiskCache:
    def __init__(self, path: str):
        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._data: Dict[str, Any] = {}
        if self._path.exists():
            try:
                self._data = json.loads(self._path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                self._data = {}

    def get(self, key: str) -> Optional[Weather]:
        raw = self._data.get(key)
        if not raw:
            return None
        return Weather(
            date=date.fromisoformat(raw["date"]),
            temperature=raw["temperature"],
            description=raw["description"],
            raw=raw["raw"],
        )

    def set(self, key: str, weather: Weather) -> None:
        self._data[key] = {
            "date": weather.date.isoformat(),
            "temperature": weather.temperature,
            "description": weather.description,
            "raw": weather.raw,
        }
        self._path.write_text(json.dumps(self._data), encoding="utf-8")
