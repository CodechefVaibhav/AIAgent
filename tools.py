## tools.py

import requests
from datetime import datetime
from collections import Counter
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OPENWEATHER_KEY = "YOURTOKEN"
VISUALCROSSING_KEY = "YOURTOKEN"

def tool_get_live_weather(city):
    try:
        logger.info(f"[Live Weather] Fetching weather for: {city}")
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {'q': city, 'appid': OPENWEATHER_KEY, 'units': 'metric'}
        response = requests.get(url, params=params)
        data = response.json()

        if "main" not in data:
            return f"Could not fetch current weather for '{city.title()}'."

        temp = data['main']['temp']
        condition = data['weather'][0]['description']
        logger.info(f"[Live Weather] Temp: {temp}°C, Condition: {condition}")
        return f"🌤️ The current temperature in {city.title()} is {temp}°C with {condition}."
    except Exception as e:
        return f"Error: {str(e)}"

def tool_get_monthly_weather(city, month):
    try:
        logger.info(f"[Monthly Weather] Fetching weather for: {city} in {month}")
        month_number = datetime.strptime(month[:3], '%b').month
        start_date = f"2023-{month_number:02d}-01"
        end_date = f"2023-{month_number:02d}-28"

        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{start_date}/{end_date}"
        params = {'unitGroup': 'metric', 'key': VISUALCROSSING_KEY, 'include': 'days', 'contentType': 'json'}
        response = requests.get(url, params=params)
        data = response.json()
        days = data.get('days', [])
        if not days:
            return f"No historical data for {city.title()} in {month.title()}."

        avg_temp = sum(day['temp'] for day in days) / len(days)
        conditions = [day['conditions'] for day in days if 'conditions' in day]
        most_common = Counter(conditions).most_common(1)[0][0] if conditions else "unknown"
        logger.info(f"[Monthly Weather] Avg Temp: {avg_temp:.1f}, Common: {most_common}")

        return f"In {month.title()}, the average temperature in {city.title()} was {avg_temp:.1f}°C with mostly {most_common.lower()} conditions."
    except Exception as e:
        return f"Error fetching monthly weather: {str(e)}"
