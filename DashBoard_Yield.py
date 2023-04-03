#Added a drop down selection to choose table. 

import pyodbc
import datetime
import pandas as pd
import numpy as np
import streamlit as st
import time
from database_connector import DatabaseConnector
from box_despatch_summary import BoxDespatchSummary
from despatch_yield import DespatchYield
from giveaway_fordash import Giveaway

connection_string = 'Driver={SQL Server};Server=172.20.2.4\mssql;Database=AMPSWDCPAC;Uid=rohit.avadhani;Pwd=Avadro.!994;'

# Set the page configuration
st.set_page_config(
    page_title="Box Despatch Summary",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Set the font and layout size
# Set the font and layout size
st.markdown("""
    <style>
    table {
        font-size: 48px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)




# Allow the user to select a delivery/weigh date
date = st.date_input("Select a date", datetime.date.today(), key='date_input')

# Allow the user to select a table
# Add the table options 
#table_options = ['Box Despatch Summary', 'Despatch Yield', 'Giveaway Yield']
table_options = ['Giveaway Yield']
#Lets you add a selcet criteria for the tables
selected_table = st.selectbox('Select a table', table_options)

# Initiate empty element
table_element = st.empty()

while True:
    # Retrieve data from the selected table for the selected delivery/weigh date
    # Change made on this line: 28
    if selected_table == 'Box Despatch Summary':
        table = BoxDespatchSummary(date.strftime('%Y-%m-%d'),connection_string)
        df = table.get_data()
    elif selected_table == 'Despatch Yield':
        table = DespatchYield(date.strftime('%Y-%m-%d'),connection_string)
        df = table.get_data()
    elif selected_table == 'Giveaway Yield':
        table = Giveaway(date.strftime('%Y-%m-%d'),connection_string)
        df = table.get_data()

    # Display the DataFrame using Streamlit
    if df is not None:
        with table_element:
            st.subheader(selected_table)
            st.dataframe(df)
    else:
        with table_element:
            st.write(f"No data found for {selected_table}")

    # Wait for 30 seconds before getting the latest data again
    time.sleep(30)
