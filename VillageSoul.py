import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import matplotlib.pyplot as plt

# OpenWeather API configuration
OPENWEATHER_API_KEY = "af8065e15aff4259be0ac375e7316f11"
VILLAGE_LOCATION = {"lat": 40.7683, "lon": -73.5251}  # Hicksville, NY

def fetch_weather():
    url = ("https://api.openweathermap.org/data/2.5/weather?lat="
           f"{VILLAGE_LOCATION['lat']}&lon={VILLAGE_LOCATION['lon']}&appid={OPENWEATHER_API_KEY}")
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        temp_k = weather_data['main']['temp']
        temp_f = (temp_k - 273.15) * 9/5 + 32
        rain = weather_data.get('weather', [{}])[0].get('main', '').lower() in ['rain', 'snow']
        return temp_f, rain
    else:
        st.error("Error fetching weather data")
        return None, None

def adjust_prices(menu_df, busy_times, temp, rain):
    current_time = datetime.now().strftime("%I %p").lower()
    current_day = datetime.now().strftime("%A")

    busy_score = busy_times.get(current_day, {}).get(current_time, 0)
    busy_threshold = 50
    
    adjusted_prices = []
    for _, row in menu_df.iterrows():
        base_price = row['Village Price']
        low_competitive_price = row['Low Price']
        high_competitive_price = row['High Price']

        if temp < 45 or rain or busy_score > busy_threshold:
            adjusted_price = max(base_price, high_competitive_price)
        else:
            adjusted_price = min(base_price, low_competitive_price)
        adjusted_prices.append(adjusted_price)
    menu_df['Adjusted Price'] = adjusted_prices
    return menu_df

def render_village_restaurant_page():
    # Load data from uploaded file
    uploaded_file = "menu_price_comparison2.csv"
    menu_df = pd.read_csv(uploaded_file)

    busy_times = {
        'Monday': {"12 pm": 46, "1 pm": 65, "2 pm": 81, "3 pm": 72, "4 pm": 55},
        'Wednesday': {"12 pm": 45, "1 pm": 78, "2 pm": 100, "3 pm": 83, "4 pm": 55},
        # Add more days as needed
    }

    st.title("Village: The Soul of India")
    st.write("### Live Adjusted Prices")

    temp, rain = fetch_weather()
    if temp is not None:
        st.write(f"#### Current Temperature: {temp:.2f}°F")
        st.write(f"#### Weather Condition: {'Rainy/Snowy' if rain else 'Clear'}")

    menu_df = adjust_prices(menu_df, busy_times, temp, rain)

    st.write("### Menu")
    st.dataframe(menu_df[['Name', 'Village Price', 'Low Price', 'High Price', 'Adjusted Price']])

    st.write("### Busy Times Graph")
    # Plot busy times graph
    fig, ax = plt.subplots()
    for day, times in busy_times.items():
        ax.plot(times.keys(), times.values(), label=day)
    ax.set_title("Busy Times per Day")
    ax.set_xlabel("Time")
    ax.set_ylabel("Busy Score")
    ax.legend()
    st.pyplot(fig)

    st.write("---")
    st.write("Powered by Streamlit | Developed with ❤️")

render_village_restaurant_page()
