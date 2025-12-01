import random

def get_weather_forecast(location: str, date: str) -> str:
    """
    Returns a mock weather forecast for a given location and date.
    """
    conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy", "Windy"]
    temp_range = (15, 30)  # Celsius
    
    condition = random.choice(conditions)
    temp = random.randint(*temp_range)
    
    return f"Forecast for {location} on {date}: {condition}, {temp}°C"
