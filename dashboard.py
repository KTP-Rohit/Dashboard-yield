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

# Allow the user to select a delivery date
delivery_date = st.date_input("Select a delivery date", datetime.date.today())

# Retrieve data from rep_BoxDespatchSummary table for the selected delivery date
summary = BoxDespatchSummary(delivery_date.strftime('%Y-%m-%d'))
df = summary.get_data()

# Display the DataFrame using Streamlit
if df is not None:
    st.dataframe(df)
else:
    st.write("No data found for rep_BoxDespatchSummary")
