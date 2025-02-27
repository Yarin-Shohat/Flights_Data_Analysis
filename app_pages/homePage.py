import streamlit as st
import pandas as pd

@st.cache_data
def get_data():
    """
    This function will only be re-run when the data is changed.
    Read
    """
    data = pd.read_csv("/workspaces/Flights_Data_Analysis/data/data.csv")
    
    return data

st.title("✈️ Flight Data Analysis")
st.write(
    """
    This is my project about flights from Israel to the world. The flights is from October 2022 to October 2024.\n
    On October 7, 2023, a terror attack in Israel led to the cancellation of all flights, significantly impacting air travel in the region. This project will explore these effects.\n
    The data, sourced from https://opensky-network.org/ via API requests, has been pre-processed by me, with all relevant code available in the repository.\n
    Both the data and the code can be found in the repository.
    """
)

st.write("Here's our first attempt at using data to create a table:")
st.write(get_data())
