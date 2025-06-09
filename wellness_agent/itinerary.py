import json
import os
from math import radians, cos, sin, asin, sqrt

PAST_ITINERARIES_PATH = 'past_itineraries.json'

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

def score_venue(venue, user_profile):
    rating_weight = 2.0
    distance_weight = 1.0
    preference_weight = 1.5
    rating = venue.get('rating', 0) or 0
    distance = venue.get('distance_km', 999)
    category = venue.get('category', '').lower()
    preference_match = 1 if category in [a.lower() for a in user_profile['preferred_activities']] else 0
    score = (
        rating_weight * rating +
        distance_weight * (1.0 / (distance + 0.1)) +
        preference_weight * preference_match
    )
    return score

def build_itinerary(user_profile, venues, date):
    for v in venues:
        v['score'] = score_venue(v, user_profile)
    venues = sorted(venues, key=lambda v: v['score'], reverse=True)
    selected = []
    used_categories = set()
    for v in venues:
        if v['category'] not in used_categories:
            selected.append(v)
            used_categories.add(v['category'])
        if len(selected) >= 3:
            break
    if len(selected) < 3:
        for v in venues:
            if v not in selected:
                selected.append(v)
            if len(selected) >= 5:
                break
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