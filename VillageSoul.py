import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def render_village_restaurant_page():
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

    # Display Menu
    st.write("### Menu")
    # Load Menu from CSV
    menu_file = "Village_menu_items.csv"  # Ensure this file exists in the project directory
    try:
        menu_df = pd.read_csv(menu_file)

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
        for _, row in menu_df.iloc[start_idx:end_idx].iterrows():
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{row['Name']}**")
                    st.caption(row.get('Description', "No description available"))
                with col2:
                    st.write(f"### {row['Price']}")
                st.divider()

        # Display current page number
        st.write(f"Page {page} of {total_pages}")

        # Buttons to navigate pages below the menu items
        col1, col2 = st.columns([1, 1])
        with col1:
            prev_button = st.button("Previous Page")
            if prev_button and st.session_state.page > 1:
                st.session_state.page -= 1
        with col2:
            next_button = st.button("Next Page")
            if next_button and st.session_state.page < total_pages:
                st.session_state.page += 1
        st.info("Restaurant Details and Menu Scraped from Yelp")                 
        st.divider()
        st.divider()     
    
    except FileNotFoundError:
        st.error(f"Menu file '{menu_file}' not found. Please ensure it is available.")
    except Exception as e:
        st.error(f"An error occurred while loading the menu: {e}")

    def render_popular_times_chart():
        # Data for popular times (hours of the day and corresponding popularity percentages for each day)
        hours = ['6a', '7a', '8a', '9a', '10a', '11a', '12p', '1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p', '10p', '11p']
        # Example data for all days except Tuesday (Holiday)
        data = {
            'Monday': [0, 7, 16, 26, 27, 0, 46, 65, 81, 72, 55, 0, 0, 0, 0, 0, 0, 0],
            'Wednesday': [0, 8, 18, 28, 29, 0, 47, 66, 82, 74, 57, 0, 0, 0, 0, 0, 0, 0],
            'Thursday': [0, 6, 15, 25, 26, 0, 44, 62, 80, 70, 53, 0, 0, 0, 0, 0, 0, 0],
            'Friday': [0, 9, 17, 27, 28, 0, 48, 67, 83, 75, 58, 0, 0, 0, 0, 0, 0, 0],
            'Saturday': [0, 5, 14, 24, 25, 0, 43, 61, 79, 69, 52, 0, 0, 0, 0, 0, 0, 0],
            'Sunday': [0, 10, 20, 30, 31, 0, 49, 68, 84, 76, 59, 0, 0, 0, 0, 0, 0, 0]
        }

        # Convert the data into a DataFrame
        df = pd.DataFrame(data, index=hours)

        # Create the bar chart using Streamlit's native bar chart function
        st.bar_chart(df)
        
        st.info("Scraped from google maps")
    # Call this function in your Streamlit app to display the chart
    render_popular_times_chart()


    # Footer Section
    st.write("---")
    st.write("Powered by Streamlit | Developed with ❤️")
