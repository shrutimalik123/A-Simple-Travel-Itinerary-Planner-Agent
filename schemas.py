from pydantic import BaseModel, Field
from typing import List, Optional

class TripRequest(BaseModel):
    destination: str = Field(..., description="The city and country the user wants to visit.")
    start_date: str = Field(..., description="Start date of the trip in YYYY-MM-DD format.")
    end_date: str = Field(..., description="End date of the trip in YYYY-MM-DD format.")
    interests: List[str] = Field(..., description="List of user interests (e.g., museums, food, hiking).")
    budget: str = Field(..., description="Budget level (e.g., budget, moderate, luxury).")

class Activity(BaseModel):
    time_of_day: str = Field(..., description="Time of day (Morning, Afternoon, Evening).")
    description: str = Field(..., description="Description of the activity.")
    location: Optional[str] = Field(None, description="Location of the activity.")

class DayItinerary(BaseModel):
    day: int = Field(..., description="Day number of the trip.")
    date: str = Field(..., description="Date of the activity.")
    activities: List[Activity] = Field(..., description="List of activities for the day.")
    weather_summary: Optional[str] = Field(None, description="Brief weather summary for this day.")

class TravelItinerary(BaseModel):
    destination: str = Field(..., description="The destination of the trip.")
    forecast: str = Field(..., description="Overall weather forecast summary for the trip.")
    days: List[DayItinerary] = Field(..., description="Day-by-day itinerary.")
