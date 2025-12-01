import streamlit as st
import datetime
from schemas import TripRequest
from main import run_trip_planner

st.set_page_config(page_title="Travel Itinerary Planner", page_icon="✈️", layout="wide")

st.title("✈️ Travel Itinerary Planner")
st.markdown("Plan your perfect trip with our AI agent!")

with st.form("trip_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        destination = st.text_input("Destination", placeholder="e.g., Tokyo, Japan")
        start_date = st.date_input("Start Date", min_value=datetime.date.today())
        
    with col2:
        budget = st.selectbox("Budget", ["budget", "moderate", "luxury"])
        end_date = st.date_input("End Date", min_value=start_date)

    interests_str = st.text_area("Interests", placeholder="e.g., Museums, Food, Hiking, Anime")
    
    submitted = st.form_submit_button("Plan Trip")

if submitted:
    if not destination or not interests_str:
        st.error("Please fill in all fields.")
    else:
        interests = [i.strip() for i in interests_str.split(",")]
        
        # Convert dates to string format expected by schema
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        
        request = TripRequest(
            destination=destination,
            start_date=start_date_str,
            end_date=end_date_str,
            interests=interests,
            budget=budget
        )
        
        with st.spinner("Generating your itinerary... This may take a moment."):
            try:
                itinerary = run_trip_planner(request)
                
                st.success(f"Itinerary for {itinerary.destination} Ready!")
                
                st.markdown(f"### 🌤️ Weather Forecast")
                st.info(itinerary.forecast)
                
                st.markdown("### 📅 Daily Plan")
                for day in itinerary.days:
                    with st.expander(f"Day {day.day}: {day.date}", expanded=True):
                        if day.weather_summary:
                            st.caption(f"Weather: {day.weather_summary}")
                        
                        for activity in day.activities:
                            st.markdown(f"**{activity.time_of_day}**: {activity.description}")
                            if activity.location:
                                st.markdown(f"*Location: {activity.location}*")
                                
            except Exception as e:
                st.error(f"An error occurred: {e}")
