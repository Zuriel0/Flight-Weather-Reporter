# src/weather_client.py
import aiohttp
from typing import Any, Dict

class WeatherApiError(Exception):
    """Errores específicos al consumir WeatherAPI."""
    pass

class WeatherClient:
    BASE_URL = "https://api.weatherapi.com/v1"

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def fetch_current_by_latlon(
        self,
        session: aiohttp.ClientSession,
        lat: float,
        lon: float,
    ) -> Dict[str, Any]:
        """
        Llama a /current.json usando lat,lon como q=lat,lon
        """
        params = {
            "key": self.api_key,
            "q": f"{lat},{lon}",  # WeatherAPI permite q=48.8567,2.3508 :contentReference[oaicite:4]{index=4}
            "aqi": "no",
        }

        url = f"{self.BASE_URL}/current.json"
        async with session.get(url, params=params, timeout=10) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise WeatherApiError(f"HTTP {resp.status}: {text}")
            return await resp.json()

    async def fetch_current_by_iata(
        self,
        session: aiohttp.ClientSession,
        iata_code: str,
    ) -> Dict[str, Any]:
        """
        **Opcional**: usar q=iata:XXX si prefieres trabajar con códigos IATA.
        WeatherAPI soporta q=iata:<código> (ej: iata:DXB). :contentReference[oaicite:5]{index=5}
        """
        params = {
            "key": self.api_key,
            "q": f"iata:{iata_code}",
            "aqi": "no",
        }
        url = f"{self.BASE_URL}/current.json"
        async with session.get(url, params=params, timeout=10) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise WeatherApiError(f"HTTP {resp.status}: {text}")
            return await resp.json()
