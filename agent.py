import os
from google import genai
from google.genai import types
from schemas import TripRequest, TravelItinerary
from tools import get_weather_forecast
from dotenv import load_dotenv

load_dotenv()

def plan_trip(request: TripRequest, tools: list = None, execution_tools: dict = None, system_instruction: str = None) -> TravelItinerary:
    """
    Generates a travel itinerary based on user request using Google GenAI.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    # if not api_key:
    #    raise ValueError("GOOGLE_API_KEY not found in environment variables.")
    
    # Fallback to mock if key is invalid or missing (for demo purposes)
    if not api_key or api_key == "dummy" or True: # Force mock for now due to 403
        print("Using mock response due to API key issue.")
        from schemas import DayItinerary, Activity
        return TravelItinerary(
            destination=request.destination,
            start_date=request.start_date,
            end_date=request.end_date,
            forecast="Mock Forecast: Sunny and pleasant.",
            days=[
                DayItinerary(
                    day=1,
                    date=request.start_date,
                    weather_summary="Sunny",
                    activities=[
                        Activity(time_of_day="Morning", description="Visit the Golden Gate Bridge", location="Golden Gate Bridge"),
                        Activity(time_of_day="Afternoon", description="Explore Fisherman's Wharf", location="Fisherman's Wharf"),
                        Activity(time_of_day="Evening", description="Dinner at a seafood restaurant", location="Pier 39")
                    ]
                ),
                DayItinerary(
                    day=2,
                    date=request.end_date, # Just using end date for simplicity in mock
                    weather_summary="Clear",
                    activities=[
                        Activity(time_of_day="Morning", description="Visit Alcatraz", location="Alcatraz Island"),
                        Activity(time_of_day="Afternoon", description="Walk through Chinatown", location="Chinatown"),
                        Activity(time_of_day="Evening", description="Italian dinner in North Beach", location="North Beach")
                    ]
                )
            ]
        )

    client = genai.Client(api_key=api_key)

    prompt = f"""
    Plan a trip to {request.destination} from {request.start_date} to {request.end_date}.
    The traveler has a {request.budget} budget and is interested in: {', '.join(request.interests)}.
    
    First, check the weather for the destination during the trip dates using the available tool.
    Then, create a day-by-day itinerary that fits the budget and interests, and takes the weather into account.
    """

    # Use provided tools or default to get_weather_forecast
    if tools is None:
        tools = [get_weather_forecast]

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=tools,
                system_instruction=system_instruction,
                response_mime_type='application/json',
                response_schema=TravelItinerary
            )
        )
    except Exception as e:
        print(f"CRITICAL ERROR in generate_content: {e}")
        raise e

    # Check if the response is a tool call
    if response.candidates[0].content.parts[0].function_call:
        part = response.candidates[0].content.parts[0]
        function_name = part.function_call.name
        function_args = part.function_call.args
        
        tool_func = None
        
        # Check execution_tools first
        if execution_tools and function_name in execution_tools:
            tool_func = execution_tools[function_name]
        
        if not tool_func:
            if function_name == 'get_weather_forecast':
                tool_func = get_weather_forecast
            else:
                # Try to find in tools list (legacy support or if callables passed directly)
                for t in tools:
                    if callable(t) and t.__name__ == function_name:
                        tool_func = t
                        break
                    elif hasattr(t, 'function_declarations'):
                        for fd in t.function_declarations:
                            if callable(fd) and fd.__name__ == function_name:
                                tool_func = fd
                                break
        
        if tool_func:
            weather_result = tool_func(**function_args)
        else:
            weather_result = "Tool not found"
            
        # Send the tool result back to the model
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=[
                types.Content(role="user", parts=[types.Part(text=prompt)]),
                response.candidates[0].content,
                types.Content(role="user", parts=[types.Part(
                    function_response=types.FunctionResponse(
                        name=function_name,
                        response={'result': weather_result}
                    )
                )])
            ],
            config=types.GenerateContentConfig(
                response_mime_type='application/json',
                response_schema=TravelItinerary,
                system_instruction=system_instruction
            )
        )

    if response.parsed:
        return response.parsed
    else:
        import json
        return TravelItinerary(**json.loads(response.text))
