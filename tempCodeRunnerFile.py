import requests
import streamlit as st

api_key = "743dd11a6e44fa1c607e5f291a56cf12"  # ⚠️ hard-coding keys is fine for learning, not for production
default_city_name = "London"
api_url = "https://api.openweathermap.org/data/2.5/weather"

def get_weather_for_city(city_name: str) -> dict:
    response = requests.get(
        api_url,
        params={"q": city_name, "appid": api_key, "units": "metric"},
        timeout=15
    )
    response.raise_for_status()
    json_data = response.json()
    return {
        "city_name": json_data.get("name", city_name),
        "temperature_celsius": json_data["main"]["temp"],
        "feels_like_celsius": json_data["main"]["feels_like"],
        "humidity_percentage": json_data["main"]["humidity"],
        "pressure_hpa": json_data["main"]["pressure"],
        "weather_main": json_data["weather"][0]["main"],
        "weather_description": json_data["weather"][0]["description"],
        "wind_speed_mps": json_data["wind"]["speed"],
    }

# ---- Streamlit UI ----
st.set_page_config(page_title="Weather (OpenWeatherMap)", layout="centered")
st.title("🌤️ Simple Weather")
city_name = st.text_input("City name", value=default_city_name)

if st.button("Fetch weather") or city_name:
    try:
        weather_info = get_weather_for_city(city_name)
        st.metric("Temperature °C", f"{weather_info['temperature_celsius']:.1f}",
                  f"Feels {weather_info['feels_like_celsius']:.1f}")
        st.write(weather_info)
    except Exception as error:
        st.error(f"Could not fetch data: {error}")
