import pyodbc
import pandas as pd


class DespatchYield:
    def __init__(self, weigh_date, connection_string):
        self.weigh_date = weigh_date
        self.connection_string = connection_string
    
    def adjust_total_cuts(self, row):
        product_name = row['ProductName']
        product_number = row['ProductNo']
        total_cuts = row['TotalCuts']
        if '255G' in product_name:
            return total_cuts * 0.255
        elif 'FILLET' in product_name and '200G' not in product_name:
            return total_cuts * 0.170
        elif '340G' in product_name:
            return total_cuts * 0.340
        elif '454G' in product_name:
            return total_cuts * 0.454
        elif '200G' in product_name:
            return total_cuts * 0.200
        elif '2478' in product_number:
            return total_cuts * 0.900
        else:
            return total_cuts

    def calculate_percentage(self, row):
        total_org_kgs = row['Kgs']
        actual_out_kgs = row['Actual_Out_Kgs']
        return 100 - (actual_out_kgs / float(total_org_kgs) * 100) if total_org_kgs != 0 else 0

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

