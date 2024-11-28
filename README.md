# Weather Dashboard

A beautiful GUI-based weather application that displays current weather and 5-day forecast using the OpenWeatherMap API.

## Features

- Current weather display with temperature, description, and humidity
- 5-day weather forecast
- Weather condition icons
- Clean and modern user interface
- Error handling for invalid city names

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Get an API key from [OpenWeatherMap](https://openweathermap.org/api):
   - Sign up for a free account
   - Navigate to your API keys section
   - Copy your API key

3. Replace the API key in `weather_app.py`:
```python
self.api_key = "YOUR_API_KEY"  # Replace with your actual API key
```

4. Run the application:
```bash
python weather_app.py
```

## Usage

1. Enter a city name in the search box
2. Click the "Search" button or press Enter
3. View the current weather and 5-day forecast

## Dependencies

- Python 3.x
- tkinter (included with Python)
- requests
- Pillow (PIL)
