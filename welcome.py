## welcome.py

import streamlit as st
import re
from datetime import datetime
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def perceive_input(text):
    text = text.lower().strip()
    match = re.search(r'(?:weather|temperature|forecast).*in\s+(.+?)\s+in\s+([a-zA-Z]+)[\?\.]?', text)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    match = re.search(r'(?:weather|temperature|forecast).*in\s+([a-zA-Z\s]+)[\?\.]?', text)
    if match:
        return match.group(1).strip(), None
    match = re.search(r'\b(january|february|...|december)\b', text)
    if match:
        return None, match.group(1).strip()
    return text.strip(), None

def is_current_month(month):
    return not month or month.lower() == datetime.now().strftime('%B').lower()

def list_available_tools():
    try:
        res = requests.get("http://localhost:8100/context")
        all_nodes = res.json()
        tools = [node for node in all_nodes if node.get("type") == "tool"]

        st.sidebar.title("🔧 Tools")
        for t in tools:
            st.sidebar.markdown(f"**{t['name']}**: {t['description']}")
    except Exception as e:
        st.sidebar.error(f"Could not load tools: {e}")


def ask_weather_from_controller(city, month=None):
    try:
        tool_id = "context:tool:get_live_weather" if not month or is_current_month(
            month) else "context:tool:get_monthly_weather"
        logger.info(f"[MCP Lookup] Tool ID selected: {tool_id}")

        # Step 1: Lookup from MCP Server
        mcp_response = requests.get(f"http://localhost:8100/context/{tool_id}")
        mcp_response.raise_for_status()
        node = mcp_response.json()
        endpoint = node["content"]["endpoint"]
        method = node["content"]["method"].upper()
        logger.info(f"[MCP Resolution] Resolved endpoint: {endpoint}, method: {method}")

        # Step 2: Prepare params
        params = {"city": city}
        if tool_id == "context:tool:get_monthly_weather":
            params["month"] = month
        logger.info(f"[Tool Request] Params: {params}")

        # Step 3: Make the actual request
        if method == "GET":
            tool_response = requests.get(endpoint, params=params)
        else:
            tool_response = requests.post(endpoint, json=params)

        logger.info(f"[Tool Response] Status: {tool_response.status_code}")
        tool_response.raise_for_status()
        return tool_response.json().get("response", "⚠️ No response from tool.")

    except Exception as e:
        logger.error(f"[Error] Tool call failed: {str(e)}")
        return f"🚨 Error contacting tool via MCP: {str(e)}"


st.set_page_config(page_title="🌦️ Weather Agent", page_icon="🌤️")
st.title("🌦️ Jaane Mausam Ka Haal")

# 🔧 Show tools from MCP in sidebar
list_available_tools()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_city" not in st.session_state:
    st.session_state.last_city = None

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask me about the weather... example: How is the weather in Karachi in May?")

if user_input:
    logger.info(f"[User Input] {user_input}")
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    city, month = perceive_input(user_input)
    logger.info(f"[Perception] Parsed city: {city}, month: {month}")
    if not city and st.session_state.last_city:
        city = st.session_state.last_city

    if not city:
        response = "⚠️ Please mention a city or ask something like 'Weather in Mumbai in July'."
    else:
        st.session_state.last_city = city
        response = ask_weather_from_controller(city, month)

    safe_response = str(response)
    st.chat_message("assistant").markdown(safe_response)
    st.session_state.messages.append({"role": "assistant", "content": safe_response})