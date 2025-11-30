# src/main.py
import asyncio
from config import Settings
from data_loader import load_dataset
from weather_service import WeatherService
from report import build_report, write_report

async def main():
    settings = Settings.from_env()

    tickets, airports = load_dataset(settings.dataset_path)

    weather_service = WeatherService(
        api_key=settings.weather_api_key,
        concurrency_limit=settings.concurrency_limit,
        cache_path=settings.cache_path,
    )

    # Aeropuertos únicos
    unique_airports = {t.origin for t in tickets} | {t.destination for t in tickets}

    # Pre-carga el clima (asíncrono, limitado en concurrencia)
    await weather_service.preload_airports_weather(unique_airports, airports)

    # Construye el reporte
    rows = build_report(tickets, airports, weather_service)

    # Escribe CSV (o lo que quieras)
    write_report(rows, settings.output_path)

if __name__ == "__main__":
    asyncio.run(main())
