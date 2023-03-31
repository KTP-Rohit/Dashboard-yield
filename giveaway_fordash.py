import pyodbc
import pandas as pd


class Giveaway:
    def __init__(self,weigh_date, connection_string):
        self.weigh_date = weigh_date
        self.connection_string = connection_string
        


    def get_data(self):
        with pyodbc.connect(self.connection_string) as connection:
            query = f"""
                SELECT *
                FROM rep_HourlyBoxingReportSummary
                WHERE 
                    WeighDate = '{self.weigh_date}' AND 
                    Line = '606'

            """
            cursor = connection.cursor()
            cursor.execute(query)
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            cursor.close()
        if len(rows) > 0:
            df = pd.DataFrame.from_records(rows, columns=columns)
            return df
        else:
            return None


