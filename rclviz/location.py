from typing import Dict
from geopy.geocoders import Nominatim

def fetch_location(university: str) -> Dict[str, float]:
    """Fetches the latitude and longitude of a university using geopy."""
    geolocator = Nominatim(user_agent="world_academic_collab")
    location = geolocator.geocode(university)
    if not location: 
        print("[WARN] Did not find " + str(university) + ". Excluding connection from plot.")
        return {'lat': 0, 'lng': 0}
    else: return {'lat': location.latitude, 'lng': location.longitude}
