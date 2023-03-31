import pyodbc
import datetime
import pandas as pd
import numpy as np
import streamlit as st
import time
from database_connector import DatabaseConnector
from box_despatch_summary import BoxDespatchSummary
from despatch_yield import DespatchYield
connection_string = 'Driver={SQL Server};Server=172.20.2.4\mssql;Database=AMPSWDCPAC;Uid=rohit.avadhani;Pwd=Avadro.!994;'

# Set the page configuration

st.set_page_config(
page_title="Box Despatch Summary",
page_icon="📦",
layout="wide",
initial_sidebar_state="collapsed",
)

# Set the font and layout size
st.markdown("""
<style>
body {
    font-family: Arial, sans-serif;
    font-size: 20px;
    line-height: 1.8;
}
</style>
""", unsafe_allow_html=True)

# Allow the user to select a delivery/weigh date
date = st.date_input("Select a date", datetime.date.today(), key='date_input')

box_summary_element = st.empty()
despatch_yield_element = st.empty()

while True:
    # Retrieve data from rep_BoxDespatchSummary table for the selected delivery/weigh date
    summary = BoxDespatchSummary(date.strftime('%Y-%m-%d'),connection_string)
    df1 = summary.get_data()

    # Retrieve data from usr_DespatchYield table for the selected delivery/weigh date
    yield_summary = DespatchYield(date.strftime('%Y-%m-%d'),connection_string)
    df2 = yield_summary.get_data()



    # Display the DataFrames using Streamlit
    if df1 is not None:
        with box_summary_element:
            st.subheader("Box Despatch Summary")
            st.dataframe(df1)

    else:
        with box_summary_element:
            st.write("No data found for Box Despatch Summary")

    if df2 is not None:
        with despatch_yield_element:
            st.subheader("Despatch Yield")
            st.dataframe(df2)

    else:
        with despatch_yield_element:
            st.write("No data found for Despatch Yield")

    # Wait for 30 seconds before getting the latest data again
    time.sleep(30)

