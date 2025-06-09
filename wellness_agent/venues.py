import os
from math import radians, cos, sin, asin, sqrt

CATALOG = 'dais-hackathon-2025'
SCHEMA = 'bright_initiative'
VENUE_TABLE = 'google_maps_businesses'

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


def load_venue_data(user_profile):
    if spark_available:
        try:
            spark = SparkSession.builder.getOrCreate()
            full_table = f'`{CATALOG}`.`{SCHEMA}`.`{VENUE_TABLE}`'
            df = spark.read.table(full_table)
            user_lat = user_profile.get('lat', 37.77)
            user_lon = user_profile.get('lon', -122.42)
            # Compute distance using pandas UDF for performance if needed, else collect and compute
            pandas_df = df.select('name', 'category', 'lat', 'lon', 'rating').toPandas()
            pandas_df['distance_km'] = pandas_df.apply(
                lambda row: haversine(user_lat, user_lon, row['lat'], row['lon']), axis=1)
            preferred = set([cat.lower() for cat in user_profile['preferred_activities']])
            filtered = pandas_df[
                pandas_df['category'].str.lower().isin(preferred) &
                (pandas_df['distance_km'] <= user_profile['radius_km'])
            ]
            return filtered.to_dict(orient='records')
        except Exception as e:
            print(f"[WARN] Could not load from Databricks table: {e}. Using sample data.")
    # Fallback to sample data
    return [
        {"name": "Zen Flow Studio", "category": "yoga", "lat": 37.77, "lon": -122.42, "rating": 4.8, "distance_km": 0.8},
        {"name": "Dolores Park", "category": "park", "lat": 37.76, "lon": -122.43, "rating": 4.7, "distance_km": 1.5},
        {"name": "Mind Calm Center", "category": "meditation", "lat": 37.75, "lon": -122.44, "rating": 4.9, "distance_km": 2.1}
    ] 