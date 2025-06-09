import json
import os
from typing import Optional, Dict
from wellness_agent.defaults import DEFAULT_CITY, DEFAULT_LAT, DEFAULT_LON, DEFAULT_NAME, DEFAULT_PROFILE, USER_PROFILE_PATH

def load_user_profile(skip_prompts: bool = False, default_profile: Optional[Dict] = None) -> Dict:
    """
    Load the user profile from file, or create it with defaults and/or prompts.
    If skip_prompts is True, use defaults or provided default_profile for all fields.
    Args:
        skip_prompts (bool): If True, do not prompt the user and use defaults.
        default_profile (Optional[Dict]): If provided, use as the default profile.
    Returns:
        dict: The user profile.
    """
    if os.path.exists(USER_PROFILE_PATH):
        with open(USER_PROFILE_PATH, 'r') as f:
            return json.load(f)
    else:
        if default_profile:
            profile = default_profile.copy()
        else:
            profile = DEFAULT_PROFILE.copy()
        if not skip_prompts:
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
            name = input(f"What is your name? (default: {DEFAULT_NAME}) ").strip() or DEFAULT_NAME
            profile.update({"name": name, "location": location, "lat": lat, "lon": lon})
        save_user_profile(profile)
        return profile

def save_user_profile(profile):
    with open(USER_PROFILE_PATH, 'w') as f:
        json.dump(profile, f, indent=2) 