import json
import os
from math import radians, cos, sin, asin, sqrt
from wellness_agent.defaults import PAST_ITINERARIES_PATH
from datetime import datetime, timedelta

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

def build_scheduled_itinerary(user_profile, venues, date, start_time, end_time, default_duration=60, speed_kmh=5):
    """
    Build a scheduled itinerary within a user-specified time window, accounting for travel and activity duration.
    Args:
        user_profile (dict): User profile with lat/lon.
        venues (list): List of venue dicts (should be pre-filtered/scored).
        date (str): Date string (YYYY-MM-DD).
        start_time (str): Start time (HH:MM, 24h).
        end_time (str): End time (HH:MM, 24h).
        default_duration (int): Default activity duration in minutes.
        speed_kmh (float): Travel speed in km/h.
    Returns:
        dict: Scheduled itinerary with activities and times.
    """
    current_time = datetime.strptime(f'{date} {start_time}', '%Y-%m-%d %H:%M')
    end_time_dt = datetime.strptime(f'{date} {end_time}', '%Y-%m-%d %H:%M')
    scheduled_activities = []
    last_lat = user_profile.get('lat', 37.77)
    last_lon = user_profile.get('lon', -122.42)

    for v in venues:
        # Calculate travel time (in minutes)
        distance = v.get('distance_km', 0)
        travel_minutes = int((distance / speed_kmh) * 60)
        duration = v.get('duration_minutes', default_duration)

        # Add travel time
        current_time += timedelta(minutes=travel_minutes)
        if current_time + timedelta(minutes=duration) > end_time_dt:
            break  # No more time for this activity

        scheduled_activities.append({
            'time': current_time.strftime('%H:%M'),
            'name': v['name'],
            'category': v['category'],
            'distance_km': round(distance, 2),
            'rating': v.get('rating', None),
            'duration_minutes': duration
        })
        # Advance time by activity duration
        current_time += timedelta(minutes=duration)
        last_lat, last_lon = v.get('lat', last_lat), v.get('lon', last_lon)

    return {
        'date': date,
        'activities': scheduled_activities
    } 