import pyodbc
import pandas as pd


class Giveaway:
    def __init__(self, weigh_date, connection_string):
        self.weigh_date = weigh_date
        self.connection_string = connection_string
        
   # Multiply the out cuts with the actual weight we need per primal
    def adjust_total_cuts(self, row):
        product_name = row['ProductName']
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
        else:
            return total_cuts

    # Calcualte the giveaway percent    
    def calculate_percentage(self, row):
        total_org_kgs = row['TotalOrgKgs']
        actual_out_kgs = row['Actual_Out_Kgs']
        return 100 - (actual_out_kgs / float(total_org_kgs) * 100) if total_org_kgs != 0 else 0
    
    #conditional format the percentage values
    def color_negative_red(self, value):
        if value < 0.1 or value > 5:
            color = 'red'
        else:
            color = 'green'
        return 'color: %s' % color
    
    
    def get_data(self):
        with pyodbc.connect(self.connection_string) as connection:
            query = f"""
                SELECT REPLACE(ProductNo, ',', '') AS ProductNo, ProductName, SUM(Cuts1) AS TotalCuts, SUM(OrgKgs1) AS TotalOrgKgs
                FROM rep_HourlyBoxingReportSummary
                WHERE 
                    WeighDate = '{self.weigh_date}' AND 
                    Line = '606' AND
                    ProductName != 'WEIGHT CHECK' AND
                    ProductNo IN ('2206','2226','2387','2393','2388','2394','2389','2395','1707','2779','2775','2776','2777','2478')
                GROUP BY REPLACE(ProductNo, ',', ''), ProductName
            """
            cursor = connection.cursor()
            cursor.execute(query)
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            cursor.close()
        if len(rows) > 0:
            df = pd.DataFrame.from_records(rows, columns=columns)
            # Rename columns
            df = df.rename(columns={'Cuts1': 'TotalCuts'})
            # Apply the adjust_total_cuts function to create a new column named AdjustedTotalCuts
            df['Actual_Out_Kgs'] = df.apply(self.adjust_total_cuts, axis=1)
            df['Giveaway'] = df.apply(self.calculate_percentage, axis=1)
            df = df.style.applymap(self.color_negative_red, subset=['Giveaway'])
            # Apply styling to the dataframe using pandas
            
            

            # Return the styled dataframe
            return df

        else:
            return None
