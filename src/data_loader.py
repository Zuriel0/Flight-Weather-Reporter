# data_loader.py
import csv
from typing import List, Dict, Tuple
from models import Ticket, Airport

def load_dataset(path: str) -> Tuple[List[Ticket], Dict[str, Airport]]:
    tickets: List[Ticket] = []
    airports: Dict[str, Airport] = {}

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 1) Ticket
            tickets.append(Ticket(
                origin=row["origin"],
                destination=row["destination"],
                airline=row["airline"],
                flight_num=str(row["flight_num"]),
            ))

            # 2) Aeropuerto origen
            o_code = row["origin_iata_code"]
            if o_code and o_code not in airports:
                airports[o_code] = Airport(
                    iata_code=o_code,
                    name=row["origin_name"],
                    latitude=float(row["origin_latitude"]),
                    longitude=float(row["origin_longitude"]),
                )

            # 3) Aeropuerto destino
            d_code = row["destination_iata_code"]
            if d_code and d_code not in airports:
                airports[d_code] = Airport(
                    iata_code=d_code,
                    name=row["destination_name"],
                    latitude=float(row["destination_latitude"]),
                    longitude=float(row["destination_longitude"]),
                )

    return tickets, airports
