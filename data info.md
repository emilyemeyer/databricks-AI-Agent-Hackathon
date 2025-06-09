DThanks, Ivan. Here's a detailed breakdown of the available data from the **Bright Initiative** catalog within the `dais-hackathon-2025` catalog on Databricks. This includes the relevant schemas and tables you'll use for your **Wellness Journey Planner AI Agent**.

---

## 📚 CATALOG: `dais-hackathon-2025`

### SCHEMA: `bright_initiative`

This schema contains datasets curated by Bright Data (The Bright Initiative), and includes web-scraped information from Airbnb, Booking.com, and Google Maps. These are rich in features and ready to be used in your agent.

---

## 🗃️ Tables and Detailed Structure

### 1. ✅ `google_maps_businesses` (Core to Your Agent)

**Purpose**: Venue-level data scraped from Google Maps: gyms, parks, therapists, yoga studios, etc.

**Key Columns**:

| Column              | Type           | Description                                      |
| ------------------- | -------------- | ------------------------------------------------ |
| `name`              | String         | Business name                                    |
| `category`          | String         | Business type (e.g., “Gym”, “Park”, “Therapist”) |
| `address`           | String         | Full address                                     |
| `lat`, `lon`        | Double         | Coordinates for distance calculations            |
| `rating`            | Double         | Google rating (0–5)                              |
| `reviews_count`     | Long           | Number of reviews                                |
| `open_hours`        | Struct         | Weekly opening hours                             |
| `open_website`      | String         | URL for more info                                |
| `phone_number`      | String         | Optional contact info                            |
| `services_provided` | Array\[String] | List of services offered                         |
| `url`               | String         | Google Maps listing URL                          |

**Use in Agent**:

* Filter venues by category and rating.
* Use coordinates to calculate proximity.
* Use hours to recommend active/open venues.
* Include website/phone in itinerary details.

---

### 2. ✅ `airbnb_properties_information` (Optional Add-on)

**Purpose**: Rich details about Airbnb listings.

**Key Columns**:

| Column                   | Type           | Description               |
| ------------------------ | -------------- | ------------------------- |
| `listing_name`, `name`   | String         | Property name             |
| `description`            | String         | Overview of the property  |
| `price`, `total_price`   | Double         | Pricing info              |
| `guests`                 | Long           | Max guest capacity        |
| `lat`, `long`            | Double         | Geo location              |
| `availability`           | String         | Whether it's bookable     |
| `amenities`              | Array\[Struct] | Amenities grouped by type |
| `ratings`, `host_rating` | Double         | Overall and host ratings  |
| `is_guest_favorite`      | Boolean        | Flag for guest favorites  |
| `image`, `url`           | String         | Visual/Booking link       |

**Use in Agent**:

* Match user’s accommodation preference (budget, location).
* Pair with venue locations for wellness retreats.
* Use amenities to identify “wellness-friendly” listings (e.g., sauna, gym, nature access).

---

### 3. ✅ `booking_hotel_listings` (Optional Add-on)

**Purpose**: Booking.com hotel and accommodation listings.

**Key Columns**:

| Column                | Description                          |
| --------------------- | ------------------------------------ |
| `title`, `location`   | Hotel name and location              |
| `lat`, `lon`          | Coordinates for proximity filtering  |
| `description`         | General description                  |
| `review_score`        | Aggregate user rating                |
| `availability`        | Availability status                  |
| `property_highlights` | Amenities/features (e.g., spa, pool) |
| `url`                 | Link to the hotel’s listing          |

**Use in Agent**:

* Alternative to Airbnb for lodging.
* Include nearby hotel options in the itinerary.

---

### 4. ❓ CSV Mirror Tables

You’ll also find `_csv` versions of each table:

* `google_maps_businesses_csv`
* `airbnb_properties_information_csv`
* `booking_hotel_listings_csv`

These are **flattened versions** of the structured tables—use them if you want a quick preview, or easier schema without nested fields.

---

## 🔍 Recommended Filtering for Wellness Journey Planner

| Goal                    | Recommended Filters                                                                             |
| ----------------------- | ----------------------------------------------------------------------------------------------- |
| Find venues             | `category` IN (“Gym”, “Therapist”, “Yoga”, “Park”) in `google_maps_businesses`                  |
| Ensure quality          | `rating` ≥ 4.0, `reviews_count` > 20                                                            |
| Filter by location      | `lat`, `lon` vs user lat/lon using haversine                                                    |
| Match time availability | Check `open_hours` for target date                                                              |
| Lodging with amenities  | Look for keywords in `amenities` (e.g., sauna, garden, fitness center) in Airbnb/Booking tables |

---

## 📈 Sample Queries You Might Run

### A. Find Top-Rated Nearby Gyms

```sql
SELECT name, address, rating, reviews_count, lat, lon
FROM `dais-hackathon-2025`.`bright_initiative`.`google_maps_businesses`
WHERE category ILIKE '%gym%'
  AND rating >= 4.0
  AND reviews_count >= 10
```

### B. Filter Available Airbnb Wellness Retreats

```sql
SELECT name, location, price, guests, amenities, lat, long, url
FROM `dais-hackathon-2025`.`bright_initiative`.`airbnb_properties_information`
WHERE amenities LIKE '%sauna%' OR amenities LIKE '%garden%'
  AND ratings >= 4.5
  AND availability = 'true'
```

---

## 🛠️ Next Steps

Let me know if you'd like help with:

* Writing Python code to query these from your Databricks notebook or local agent
* Calculating distances between venues and the user
* Creating a scoring model to rank venues
* Building a sample itinerary using real data

You're ready to start querying and filtering! Would you like a Jupyter or Databricks notebook example to bootstrap your development?
