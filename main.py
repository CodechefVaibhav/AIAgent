## main.py

import requests

def ask_weather(city, month=None):
    if month:
        response = requests.get("http://localhost:8000/weather/monthly", params={"city": city, "month": month})
    else:
        response = requests.get("http://localhost:8000/weather/live", params={"city": city})
    return response.json()

if __name__ == "__main__":
    print("********************Welcome to MCP Controller")
    city = input("City? ")
    month = input("Month (leave empty for current)? ")

    result = ask_weather(city, month if month else None)
    print("\U0001F449", result['response'])