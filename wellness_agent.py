"""
wellness_agent.py
Main entry point for the Wellness Journey Planner CLI agent.
Coordinates user interaction, itinerary planning, and AI explanations.
"""

import sys
from datetime import datetime, timedelta
from wellness_agent.user_profile import load_user_profile
from wellness_agent.itinerary import load_past_itineraries, save_past_itinerary, build_itinerary
from wellness_agent.venues import load_venue_data
from wellness_agent.llm import llm_explain_itinerary
from wellness_agent.logging import log_event, log_llm_interaction
from wellness_agent.defaults import *


def prompt_yes_no(message: str, default: bool = True) -> bool:
    """
    Prompt the user for a yes/no answer.
    Args:
        message (str): The prompt message.
        default (bool): The default value if the user presses Enter.
    Returns:
        bool: True for yes, False for no.
    """
    suffix = "[Y/n]" if default else "[y/N]"
    while True:
        resp = input(f"{message} {suffix} ").strip().lower()
        if not resp:
            return default
        if resp in ("y", "yes"): return True
        if resp in ("n", "no"): return False
        print("Please enter 'y' or 'n'.")


def prompt_date(message: str, default_date: str = None) -> str:
    """
    Prompt the user for a date in YYYY-MM-DD format, with a default suggestion.
    Returns:
        str: The validated date string.
    """
    while True:
        prompt = message
        if default_date:
            prompt += f" (default: {default_date})"
        date = input(prompt + " ").strip()
        if not date and default_date:
            return default_date
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return date
        except ValueError:
            print("Please enter a valid date in YYYY-MM-DD format.")


def print_itinerary(itinerary: dict):
    """
    Print the formatted itinerary to the terminal.
    Args:
        itinerary (dict): The itinerary dictionary.
    """
    print(f"\nHere's your wellness itinerary for {itinerary['date']}:")
    for act in itinerary["activities"]:
        print(f"- {act['time']}: {act['name']} ({act['category']}, {act['distance_km']} km, rating: {act['rating']})")


def main():
    """
    Main CLI flow for the Wellness Journey Planner.
    Handles user profile, itinerary planning, AI explanation, and logging.
    """
    print("\n👋 Welcome to the Wellness Journey Planner!")
    try:
        # Use skip_prompts=True to prefill defaults if profile does not exist
        user_profile = load_user_profile(skip_prompts=True)
        log_event('user_profile_loaded', user_profile)
        print(f"Hello {user_profile['name']}! Location: {user_profile['location']}")
    except Exception as e:
        log_event('error', {'stage': 'load_user_profile', 'error': str(e)})
        print(f"[ERROR] Failed to load user profile: {e}")
        sys.exit(1)

    if not prompt_yes_no("Shall we plan a new wellness day?", default=True):
        print("Goodbye!")
        log_event('exit', {'reason': 'user_declined'})
        return

    # Suggest tomorrow as the default itinerary date
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    date = prompt_date("What day are you planning for? (YYYY-MM-DD)", default_date=tomorrow)

    try:
        venues = load_venue_data(user_profile)
    except Exception as e:
        log_event('error', {'stage': 'load_venue_data', 'error': str(e)})
        print(f"[ERROR] Failed to load venue data: {e}")
        sys.exit(1)

    if not venues:
        print("No venues found for your preferences and location.")
        log_event('no_venues_found', {'user_profile': user_profile, 'date': date})
        return

    try:
        itinerary = build_itinerary(user_profile, venues, date)
        log_event('itinerary_built', itinerary)
    except Exception as e:
        log_event('error', {'stage': 'build_itinerary', 'error': str(e)})
        print(f"[ERROR] Failed to build itinerary: {e}")
        sys.exit(1)

    print_itinerary(itinerary)

    if prompt_yes_no("\nWould you like to ask the AI about your plan or get an explanation?", default=True):
        user_question = input("Type your question about the itinerary (or press Enter for a summary): ").strip()
        if not user_question:
            user_question = "Can you summarize my wellness itinerary and explain why these activities were chosen for me?"
        try:
            response = llm_explain_itinerary(itinerary, user_question)
            print(f"\n🤖 AI says: {response}")
            log_llm_interaction({'itinerary': itinerary, 'user_question': user_question}, response)
        except Exception as e:
            log_event('error', {'stage': 'llm_explain_itinerary', 'error': str(e)})
            print(f"[ERROR] AI explanation failed: {e}")

    if prompt_yes_no("\nWould you like to save this?", default=True):
        try:
            save_past_itinerary(itinerary)
            log_event('itinerary_saved', itinerary)
            print("Itinerary saved!")
        except Exception as e:
            log_event('error', {'stage': 'save_past_itinerary', 'error': str(e)})
            print(f"[ERROR] Failed to save itinerary: {e}")

    print("Done! Enjoy your journey. 🌿")
    log_event('session_complete', {'date': date})


if __name__ == "__main__":
    main() 