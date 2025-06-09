# Data Dictionary: Wellness Journey Planner

This document provides an overview of the available data sources, their schemas, and the meaning of key columns. Use this as a reference for data exploration, feature engineering, and modeling.

---

## Catalog: `dais-hackathon-2025`
### Schema: `bright_initiative`

### **Available Tables**
- `airbnb_properties_information`
- `airbnb_properties_information_csv`
- `booking_hotel_listings`
- `booking_hotel_listings_csv`
- `google_maps_businesses`
- `google_maps_businesses_csv`

---

## Table: `airbnb_properties_information`
**Description:**
Detailed Airbnb property listings with rich, nested information about amenities, host, pricing, reviews, and more.

**Columns:**
- `amenities`: Array of groups, each with a group name and items (name, value)
- `arrangement_details`: Array of name/value pairs (e.g., room arrangements)
- `availability`: String (availability status)
- `available_dates`: Array of available date strings
- `breadcrumbs`: String (location breadcrumbs)
- `cancellation_policy`: Array of cancellation policy details
- `category`: String (property category)
- `category_rating`: Array of category ratings
- `currency`: String (e.g., USD)
- `description`: String (property description)
- `description_by_sections`: Array of sectioned descriptions
- `description_html`: String (HTML description)
- `description_items`: Array of description items
- `details`: Array of details
- `discount`: String (discount info)
- `final_url`: String (final listing URL)
- `guests`: Long (max guests)
- `highlights`: Array of highlights
- `host_number_of_reviews`: Long
- `host_rating`: Double
- `host_response_rate`: Long
- `hosts_year`: Long (years as host)
- `house_rules`: Array of house rules
- `image`: String (main image URL)
- `images`: Array of image URLs
- `is_guest_favorite`: Boolean
- `is_supperhost`: Boolean
- `lat`: Double (latitude)
- `listing_name`: String
- `listing_title`: String
- `location`: String
- `location_details`: Array of location details
- `location_details_html`: String
- `long`: Double (longitude)
- `name`: String
- `pets_allowed`: Boolean
- `price`: Double (price per night)
- `pricing_details`: Struct (fees, price breakdown)
- `property_id`: String
- `property_number_of_reviews`: Long
- `ratings`: Double
- `reviews`: Array of review strings
- `seller_info`: Struct (host info)
- `total_price`: Double
- `travel_details`: Struct (check-in/out, guests)
- `url`: String (listing URL)

---

## Table: `airbnb_properties_information_csv`
**Description:**
A flattened, CSV-friendly version of Airbnb property listings. Useful for quick analysis and ML pipelines.

**Columns:**
- `name`: String
- `price`: Double
- `image`: String
- `description`: String
- `category`: String
- `availability`: Boolean
- `discount`: String
- `reviews`: String
- `ratings`: Double
- `seller_info`: String
- `breadcrumbs`: String
- `location`: String
- `lat`: Double
- `long`: Double
- `guests`: Integer
- `pets_allowed`: Boolean
- `description_items`: String
- `category_rating`: String
- `house_rules`: String
- `details`: String
- `highlights`: String
- `arrangement_details`: String
- `amenities`: String
- `images`: String
- `available_dates`: String
- `url`: String
- `final_url`: String
- `listing_title`: String
- `property_id`: Long
- `listing_name`: String
- `location_details`: String
- `description_by_sections`: String
- `description_html`: String
- `location_details_html`: String
- `is_supperhost`: Boolean
- `host_number_of_reviews`: Integer
- `host_rating`: Double
- `hosts_year`: Integer
- `host_response_rate`: Integer
- `is_guest_favorite`: Boolean
- `travel_details`: String
- `pricing_details`: String
- `total_price`: Double
- `currency`: String
- `cancellation_policy`: String
- `property_number_of_reviews`: Integer
- `country`: String
- `postcode_map_url`: String
- `host_image`: String

---

## Table: `google_maps_businesses`
**Description:**
Detailed business listings from Google Maps, including geolocation, category, hours, ratings, and more. Useful for finding wellness venues, gyms, parks, etc.

**Columns:**
- `address`: String
- `category`: String
- `category_search_input`: String
- `country`: String
- `description`: String
- `hotel_amenities`: Array of strings
- `hotel_star_ratings`: String
- `lat`: Double
- `lon`: Double
- `main_image`: String
- `name`: String
- `number_of_results`: Long
- `open_hours`: Struct (day-specific hours)
- `open_hours_updated`: String
- `open_website`: String
- `phone_number`: String
- `place_an_order`: Array of structs (platform_name, platform_url)
- `place_id`: String
- `popular_times`: String
- `price_range`: String
- `rating`: Double
- `reviews`: String
- `reviews_count`: Long
- `services_provided`: Array of strings
- `url`: String
- `zoom_level`: Long

---

## Table: `google_maps_businesses_csv`
**Description:**
A flattened, CSV-friendly version of Google Maps business listings. Useful for quick analysis and ML pipelines.

**Columns:**
- `name`: String
- `category`: String
- `address`: String
- `description`: String
- `Open website`: String
- `phone number`: String
- `open_hours`: String
- `open_hours_updated`: String
- `reviews_count`: Integer
- `rating`: Double
- `main_image`: String
- `reviews`: String
- `url`: String
- `lat`: Double
- `lon`: Double
- `place_id`: String
- `country`: String
- `price_range`: String
- `services_provided`: String
- `hotel_amenities`: String
- `hotel_star_ratings`: String
- `zip_code`: String
- `sample`: String
- `country_name`: String
- `category_search_input`: String
- `open_website`: String
- `phone_number`: String
- `place_an_order`: String
- `records_limit`: String
- `number_of_results`: Integer
- `zoom_level`: Integer
- `permanently_closed`: String
- `popular_times`: String

---

## Table: `booking_hotel_listings`
**Description:**
Detailed hotel listings from Booking.com, including amenities, location, reviews, and more. (Schema not fully shown in sample, but likely similar to the CSV version below.)

---

## Table: `booking_hotel_listings_csv`
**Description:**
A flattened, CSV-friendly version of Booking.com hotel listings. Useful for quick analysis and ML pipelines.

**Columns:**
- `timestamp`: String
- `url`: String
- `hotel_id`: String
- `title`: String
- `location`: String
- `country`: String
- `city`: String
- `metro_railway_access`: String
- `images`: String
- `number_of_reviews`: String
- `review_score`: String
- `description`: String
- `property_highlights`: String
- `most_popular_facilities`: String
- `availability`: String
- `reviews_scores`: String
- `top_reviews`: String
- `managed_by`: String
- `manager_score`: Double
- `property_information`: String
- `manager_language_spoken`: String
- `property_surroundings`: String
- `popular_facilities`: String
- `house_rules`: String
- `fine_print`: String
- `coordinates`: String

---

# Notes
- For all tables, see the Databricks schema browser or use the provided data_ingestion.py script for the most up-to-date column info.
- The `_csv` tables are flattened and easier to use for ML and analytics, while the non-CSV tables contain richer, nested data.
- Some columns may be NULL or missing for certain rows, depending on data source completeness.

---

This data dictionary should help you and your team quickly understand the available data and plan your data processing and modeling steps. 