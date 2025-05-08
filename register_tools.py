## register_tools.py

import requests

MCP_SERVER = "http://localhost:8100/register"

## TOOLS are the NODES

tools = [
    {
        "id": "context:tool:get_live_weather",
        "type": "tool",
        "name": "Live Weather",
        "description": "Provides live weather for a given city using OpenWeatherMap.",
        "content": {
            "endpoint": "http://localhost:8000/weather/live",
            "method": "GET",
            "params": {"city": "City name"}
        }
    },
    {
        "id": "context:tool:get_monthly_weather",
        "type": "tool",
        "name": "Monthly Weather",
        "description": "Provides average monthly weather for a city using VisualCrossing.",
        "content": {
            "endpoint": "http://localhost:8000/weather/monthly",
            "method": "GET",
            "params": {"city": "City name", "month": "Month"}
        }
    }
]

for tool in tools:
    response = requests.post(MCP_SERVER, json=tool)
    print(response.status_code, response.json())