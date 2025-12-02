# src/weather_service.py
import asyncio
from datetime import date
from typing import Dict, Iterable, Set, Optional

import aiohttp

from models import Airport, Weather
from weather_client import WeatherClient, WeatherApiError
from utils.cache import DiskCache

class WeatherService:
    def __init__(self, api_key: str, concurrency_limit: int, cache_path: str):
        self._client = WeatherClient(api_key)
        self._semaphore = asyncio.Semaphore(concurrency_limit)
        self._cache = DiskCache(cache_path)
        self._in_memory: Dict[str, Weather] = {}

    def _cache_key(self, airport: Airport) -> str:
        """Cache por aeropuerto y fecha de hoy."""
        return f"{airport.iata_code}:{date.today().isoformat()}"

    def _from_weatherapi_response(self, data: Dict) -> Weather:

        current = data.get("current", {})
        temp_c = current.get("temp_c")
        condition = current.get("condition", {}) or {}
        text = condition.get("text")

        return Weather(
            date=date.today(),  # podrías parsear location.localtime si quisieras
            temperature=temp_c,
            description=text,
            raw=data,
        )

    async def _fetch_and_cache(
        self,
        airport: Airport,
        session: aiohttp.ClientSession,
    ) -> Optional[Weather]:

        key = self._cache_key(airport)

        # 1) caché en memoria
        if key in self._in_memory:
            return self._in_memory[key]

        # 2) caché en disco
        cached = self._cache.get(key)
        if cached:
            self._in_memory[key] = cached
            return cached

        # 3) llamada real con semaphore
        try:
            async with self._semaphore:
                data = await self._client.fetch_current_by_latlon(
                    session,
                    lat=airport.latitude,
                    lon=airport.longitude,
                )
        except WeatherApiError as e:
            # aquí podrías loggear el error
            print(f"[WeatherService] Error API para {airport.iata_code}: {e}")
            return None
        except asyncio.TimeoutError:
            print(f"[WeatherService] Timeout consultando {airport.iata_code}")
            return None

        weather = self._from_weatherapi_response(data)

        self._in_memory[key] = weather
        self._cache.set(key, weather)
        return weather

    async def get_weather_for_airport(self, airport: Airport) -> Optional[Weather]:
        """
        Método de conveniencia si quieres pedir 1 aeropuerto "suelto"
        (abre y cierra su propia sesión de aiohttp).
        """
        async with aiohttp.ClientSession() as session:
            return await self._fetch_and_cache(airport, session)

    async def preload_airports_weather(
        self,
        iata_codes: Set[str],
        airports: Dict[str, Airport],
    ) -> None:
        """
        Pre-carga el clima para un conjunto de aeropuertos.

        - Reutiliza una sola sesión HTTP.
        - Respeta el límite de concurrencia con el semaphore.
        - Ignora aeropuertos que no existen en el dict.
        """
        async with aiohttp.ClientSession() as session:
            tasks = []
            for code in iata_codes:
                airport = airports.get(code)
                if not airport:
                    print(f"[WeatherService] No encuentro datos para aeropuerto {code}")
                    continue
                tasks.append(self._fetch_and_cache(airport, session))

            results = await asyncio.gather(*tasks, return_exceptions=True)
            # podrías procesar exceptions aquí si quieres log detallado
