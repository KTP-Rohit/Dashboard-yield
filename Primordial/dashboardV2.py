import pyodbc
import datetime
import pandas as pd
import numpy as np
import streamlit as st

class DatabaseConnector:
    def __init__(self, connection_string):
        self.connection_string = connection_string
    
    def __enter__(self):
        self.connection = pyodbc.connect(self.connection_string)
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

class BoxDespatchSummary:
    def __init__(self, delivery_date):
        self.delivery_date = delivery_date
        self.connection_string = 'Driver={SQL Server};Server=172.20.2.4\mssql;Database=AMPSWDCPAC;Uid=rohit.avadhani;Pwd=Avadro.!994;'

    def get_data(self):
        with DatabaseConnector(self.connection_string) as connection:
            query = f"""
                SELECT CustomerNo, ProductNo, ProductName,
                       SUM(Cuts1) AS TotalCuts, SUM(Kgs) AS TotalKgs,
                       CASE WHEN SUM(Cuts1) = 0 THEN NULL ELSE SUM(Kgs)/SUM(Cuts1) END AS KgsPerCut
                FROM rep_BoxDespatchSummary
                WHERE 
                    DeliveryNo > 26310000 AND DeliveryNo < 26320000 AND
                    ProductNo > 2000 AND
                    ProductName NOT LIKE '%UNPACKED%' AND
                    DeliveryDate = '{self.delivery_date}'
                GROUP BY CustomerNo, ProductNo, ProductName
            """
            cursor = connection.cursor()
            cursor.execute(query)
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            cursor.close()
        if len(rows) > 0:
            df = pd.DataFrame.from_records(rows, columns=columns)
            df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["KgsPerCut"], how="all")
            return df
        else:
            return None
class DespatchYield:
    def __init__(self, weigh_date):
        self.weigh_date = weigh_date
        self.connection_string = 'Driver={SQL Server};Server=172.20.2.4\mssql;Database=AMPSWDCPAC;Uid=rohit.avadhani;Pwd=Avadro.!994;'

    def get_data(self):
        with DatabaseConnector(self.connection_string) as connection:
            query = f"""
                SELECT BatchNo, Cuts1, Kgs, ProductName, WeighDate
                FROM usr_DespatchYield
                WHERE 
                    WeighDate = '{self.weigh_date}' AND
                    Kgs > 0
            """
            cursor = connection.cursor()
            cursor.execute(query)
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            cursor.close()
        if len(rows) > 0:
            return pd.DataFrame.from_records(rows, columns=columns)
        else:
            return None

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
    font-size: 16px;
    line-height: 1.8;
}
</style>
""", unsafe_allow_html=True)

# Allow the user to select a delivery/weigh date
date = st.date_input("Select a date", datetime.date.today())

# Retrieve data from rep_BoxDespatchSummary table for the selected delivery/weigh date
summary = BoxDespatchSummary(date.strftime('%Y-%m-%d'))
df1 = summary.get_data()

# Retrieve data from usr_DespatchYield table for the selected delivery/weigh date
yield_summary = DespatchYield(date.strftime('%Y-%m-%d'))
df2 = yield_summary.get_data()

# Display the DataFrames using Streamlit
if df1 is not None:
    st.subheader("rep_BoxDespatchSummary")
    st.dataframe(df1)
else:
    st.write("No data found for rep_BoxDespatchSummary")

if df2 is not None:
    st.subheader("usr_DespatchYield")
    st.dataframe(df2)
else:
    st.write("No data found for usr_DespatchYield")
