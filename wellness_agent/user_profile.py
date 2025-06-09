import json
import os

USER_PROFILE_PATH = 'user_profile.json'

DEFAULT_CITY = "San Francisco, CA"
DEFAULT_LAT = 37.77
DEFAULT_LON = -122.42

def load_user_profile():
    if os.path.exists(USER_PROFILE_PATH):
        with open(USER_PROFILE_PATH, 'r') as f:
            return json.load(f)
    else:
        print("Set your location:")
        use_coords = input("Do you want to enter latitude/longitude? [y/N] ").strip().lower()
        if use_coords == 'y':
            try:
                lat = float(input("Enter latitude: ").strip())
                lon = float(input("Enter longitude: ").strip())
            except Exception:
                print("Invalid input. Using default coordinates.")
                lat, lon = DEFAULT_LAT, DEFAULT_LON
            location = f"({lat}, {lon})"
        else:
            location = input(f"What is your city/location? (default: {DEFAULT_CITY}) ").strip() or DEFAULT_CITY
            lat, lon = DEFAULT_LAT, DEFAULT_LON  # Optionally, geocode here
        profile = {
            "name": input("What is your name? "),
            "location": location,
            "lat": lat,
            "lon": lon,
            "radius_km": 15,
            "preferred_activities": ["yoga", "meditation", "gym", "nature"],
            "accessibility_needs": [],
            "budget_per_day": 50
        }
        save_user_profile(profile)
        return profile

def save_user_profile(profile):
    with open(USER_PROFILE_PATH, 'w') as f:
        json.dump(profile, f, indent=2) 