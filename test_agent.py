import unittest
from schemas import TripRequest, TravelItinerary, DayItinerary, Activity
from tools import get_weather_forecast
from agent import plan_trip
from unittest.mock import MagicMock, patch

# Mock tool for testing
def mock_tool(location: str):
    return f"Mock weather for {location}"

class TestTravelAgent(unittest.TestCase):
    def test_schemas(self):
        request = TripRequest(
            destination="Paris",
            start_date="2023-10-01",
            end_date="2023-10-05",
            interests=["Art", "Food"],
            budget="moderate"
        )
        self.assertEqual(request.destination, "Paris")
        
        activity = Activity(
            time_of_day="Morning",
            description="Visit Louvre",
            location="Louvre Museum"
        )
        
        day_itinerary = DayItinerary(
            day=1,
            date="2023-10-01",
            activities=[activity],
            weather_summary="Sunny"
        )
        
        itinerary = TravelItinerary(
            destination="Paris",
            forecast="Sunny all week",
            days=[day_itinerary]
        )
        self.assertEqual(itinerary.destination, "Paris")

    def test_weather_tool(self):
        forecast = get_weather_forecast("London", "2023-10-01")
        self.assertIn("Forecast for London", forecast)

    def test_agent_tool_passing(self):
        # This test verifies that we can pass a tool list to plan_trip
        # We won't actually call the API (which would fail without key), but we check the signature
        # and basic logic if we could mock the client.
        # For now, just ensuring the function accepts the argument is enough for this step.
        try:
            # Just calling it to see if it errors on argument mismatch
            # It will fail on API key or client init, but that's expected.
            # We just want to ensure 'tools' arg is accepted.
            pass
        except Exception:
            pass
        
        # A better test would be to inspect the function signature
        import inspect
        sig = inspect.signature(plan_trip)
        self.assertIn('tools', sig.parameters)

if __name__ == '__main__':
    unittest.main()
