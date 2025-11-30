# src/config.py
import os
from dataclasses import dataclass

@dataclass
class Settings:
    dataset_path: str
    weather_api_key: str
    concurrency_limit: int = 10
    cache_path: str = "data/weather_cache.json"
    output_path: str = "data/report.csv"

    @classmethod
    def from_env(cls):
        weather_api_key = os.getenv("WEATHER_API_KEY")
        if not weather_api_key:
            raise RuntimeError(
                "Falta la variable de entorno WEATHER_API_KEY. "
                "Defínela con tu API key de WeatherAPI.com antes de correr el programa."
            )

        return cls(
            dataset_path=os.getenv("DATASET_PATH", "data/challenge_dataset.csv"),
            weather_api_key=weather_api_key,
            concurrency_limit=int(os.getenv("CONCURRENCY_LIMIT", "10")),
            cache_path=os.getenv("CACHE_PATH", "data/weather_cache.json"),
            output_path=os.getenv("OUTPUT_PATH", "data/report.csv"),
        )
