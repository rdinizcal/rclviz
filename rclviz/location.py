from typing import Dict
from geopy.geocoders import Nominatim

class LocationNotFoundError(Exception):
    pass

def fetch_location(university: str) -> Dict[str, float]:
    """Fetches the latitude and longitude of a university using geopy."""
    geolocator = Nominatim(user_agent="world_academic_collab")
    location = geolocator.geocode(university)
    if not location: 
        raise LocationNotFoundError(f"Could not find location for {university}.")
    else: 
        return {'lat': location.latitude, 'lng': location.longitude}
