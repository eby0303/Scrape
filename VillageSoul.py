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
        base_price = row.get('Village Price', 0)
        low_competitive_price = row.get('Low Price', 0)
        high_competitive_price = row.get('High Price', 0)

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
    try:
        menu_df = pd.read_csv(uploaded_file)
    except KeyError as e:
        st.error(f"Error in reading the file: {e}")
        return

    # Define hours
    hours = ['6 am', '7 am', '8 am', '9 am', '10 am', '11 am', '12 pm', 
             '1 pm', '2 pm', '3 pm', '4 pm', '5 pm', '6 pm', '7 pm', 
             '8 pm', '9 pm', '10 pm', '11 pm']

    # Define the data
    busy_times = {
        'Monday': [0, 0, 0, 0, 0, 7, 16, 26, 27, 0, 0, 46, 65, 81, 72, 55, 0, 0],
        'Wednesday': [0, 0, 0, 0, 0, 29, 29, 31, 25, 0, 0, 45, 78, 100, 83, 55, 0, 0],
        'Thursday': [0, 0, 0, 0, 0, 13, 25, 29, 25, 0, 0, 26, 40, 62, 58, 43, 0, 0],
        'Friday': [0, 0, 0, 0, 0, 25, 41, 40, 32, 0, 0, 34, 64, 82, 77, 53, 0, 0],
        'Saturday': [0, 0, 0, 0, 0, 25, 48, 55, 53, 0, 0, 37, 54, 72, 74, 56, 0, 0],
        'Sunday': [0, 0, 0, 0, 0, 22, 45, 63, 55, 0, 0, 49, 81, 89, 77, 46, 0, 0]
    }

    st.title("Village: The Soul of India")
    st.write("### Live Adjusted Prices")

    temp, rain = fetch_weather()
    if temp is not None:
        st.write(f"#### Current Temperature: {temp:.2f}°F")
        st.write(f"#### Weather Condition: {'Rainy/Snowy' if rain else 'Clear'}")

    busy_times_dict = {day: dict(zip(hours, values)) for day, values in busy_times.items()}

    menu_df = adjust_prices(menu_df, busy_times_dict, temp, rain)

    st.write("### Menu")
    st.dataframe(menu_df[['Name', 'Village Price', 'Low Price', 'High Price', 'Adjusted Price']])

    st.write("### Busy Times Graph")
    # Plot busy times graph
    fig, ax = plt.subplots()
    for day, values in busy_times.items():
        ax.plot(hours, values, label=day)
    ax.set_title("Busy Times per Day")
    ax.set_xlabel("Time")
    ax.set_ylabel("Busy Score")
    ax.legend()
    st.pyplot(fig)

    st.write("---")
    st.write("Powered by Streamlit | Developed with ❤️")
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
