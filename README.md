Here is your **complete, updated project plan** for the **Wellness Journey Planner AI Agent**, designed to run entirely from the **terminal** and use **local file-based storage** — perfect for the AI Agents Hackathon at the Data + AI Summit 2025.

---

# 🧘 Wellness Journey Planner – AI Agent Project Plan

## 🎯 Project Overview

**Goal**:
Develop a **terminal-based AI agent** that curates personalized wellness itineraries using local business data. It recommends **gyms, therapy centers, parks**, and optionally wellness-focused accommodations. The agent builds a day-by-day schedule based on user preferences and continuously learns and adapts using locally stored user history.

---

## 🧱 Architecture Overview

| Layer         | Technology/Methodology                                  |
| ------------- | ------------------------------------------------------- |
| Interface     | Terminal-based (CLI using Python `input()`/`print()`)   |
| Agent Logic   | Python class-based AI logic with state tracking         |
| Data Storage  | `user_profile.json` and `past_itineraries.json` (local) |
| Data Sources  | Bright Data (Google Maps listings, Airbnb listings)     |
| Processing    | Pandas, geopy (distance), basic scoring heuristics      |
| Future Option | Extend with LangChain or AutoGen for enhanced UX        |

---

## 🗃️ Datasets Used

### 1. **Bright Data – Google Maps Listings**

* Fields: Name, category, rating, reviews, address, coordinates
* Filtered categories: `gym`, `park`, `therapist`, `meditation`, `yoga`

### 2. **Bright Data – Airbnb Listings (Optional)**

* Used if multi-day itinerary includes accommodation

---

## 🛠️ Components

### 1. **Agent Boot & Welcome**

* Detects or creates `user_profile.json`
* Greets the user:

  ```
  Hello Ivan! Welcome back.
  Let’s plan your next wellness day.
  ```

---

### 2. **User Profile Management**

#### File: `user_profile.json`

Stores preferences such as:

```json
{
  "name": "Ivan",
  "location": "San Francisco, CA",
  "radius_km": 15,
  "preferred_activities": ["yoga", "meditation", "gym", "nature"],
  "accessibility_needs": ["wheelchair"],
  "budget_per_day": 50
}
```

#### Agent Capabilities:

* Load on startup
* Prompt edits as needed:

  > “Want to update your preferred activities? \[y/N]”

---

### 3. **User Interaction Flow**

#### a. Set Trip Parameters

* Date range: `1 day` or `multi-day`
* Max hours per day
* Activity intensity preference (light/medium/high)

#### b. Agent Queries Data

* Loads and filters venue dataset
* Ranks venues by:

  * Proximity (via Haversine distance)
  * Ratings
  * Category match
  * Accessibility flags

#### c. Itinerary Construction

* Selects 3–5 activities per day
* Spaces activities with breaks
* Outputs a daily plan in terminal:

  ```
  📅 Monday, June 10
  - 9:00 AM: Morning yoga @ Zen Flow Studio (0.8 km)
  - 11:30 AM: Walk @ Dolores Park (1.5 km)
  - 2:00 PM: Meditation class @ Mind Calm Center (2.1 km)
  ```

#### d. Save to File

* Appends to `past_itineraries.json` for recall or learning

---

### 4. **File: `past_itineraries.json`**

Example structure:

```json
[
  {
    "date": "2025-06-10",
    "activities": [
      {"time": "9:00", "name": "Zen Flow Studio", "category": "yoga"},
      {"time": "11:30", "name": "Dolores Park", "category": "park"}
    ]
  }
]
```

---

### 5. **Customization & Feedback**

* User can say:

  * “I want more outdoors today.”
  * “Skip gym today.”
* Agent dynamically rebuilds the day
* Asks for feedback after the itinerary:

  > “How was your day? \[1–5 stars]”

---

## 🧪 Sample Workflow

```bash
$ python wellness_agent.py
```

```
👋 Hi Ivan! Welcome back to your Wellness Journey Planner.
Shall we plan a new wellness day? [Y/n]
> Y

What day are you planning for? (YYYY-MM-DD)
> 2025-06-10

Would you like to update your preferences?
> n

Great. Planning a medium-intensity day near San Francisco...

Here's your wellness itinerary for Tuesday:
- 8:30 AM: Sunrise Yoga @ BayView Studio
- 10:30 AM: Park walk @ Golden Gate Park
- 1:00 PM: Sound Meditation @ Inner Peace SF
...
Would you like to save this? [Y/n]
> Y

Done! Enjoy your journey. 🌿
```

---

## 🧠 AI Logic (Simplified)

1. **Scoring Formula**:

   ```
   score = rating_weight * rating + distance_weight * (1/distance_km) + preference_match_weight
   ```

2. **Itinerary Algorithm**:

   * Choose top-scoring venues in different time slots
   * Ensure venue types are balanced (not all gyms)
   * Respect user’s max hours per day

3. **Learning From Past**:

   * Adjust scores if user rates certain categories higher/lower

---

## 🗓️ Hackathon Execution Timeline (6 Hours)

| Time   | Task                                     |
| ------ | ---------------------------------------- |
| 0–1 hr | Setup project structure & CLI boot flow  |
| 1–2 hr | Implement user profile read/write logic  |
| 2–3 hr | Load & clean Bright Data sample          |
| 3–4 hr | Build scoring and itinerary logic        |
| 4–5 hr | Enable feedback and personalization loop |
| 5–6 hr | Testing, polish CLI, prep demo           |

---

## ✅ Success Criteria

* [x] Runs entirely in terminal
* [x] Uses live or sample business datasets
* [x] Generates complete, personalized itinerary
* [x] Updates and reads user profile from local file
* [x] Logs itinerary history for future learning

---

Would you like me to generate the starter Python file structure and stub functions next?
