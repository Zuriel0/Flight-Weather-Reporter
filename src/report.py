# src/report.py
from typing import List, Dict
from models import Ticket, Airport, Weather
from weather_service import WeatherService
import csv

def build_report(tickets: List[Ticket], airports: Dict[str, Airport], weather_service: WeatherService):
    rows = []
    for t in tickets:
        origin_airport = airports.get(t.origin)
        dest_airport = airports.get(t.destination)

        # En la arquitectura propuesta, el weather ya se precargó en preload_airports_weather
        origin_weather: Weather = weather_service._in_memory.get(
            weather_service._cache_key(origin_airport)
        ) if origin_airport else None

        dest_weather: Weather = weather_service._in_memory.get(
            weather_service._cache_key(dest_airport)
        ) if dest_airport else None

        rows.append({
            "origin": t.origin,
            "destination": t.destination,
            "airline": t.airline,
            "flight_num": t.flight_num,
            "origin_temp": getattr(origin_weather, "temperature", None),
            "origin_desc": getattr(origin_weather, "description", None),
            "dest_temp": getattr(dest_weather, "temperature", None),
            "dest_desc": getattr(dest_weather, "description", None),
        })
    return rows

def write_report(rows, path: str):
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
