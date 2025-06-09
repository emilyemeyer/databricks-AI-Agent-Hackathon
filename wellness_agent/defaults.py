# wellness_agent/defaults.py
"""
Centralized static variables, preferences, and default values for the Wellness Journey Planner.
"""

# File paths
USER_PROFILE_PATH = 'user_profile.json'
PAST_ITINERARIES_PATH = 'past_itineraries.json'
VENUE_DATA_PATH = 'data/google_maps_businesses.csv'  # Used for local CSV fallback
LOG_PATH = 'agent.log'

# User profile defaults
DEFAULT_NAME = "ivan"
DEFAULT_CITY = "San Francisco, CA"
DEFAULT_LAT = 37.77
DEFAULT_LON = -122.42

DEFAULT_PROFILE = {
    "name": DEFAULT_NAME,
    "location": DEFAULT_CITY,
    "lat": DEFAULT_LAT,
    "lon": DEFAULT_LON,
    "radius_km": 15,
    "preferred_activities": [],
    "accessibility_needs": [],
    "budget_per_day": 50
}

# Databricks catalog/table defaults
CATALOG = 'dais-hackathon-2025'
SCHEMA = 'bright_initiative'
VENUE_TABLE = 'google_maps_businesses' 