import pyodbc
import datetime
import pandas as pd
import numpy as np
import streamlit as st
import time
from dependencies.database_connector import connection_string
class BoxDespatchSummary:
    def __init__(self, delivery_date,connection_string):
        self.delivery_date = delivery_date
        self.connection_string = connection_string
        self.main_words = {'RUMP','LOIN','RIB','FILLET'}
    
    def get_data(self):
        with pyodbc.connect(self.connection_string) as connection:
            query = f"""
                                SELECT DeliveryNo, ProductNo, ProductName,
                    SUM(Cuts1) AS TotalPrimalsIn, SUM(Kgs) AS TotalKgs,
                    CASE WHEN SUM(Cuts1) = 0 THEN NULL ELSE SUM(Kgs)/SUM(Cuts1) END AS KgsPerPrimal,
                    CASE 
                        WHEN ProductNo IN (2770, 2771, 2850, 2422, 2423, 2420, 2421) THEN 15 
                        WHEN ProductNo IN (2772, 2223, 2203) THEN 20
                        WHEN ProductNo IN (2530) THEN 20
                        WHEN ProductNo IN (2531) THEN 28
                        WHEN ProductNo IN (2774, 2221, 2201) THEN 10
                        WHEN ProductNo IN (2773, 2222, 2202) THEN 10
                        ELSE NULL
                    END AS CutsPerPrimal,
                    CASE WHEN SUM(Cuts1) = 0 THEN NULL ELSE SUM(Kgs)/SUM(Cuts1) END / 
                        CASE 
                            WHEN ProductNo IN (2770, 2771, 2850, 2422, 2423, 2420, 2421) THEN 15
                            WHEN ProductNo IN (2530) THEN 20
                            WHEN ProductNo IN (2531) THEN 28
                            WHEN ProductNo IN (2772, 2223, 2203) THEN 20
                            WHEN ProductNo IN (2774, 2221, 2201) THEN 10
                            WHEN ProductNo IN (2773, 2222, 2202) THEN 10
                            ELSE NULL
                        END AS KgsPerCut
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
            df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["KgsPerPrimal"], how="all")
            df["ProductNo"] = df["ProductNo"].apply(lambda x: "{:.0f}".format(x))
            df["DeliveryNo"] = df["DeliveryNo"].apply(lambda x: "{:.0f}".format(x))
            
            # Define the main words dictionary
            main_words = {"RUMP", "LOIN", "RIB", "FILLET"}
            
            # Replace product names with main words if they exist in the name
            for delivery in df["DeliveryNo"].unique():
                delivery_df = df[df["DeliveryNo"] == delivery]
                product_names = set(delivery_df["ProductName"])
                common_words = main_words.intersection(*[set(name.split()) for name in product_names])
                if len(common_words) > 0:
                    replace_word = common_words.pop()
                    df.loc[df["DeliveryNo"] == delivery, "ProductName"] = replace_word
            
            # group by delivery number
            df = df.groupby("DeliveryNo").agg({
                "ProductNo": "first",
                "ProductName": "first",
                "TotalPrimalsIn": "sum",
                "TotalKgs": "sum",
                "KgsPerPrimal": "mean",
                "CutsPerPrimal": "mean",
                "KgsPerCut": "mean"
            }).reset_index()
            return df
        else:
            return None



