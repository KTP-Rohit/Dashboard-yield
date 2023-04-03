import pyodbc
import datetime
import pandas as pd
import numpy as np
import streamlit as st
import time
class BoxDespatchSummary:
    def __init__(self, delivery_date,connection_string):
        self.delivery_date = delivery_date
        self.connection_string = 'Driver={SQL Server};Server=172.20.2.4\mssql;Database=AMPSWDCPAC;Uid=rohit.avadhani;Pwd=Avadro.!994;'
    
    def get_data(self):
        with pyodbc.connect(self.connection_string) as connection:
            query = f"""
                SELECT DeliveryNo, ProductNo, ProductName,
                    SUM(Cuts1) AS TotalCuts, SUM(Kgs) AS TotalKgs,
                    CASE WHEN SUM(Cuts1) = 0 THEN NULL ELSE SUM(Kgs)/SUM(Cuts1) END AS KgsPerCut,
                    CASE 
                            WHEN ProductNo IN (2770, 2771, 2850, 2422, 2423, 2420, 2421) THEN 10 
                            WHEN ProductNo IN (2772, 2223, 2203) THEN 20
                            WHEN ProductNo IN (2774, 2221, 2201) THEN 10
                            WHEN ProductNo IN (2773, 2222, 2202) THEN 10
                            ELSE NULL
                    END AS CutsPerPrimal,
                    CASE WHEN SUM(Cuts1) = 0 THEN NULL ELSE SUM(Kgs)/SUM(Cuts1) END / 
                            CASE 
                                WHEN ProductNo IN (2770, 2771, 2850, 2422, 2423, 2420, 2421) THEN 10 
                                WHEN ProductNo IN (2772, 2223, 2203) THEN 20
                                WHEN ProductNo IN (2774, 2221, 2201) THEN 10
                                WHEN ProductNo IN (2773, 2222, 2202) THEN 10
                                ELSE NULL
                            END AS KgsPerCutPerPrimal
                FROM rep_BoxDespatchSummary
                WHERE 
                    DeliveryNo > 26310000 AND DeliveryNo < 26320000 AND
                    ProductNo > 2000 AND
                    ProductName NOT LIKE '%UNPACKED%' AND
                    DeliveryDate = '{self.delivery_date}'
                GROUP BY DeliveryNo, ProductNo, ProductName
            """
            cursor = connection.cursor()
            cursor.execute(query)
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            connection.commit()
            cursor.close()
        if len(rows) > 0:
            df = pd.DataFrame.from_records(rows, columns=columns)
            df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["KgsPerCut"], how="all")
            # Remove commas from CustomerNo and BatchNo columns
            
            df["ProductNo"] = df["ProductNo"].apply(lambda x: "{:.0f}".format(x))
            df["DeliveryNo"] = df["DeliveryNo"].apply(lambda x: "{:.0f}".format(x))
            return df
        else:
            return None