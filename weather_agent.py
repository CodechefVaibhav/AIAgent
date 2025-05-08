## weather_agent.py

from fastapi import FastAPI, Query
from tools import tool_get_live_weather, tool_get_monthly_weather
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/weather/live")
def get_weather(city: str = Query(...)):
    logger.info(f"[Weather Agent] Received live weather request for city: {city}")
    return {"response": tool_get_live_weather(city)}

@app.get("/weather/monthly")
def get_monthly(city: str = Query(...), month: str = Query(...)):
    logger.info(f"[Weather Agent] Received monthly weather request for city: {city}, month: {month}")
    return {"response": tool_get_monthly_weather(city, month)}
