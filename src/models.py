# models.py
from dataclasses import dataclass
from datetime import date
from typing import Optional, Dict

@dataclass
class Ticket:
    origin: str
    destination: str
    airline: str
    flight_num: str

@dataclass
class Airport:
    iata_code: str
    name: str
    latitude: float
    longitude: float

@dataclass
class Weather:
    date: date
    temperature: float
    description: str
    raw: Dict
