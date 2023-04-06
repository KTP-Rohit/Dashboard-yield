import pyodbc
import datetime
import pandas as pd
import numpy as np
import streamlit as st
import time
from dependencies.database_connector import connection_string
from dependencies.box_despatch_summary import BoxDespatchSummary
from dependencies.despatch_yield import DespatchYield
from dependencies.giveaway_fordash import Giveaway
from Primal_cuts import PrimalCuts


# Set the page configuration
st.set_page_config(
    page_title="Yield Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Set the font and layout size
st.markdown("""
    <style>
    body {
        font-size: 0.2em;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)


#Adding Title
# Set the page title
st.title("Yield and Giveaway Dashs")
# Allow the user to select a date
date = st.date_input("Select a date", datetime.date.today(), key='date_input')

# Allow the user to select a table
table_options = ['Box Despatch Summary', 'Despatch Yield', 'Giveaway Yield', 'Primal Cuts']
selected_table = st.selectbox('Select a table', table_options)

# Create an empty placeholder element
table_element = st.empty()

# Add a checkbox to allow user to manually refresh data
manual_refresh = st.checkbox('Manual Refresh', key='manual_refresh')

while True:
    # Retrieve data from the selected table for the selected date
    if selected_table == 'Box Despatch Summary':
        table = BoxDespatchSummary(delivery_date=date.strftime('%Y-%m-%d'), connection_string=connection_string)
        df = table.get_data()
    elif selected_table == 'Despatch Yield':
        table = DespatchYield(weigh_date=date.strftime('%Y-%m-%d'), connection_string=connection_string)
        df = table.get_data()
        # Filter out rows with 'VL' in the ProductName column
        df = df[~df['ProductName'].str.contains('VL', na=False)]
    elif selected_table == 'Giveaway Yield':
        table = Giveaway(date.strftime('%Y-%m-%d'), connection_string=connection_string)
        df = table.get_data()
    elif selected_table == 'Primal Cuts':
        table = PrimalCuts(date.strftime('%Y-%m-%d'), connection_string=connection_string)
        df = table.get_data()

   # Set the font size
    font_size = 20

    if df is not None:
        with table_element:
            st.subheader(selected_table)
            # Apply a custom CSS style to the subheader element
            st.markdown(f"<p style='font-size:{font_size}px'>{selected_table}</p>", unsafe_allow_html=True)
            st.dataframe(df, width=2000, height=500)
    else:
        with table_element:
            st.write(f"No data found for {selected_table}")
            # Apply a custom CSS style to the write element
            st.markdown(f"<p style='font-size:{font_size}px'>No data found for {selected_table}</p>", unsafe_allow_html=True)


    # Wait for 30 seconds before getting the latest data again
    time.sleep(30)
