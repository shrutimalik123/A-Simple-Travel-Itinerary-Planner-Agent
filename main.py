import argparse
import os
from dotenv import load_dotenv
from google.genai import types
from schemas import TripRequest, TravelItinerary
from agent import plan_trip

load_dotenv()

def get_current_weather(city: str) -> str:
    """
    Returns the current weather for a given city.
    """
    city = city.lower()
    if "rome" in city:
        return "sunny"
    elif "san francisco" in city:
        return "foggy"
    else:
        return "clear"

def run_trip_planner(request: TripRequest) -> TravelItinerary:
    """
    Helper function to run the trip planner with the configured tool and system instruction.
    """
    system_instruction = (
        "You are a friendly, expert travel agent. "
        "You must always use the get_current_weather tool before generating the itinerary. "
        "Your final output must strictly follow the TravelItinerary JSON schema and be well-reasoned."
    )
    
    # Create the Python object that declares the function as a callable tool
    # We pass the function directly, and the SDK wraps it in a Tool object automatically.
    # This satisfies the requirement of using a tool, while avoiding manual construction issues.
    weather_tool = get_current_weather
    
    return plan_trip(
        request, 
        tools=[weather_tool], 
        execution_tools={"get_current_weather": get_current_weather},
        system_instruction=system_instruction
    )

def main():
    parser = argparse.ArgumentParser(description="Travel Itinerary Planner Agent")
    parser.add_argument("--destination", type=str, help="Destination city/country")
    parser.add_argument("--start-date", type=str, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", type=str, help="End date (YYYY-MM-DD)")
    parser.add_argument("--interests", type=str, help="Comma-separated list of interests")
    parser.add_argument("--budget", type=str, help="Budget level (budget, moderate, luxury)")
    
    args = parser.parse_args()

    if not os.getenv("GOOGLE_API_KEY"):
        print("Warning: GOOGLE_API_KEY not found or invalid. Running in mock mode.")
        # return

    # Interactive mode if arguments are missing
    if not all([args.destination, args.start_date, args.end_date, args.interests, args.budget]):
        print("--- Travel Itinerary Planner ---")
        destination = args.destination or input("Enter destination: ")
        start_date = args.start_date or input("Enter start date (YYYY-MM-DD): ")
        end_date = args.end_date or input("Enter end date (YYYY-MM-DD): ")
        interests_input = args.interests or input("Enter interests (comma-separated): ")
        budget = args.budget or input("Enter budget (budget, moderate, luxury): ")
        
        interests = [i.strip() for i in interests_input.split(",")]
    else:
        destination = args.destination
        start_date = args.start_date
        end_date = args.end_date
        interests = [i.strip() for i in args.interests.split(",")]
        budget = args.budget

    request = TripRequest(
        destination=destination,
        start_date=start_date,
        end_date=end_date,
        interests=interests,
        budget=budget
    )

    print("\nGenerating itinerary... This may take a moment.")
    try:
        itinerary = run_trip_planner(request)
        print("\n--- Itinerary ---")
        print(itinerary.model_dump_json(indent=2))
    except Exception as e:
        print(f"\nError generating itinerary: {e}")

if __name__ == "__main__":
    main()
