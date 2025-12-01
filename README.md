# ✈️ AI Travel Itinerary Planner

A smart travel agent powered by Google's Gemini 2.0 Flash model. This application plans detailed, day-by-day travel itineraries based on your destination, dates, interests, and budget, while also checking the weather forecast to ensure your plans are feasible.

## ✨ Features

-   **AI-Powered Planning**: Uses Google Gemini 2.0 Flash to generate personalized itineraries.
-   **Weather Integration**: Automatically checks the weather for your destination using a custom tool.
-   **Structured Output**: Returns itineraries in a clean, structured JSON format (validated by Pydantic).
-   **User-Friendly Interface**: Includes a modern Streamlit web app for easy interaction.
-   **Command Line Interface**: Also supports running directly from the terminal.

> [!NOTE]
> **Mock Data**: The application currently runs on mock data for demonstration purposes due to API access restrictions.

<img width="1882" height="873" alt="Screenshot 2025-11-30 170716" src="https://github.com/user-attachments/assets/4a814838-3d12-43ba-84aa-b85a0b13a10a" />


## 🛠️ Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd A-Simple-Travel-Itinerary-Planner-Agent
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Key**:
    *   Create a `.env` file in the root directory.
    *   Add your Google API key:
        ```env
        GOOGLE_API_KEY=your_api_key_here
        ```

## 🚀 Usage

### Streamlit App (Recommended)

Run the interactive web interface:

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501` to start planning your trip!

### Command Line Interface

Run the planner directly from your terminal:

```bash
python main.py --destination "Paris" --start-date "2024-05-01" --end-date "2024-05-05" --interests "Art, Food" --budget "luxury"
```

**Arguments:**
*   `--destination`: City or country to visit.
*   `--start-date`: Start date of the trip (YYYY-MM-DD).
*   `--end-date`: End date of the trip (YYYY-MM-DD).
*   `--interests`: Comma-separated list of interests (e.g., "History, Hiking").
*   `--budget`: Budget level (`budget`, `moderate`, `luxury`).

## 📂 Project Structure

*   `app.py`: Streamlit frontend application.
*   `main.py`: CLI entry point and tool definition.
*   `agent.py`: Core logic for interacting with the Gemini model.
*   `schemas.py`: Pydantic data models for input/output validation.
*   `tools.py`: Helper functions for weather data.
*   `requirements.txt`: Python dependencies.

## 🧪 Testing

Run the unit tests to verify the agent's logic:

```bash
python test_agent.py
```
