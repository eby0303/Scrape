# import streamlit as st
# import pandas as pd
# import plotly.graph_objects as go

# def render_village_restaurant_page():
#     # Restaurant Information
#     restaurant_name = "Village: The Soul of India"
#     restaurant_address = "123 Main Street, Hicksville, NY 11801"
#     opening_time = "11:00 AM"
#     closing_time = "10:00 PM"

#     # Header Section
#     st.title(f"{restaurant_name}")

#     # Restaurant Info Section
#     st.write("## Restaurant Details")
#     st.write(f"### Address: *{restaurant_address}*")
#     st.write("### Opening Hours: *11:00 AM - 3:00 PM, 5:00 PM - 10:00 PM*")

#     # Display Menu
#     st.write("### Menu")
#     # Load Menu from CSV
#     menu_file = "Village_menu_items.csv"  
#     try:
#         menu_df = pd.read_csv(menu_file)

#         # Paginated Menu Display
#         items_per_page = 10
#         total_items = len(menu_df)
#         total_pages = (total_items + items_per_page - 1) // items_per_page

#         if 'page' not in st.session_state:
#             st.session_state.page = 1

#         # Display current page
#         page = st.session_state.page
#         start_idx = (page - 1) * items_per_page
#         end_idx = start_idx + items_per_page

#         # Display Menu Items for Selected Page
#         for _, row in menu_df.iloc[start_idx:end_idx].iterrows():
#             with st.container():
#                 col1, col2 = st.columns([3, 1])
#                 with col1:
#                     st.write(f"**{row['Name']}**")
#                     st.caption(row.get('Description', "No description available"))
#                 with col2:
#                     st.write(f"### {row['Price']}")
#                 st.divider()

#         # Display current page 
#         st.write(f"Page {page} of {total_pages}")

#         col1, col2 = st.columns([1, 1])
#         with col1:
#             prev_button = st.button("Previous Page")
#             if prev_button and st.session_state.page > 1:
#                 st.session_state.page -= 1
#         with col2:
#             next_button = st.button("Next Page")
#             if next_button and st.session_state.page < total_pages:
#                 st.session_state.page += 1
#         st.info("Restaurant Details and Menu Scraped from Yelp")                 
#         st.divider()
#         st.divider()     
    
#     except FileNotFoundError:
#         st.error(f"Menu file '{menu_file}' not found. Please ensure it is available.")
#     except Exception as e:
#         st.error(f"An error occurred while loading the menu: {e}")

#     def render_popular_times_chart():
#         # Define hours
#         hours = ['6 am', '7 am', '8 am', '9 am', '10 am', '11 am', '12 pm', 
#                 '1 pm', '2 pm', '3 pm', '4 pm', '5 pm', '6 pm', '7 pm', 
#                 '8 pm', '9 pm', '10 pm', '11 pm']

#         # Define the data
#         data = {
#             'Monday': [0, 0, 0, 0, 0, 7, 16, 26, 27, 0, 0, 46, 65, 81, 72, 55, 0, 0],
#             'Wednesday': [0, 0, 0, 0, 0, 29, 29, 31, 25, 0, 0, 45, 78, 100, 83, 55, 0, 0],
#             'Thursday': [0, 0, 0, 0, 0, 13, 25, 29, 25, 0, 0, 26, 40, 62, 58, 43, 0, 0],
#             'Friday': [0, 0, 0, 0, 0, 25, 41, 40, 32, 0, 0, 34, 64, 82, 77, 53, 0, 0],
#             'Saturday': [0, 0, 0, 0, 0, 25, 48, 55, 53, 0, 0, 37, 54, 72, 74, 56, 0, 0],
#             'Sunday': [0, 0, 0, 0, 0, 22, 45, 63, 55, 0, 0, 49, 81, 89, 77, 46, 0, 0]
#         }

#         # Convert the data into a DataFrame
#         df = pd.DataFrame(data, index=hours)

#         # Ensure hours are in correct order using a categorical index
#         df.index = pd.CategoricalIndex(df.index, categories=hours, ordered=True)

#         # Sort the index (ensures it stays in order for the bar chart)
#         df = df.sort_index()

#         # Render bar chart
#         st.bar_chart(df)
#         st.info("Scraped Popularity Time from Google Maps")

#     render_popular_times_chart()



