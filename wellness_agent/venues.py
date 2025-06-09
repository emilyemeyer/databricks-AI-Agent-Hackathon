import os
from math import radians, cos, sin, asin, sqrt
from wellness_agent.defaults import CATALOG, SCHEMA, VENUE_TABLE

# Try to import Spark, fallback if not available
try:
    from pyspark.sql import SparkSession
    spark_available = True
except ImportError:
    spark_available = False


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c


def load_venue_data(user_profile, min_rating=4.0, min_reviews=10, max_distance_km=None, open_now=None, preferred_price_ranges=None):
    """
    Load venue data from the Databricks catalog (google_maps_businesses table) using the rich schema described in data_dictionary.md.
    Filters by user preferences, minimum rating, review count, distance, and optionally open hours and price range.
    Returns a list of venue dicts with all relevant fields for itinerary planning.
    Args:
        user_profile (dict): User profile with lat/lon and preferences.
        min_rating (float): Minimum rating to include.
        min_reviews (int): Minimum number of reviews to include.
        max_distance_km (float): Maximum distance from user (defaults to user_profile['radius_km']).
        open_now (bool or None): If True, only include venues open now (requires open_hours parsing).
        preferred_price_ranges (list or None): List of acceptable price ranges (e.g., ['$', '$$']).
    Returns:
        list of dict: Venue records with all relevant fields.
    """
    if not spark_available:
        raise RuntimeError("Spark is required to load venue data from the Databricks catalog.")

    spark = SparkSession.builder.getOrCreate()
    full_table = f'`{CATALOG}`.`{SCHEMA}`.`{VENUE_TABLE}`'
    df = spark.read.table(full_table)

    user_lat = user_profile.get('lat', 37.77)
    user_lon = user_profile.get('lon', -122.42)
    preferred = set([cat.lower() for cat in user_profile.get('preferred_activities', [])])
    max_distance_km = max_distance_km if max_distance_km is not None else user_profile.get('radius_km', 15)

    # Select relevant columns for itinerary planning
    columns = [
        'name', 'category', 'lat', 'lon', 'rating', 'reviews_count', 'open_hours',
        'price_range', 'description', 'url', 'address', 'main_image', 'phone_number'
    ]
    # Only select columns that exist in the table
    available_columns = [c for c in columns if c in df.columns]
    pandas_df = df.select(*available_columns).toPandas()

    # Calculate distance from user
    pandas_df['distance_km'] = pandas_df.apply(
        lambda row: haversine(user_lat, user_lon, row['lat'], row['lon']), axis=1)

    # Filter by preferred activities (category), distance, rating, review count, price range
    mask = (
        pandas_df['category'].str.lower().isin(preferred)
        & (pandas_df['distance_km'] <= max_distance_km)
        & (pandas_df['rating'] >= min_rating)
        & (pandas_df['reviews_count'] >= min_reviews)
    )
    if preferred_price_ranges:
        mask &= pandas_df['price_range'].isin(preferred_price_ranges)

    filtered = pandas_df[mask]

    # Optionally, filter by open_now (requires open_hours parsing, not implemented here)
    # TODO: Implement open_now filtering if needed

    # Convert to list of dicts for downstream use
    venues = filtered.to_dict(orient='records')
    return venues 