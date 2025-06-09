import json
import os
from datetime import datetime
import pandas as pd
from math import radians, cos, sin, asin, sqrt
from wellness_agent.user_profile import load_user_profile, save_user_profile
from wellness_agent.itinerary import load_past_itineraries, save_past_itinerary, build_itinerary
from wellness_agent.venues import load_venue_data
from wellness_agent.llm import llm_explain_itinerary
from wellness_agent.logging import log_event, log_llm_interaction

USER_PROFILE_PATH = 'user_profile.json'
PAST_ITINERARIES_PATH = 'past_itineraries.json'
VENUE_DATA_PATH = 'data/google_maps_businesses.csv'  # Update as needed

# 1. User Profile Management

def load_user_profile():
    if os.path.exists(USER_PROFILE_PATH):
        with open(USER_PROFILE_PATH, 'r') as f:
            return json.load(f)
    else:
        profile = {
            "name": input("What is your name? "),
            "location": input("What is your city/location? "),
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

# 2. Past Itineraries

def load_past_itineraries():
    if os.path.exists(PAST_ITINERARIES_PATH):
        with open(PAST_ITINERARIES_PATH, 'r') as f:
            return json.load(f)
    else:
        return []

def save_past_itinerary(itinerary):
    all_itins = load_past_itineraries()
    all_itins.append(itinerary)
    with open(PAST_ITINERARIES_PATH, 'w') as f:
        json.dump(all_itins, f, indent=2)

# 3. Venue Data

def haversine(lat1, lon1, lat2, lon2):
    # Calculate the great circle distance between two points on the earth (km)
    R = 6371  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

def load_venue_data(user_profile):
    if not os.path.exists(VENUE_DATA_PATH):
        print("Venue data file not found. Using sample data.")
        return [
            {"name": "Zen Flow Studio", "category": "yoga", "lat": 37.77, "lon": -122.42, "rating": 4.8, "distance_km": 0.8},
            {"name": "Dolores Park", "category": "park", "lat": 37.76, "lon": -122.43, "rating": 4.7, "distance_km": 1.5},
            {"name": "Mind Calm Center", "category": "meditation", "lat": 37.75, "lon": -122.44, "rating": 4.9, "distance_km": 2.1}
        ]
    df = pd.read_csv(VENUE_DATA_PATH)
    # For demo, assume user location is San Francisco (lat/lon hardcoded)
    # In production, use geocoding to get user lat/lon from city name
    user_lat, user_lon = 37.77, -122.42
    df['distance_km'] = df.apply(lambda row: haversine(user_lat, user_lon, row['lat'], row['lon']), axis=1)
    # Filter by preferred activities (category) and radius
    preferred = set([cat.lower() for cat in user_profile['preferred_activities']])
    filtered = df[df['category'].str.lower().isin(preferred) & (df['distance_km'] <= user_profile['radius_km'])]
    return filtered.to_dict(orient='records')

# 4. Scoring and Itinerary Construction

def score_venue(venue, user_profile):
    # Weights
    rating_weight = 2.0
    distance_weight = 1.0
    preference_weight = 1.5
    # Score components
    rating = venue.get('rating', 0) or 0
    distance = venue.get('distance_km', 999)
    category = venue.get('category', '').lower()
    preference_match = 1 if category in [a.lower() for a in user_profile['preferred_activities']] else 0
    # Lower distance is better, so use inverse
    score = (
        rating_weight * rating +
        distance_weight * (1.0 / (distance + 0.1)) +  # avoid div by zero
        preference_weight * preference_match
    )
    return score

def build_itinerary(user_profile, venues, date):
    # Score all venues
    for v in venues:
        v['score'] = score_venue(v, user_profile)
    # Sort by score, then by category diversity
    venues = sorted(venues, key=lambda v: v['score'], reverse=True)
    selected = []
    used_categories = set()
    for v in venues:
        if v['category'] not in used_categories:
            selected.append(v)
            used_categories.add(v['category'])
        if len(selected) >= 3:
            break
    # If not enough diversity, fill with top remaining
    if len(selected) < 3:
        for v in venues:
            if v not in selected:
                selected.append(v)
            if len(selected) >= 5:
                break
    # Build time slots
    times = ["9:00 AM", "11:30 AM", "2:00 PM", "4:00 PM", "6:00 PM"]
    activities = []
    for i, v in enumerate(selected):
        activities.append({
            "time": times[i],
            "name": v["name"],
            "category": v["category"],
            "distance_km": round(v["distance_km"], 2),
            "rating": v.get("rating", None)
        })
    return {
        "date": date,
        "activities": activities
    }

# 5. Main CLI Flow

def main():
    print("\n👋 Welcome to the Wellness Journey Planner!")
    user_profile = load_user_profile()
    log_event('user_profile_loaded', user_profile)
    print(f"Hello {user_profile['name']}! Location: {user_profile['location']}")
    plan = input("Shall we plan a new wellness day? [Y/n] ").strip().lower()
    if plan and plan != 'y':
        print("Goodbye!")
        log_event('exit', {'reason': 'user_declined'})
        return
    # Date input with validation
    while True:
        date = input("What day are you planning for? (YYYY-MM-DD) ").strip()
        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("Please enter a valid date in YYYY-MM-DD format.")
    venues = load_venue_data(user_profile)
    if not venues:
        print("No venues found for your preferences and location.")
        log_event('no_venues_found', {'user_profile': user_profile, 'date': date})
        return
    itinerary = build_itinerary(user_profile, venues, date)
    log_event('itinerary_built', itinerary)
    print(f"\nHere's your wellness itinerary for {date}:")
    for act in itinerary["activities"]:
        print(f"- {act['time']}: {act['name']} ({act['category']}, {act['distance_km']} km, rating: {act['rating']})")
    # LLM chat/explanation
    ask_ai = input("\nWould you like to ask the AI about your plan or get an explanation? [Y/n] ").strip().lower()
    if not ask_ai or ask_ai == 'y':
        user_question = input("Type your question about the itinerary (or press Enter for a summary): ").strip()
        if not user_question:
            user_question = "Can you summarize my wellness itinerary and explain why these activities were chosen for me?"
        response = llm_explain_itinerary(itinerary, user_question)
        print(f"\n🤖 AI says: {response}")
        log_llm_interaction({'itinerary': itinerary, 'user_question': user_question}, response)
    save = input("\nWould you like to save this? [Y/n] ").strip().lower()
    if not save or save == 'y':
        save_past_itinerary(itinerary)
        log_event('itinerary_saved', itinerary)
        print("Itinerary saved!")
    print("Done! Enjoy your journey. 🌿")
    log_event('session_complete', {'date': date})

if __name__ == "__main__":
    main() 