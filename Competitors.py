import streamlit as st
import pandas as pd

def competitors_display():

    village_menu = pd.read_csv("menu_price_comparison2.csv")
    menu_files = ["Chennai_menu_items_comparison.csv", "Hillside_menu_items_comparison.csv", 
                "House_menu_items_comparison.csv", "Taste_menu_items_comparison.csv", 
                "World_menu_items_comparison.csv"]

    restaurant_links = {
        "Chennai Dosas": "https://www.yelp.com/biz/chennai-dosas-hicksville?osq=Indian+Vegetarian",
        "Hillside Dosa Hut": "https://www.yelp.com/biz/hillside-dosa-hutt-glen-oaks",
        "Taste Of Chennai": "https://www.yelp.com/biz/taste-of-chennai-hicksville?osq=Indian+Vegetarian",
        "Dosa World": "https://www.yelp.com/menu/dosa-world-hicksville-2?osq=Indian+Vegetarian",
        "House of Dosa": "https://www.yelp.com/menu/house-of-dosas-hicksville?osq=Indian+Vegetarian"
    }

    st.title("Main Menu - Village: The Soul of India")

   
    village_table = village_menu[['Name', 'Description', 'Village_Price', 'Highest_Price', 'Lowest_Price', 'Comparison_Status']]
    st.write("### Village: The Soul of India Menu")
    st.dataframe(village_table, height=300, use_container_width=True)



 
    for menu_file in menu_files:
        comparative_menu = pd.read_csv(menu_file)
        menu_name = menu_file.split("_")[0] 
        
       
        full_name = {
            "Chennai": "Chennai Dosas",
            "Hillside": "Hillside Dosa Hut",
            "House": "House of Dosa",
            "Taste": "Taste Of Chennai",
            "World": "Dosa World"
        }.get(menu_name, "Unknown Restaurant")
        
        # Display the restaurant's full name
        st.markdown(f"### {full_name}")

        # Display the comparative table for the restaurant
        comparative_table = comparative_menu[['Name', 'Description_Village', 'Price_Village', 
                                            f'Description_{menu_name}_menu_items.csv', 
                                            f'Price_{menu_name}_menu_items.csv', 
                                            f'Price_Difference_{menu_name}_menu_items.csv']]
        st.dataframe(comparative_table, height=300, use_container_width=True)

        # Display Yelp link below the table
        st.link_button(f"Visit {full_name} on Yelp", restaurant_links[full_name])

