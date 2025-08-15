import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_location(address: str):
    """
    Get latitude and longitude for a given address using Google Maps Geocoding API.
    """
    LOCATION_API_KEY = os.getenv("LOCATION_API_KEY")
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={LOCATION_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    else:
        raise Exception(f"Geocoding failed: {data['status']} - {data.get('error_message', '')}")