#     st.write("---")
#     st.write("Powered by Streamlit | Developed with ❤️ by eby0303")



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
    busy_threshold = 50  # ensure this is an integer

    adjusted_prices = []
    for _, row in menu_df.iterrows():
        # Remove dollar sign and spaces, then convert to float
        base_price = float(row.get('Village_Price', '0').replace('$', '').replace(' ', ''))
        low_competitive_price = float(row.get('Lowest_Price', '0').replace('$', '').replace(' ', ''))
        high_competitive_price = float(row.get('Highest_Price', '0').replace('$', '').replace(' ', ''))

        # Compare prices
        if temp < 45 or rain or busy_score > busy_threshold:
            adjusted_price = max(base_price, high_competitive_price)
        else:
            adjusted_price = min(base_price, low_competitive_price)
        adjusted_prices.append(adjusted_price)

    menu_df['Adjusted_Price'] = adjusted_prices
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

    # Restaurant Information
    restaurant_name = "Village: The Soul of India"
    restaurant_address = "123 Main Street, Hicksville, NY 11801"
    opening_time = "11:00 AM"
    closing_time = "10:00 PM"

    # Header Section
    st.title(f"{restaurant_name}")

    # Restaurant Info Section
    st.write("## Restaurant Details")
    st.write(f"### Address: *{restaurant_address}*")
    st.write("### Opening Hours: *11:00 AM - 3:00 PM, 5:00 PM - 10:00 PM*")

    temp, rain = fetch_weather()
    if temp is not None:
        st.write(f"#### Current Temperature: *{temp:.2f}°F*")
        st.write(f"#### Weather Condition: *{'Rainy/Snowy' if rain else 'Clear'}*")

    busy_times_dict = {day: dict(zip(hours, values)) for day, values in busy_times.items()}

    menu_df = adjust_prices(menu_df, busy_times_dict, temp, rain)

    # Paginated Menu Display
    items_per_page = 10
    total_items = len(menu_df)
    total_pages = (total_items + items_per_page - 1) // items_per_page

    if 'page' not in st.session_state:
        st.session_state.page = 1

    # Display current page
    page = st.session_state.page
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page

    # Display Menu Items for Selected Page
    st.write("### Live Menu")
    for _, row in menu_df.iloc[start_idx:end_idx].iterrows():
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{row['Name']}**")
                st.caption(row.get('Description', "No description available"))
            with col2:
                st.write(f"### ${row['Adjusted_Price']}")
            st.divider()

    # Display current page
    st.write(f"Page {page} of {total_pages}")

    col1, col2 = st.columns([1, 1])
    with col1:
        prev_button = st.button("Previous Page")
        if prev_button and st.session_state.page > 1:
            st.session_state.page -= 1
    with col2:
        next_button = st.button("Next Page")
        if next_button and st.session_state.page < total_pages:
            st.session_state.page += 1

    def render_popular_times_chart():
        # Define hours
        hours = ['6 am', '7 am', '8 am', '9 am', '10 am', '11 am', '12 pm', 
                '1 pm', '2 pm', '3 pm', '4 pm', '5 pm', '6 pm', '7 pm', 
                '8 pm', '9 pm', '10 pm', '11 pm']

        # Define the data
        data = {
            'Monday': [0, 0, 0, 0, 0, 7, 16, 26, 27, 0, 0, 46, 65, 81, 72, 55, 0, 0],
            'Wednesday': [0, 0, 0, 0, 0, 29, 29, 31, 25, 0, 0, 45, 78, 100, 83, 55, 0, 0],
            'Thursday': [0, 0, 0, 0, 0, 13, 25, 29, 25, 0, 0, 26, 40, 62, 58, 43, 0, 0],
            'Friday': [0, 0, 0, 0, 0, 25, 41, 40, 32, 0, 0, 34, 64, 82, 77, 53, 0, 0],
            'Saturday': [0, 0, 0, 0, 0, 25, 48, 55, 53, 0, 0, 37, 54, 72, 74, 56, 0, 0],
            'Sunday': [0, 0, 0, 0, 0, 22, 45, 63, 55, 0, 0, 49, 81, 89, 77, 46, 0, 0]
        }

        # Convert the data into a DataFrame
        df = pd.DataFrame(data, index=hours)

        # Ensure hours are in correct order using a categorical index
        df.index = pd.CategoricalIndex(df.index, categories=hours, ordered=True)

        # Sort the index (ensures it stays in order for the bar chart)
        df = df.sort_index()

        # Render bar chart
        st.bar_chart(df)
        st.info("Scraped Popularity Time from Google Maps")

    render_popular_times_chart()

    st.write("---")
    st.write("Powered by Streamlit | Developed with ❤️")

render_village_restaurant_page()
