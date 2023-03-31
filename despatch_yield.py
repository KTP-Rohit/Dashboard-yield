import pyodbc
import pandas as pd


class DespatchYield:
    def __init__(self, weigh_date, connection_string):
        self.weigh_date = weigh_date
        self.connection_string = connection_string

    def get_data(self):
        with pyodbc.connect(self.connection_string) as connection:
            query = f"""
                SELECT BatchNo, Cuts1, Kgs, ProductName,
                    CASE WHEN Cuts1 = 0 THEN NULL ELSE Kgs/Cuts1 END AS KgsPerCut
                FROM usr_DespatchYield
                WHERE 
                    WeighDate = '{self.weigh_date}' AND
                    BatchNo > 26310000 AND BatchNo < 26320000 AND
                    Kgs > 0
            """
            cursor = connection.cursor()
            cursor.execute(query)
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            cursor.close()
        if len(rows) > 0:
            df = pd.DataFrame.from_records(rows, columns=columns)
            df["BatchNo"] = df["BatchNo"].apply(lambda x: "{:.0f}".format(x))
            return df
        else:
            return None

