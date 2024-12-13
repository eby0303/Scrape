import streamlit as st
from streamlit_option_menu import option_menu
from VillageSoul import render_village_restaurant_page
from Competitors import competitors_display


def run_apps():

    with st.sidebar:
        # Sidebar configuration
        st.title("Main Menu")

        # Options
        options = ["Village Soul of India", "Competitors"]

        # Selectbox for menu
        selected = option_menu(
            menu_title="",
            options=options,
            menu_icon="cast",
            default_index=0,
        )

    if selected == "Village Soul of India":
        render_village_restaurant_page()
    if selected == "Competitors":
        competitors_display()    
        
        
run_apps()