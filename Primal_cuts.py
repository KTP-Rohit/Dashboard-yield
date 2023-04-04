import pyodbc
import pandas as pd
from dependencies.database_connector import connection_string
from dependencies.box_despatch_summary import BoxDespatchSummary
from dependencies.despatch_yield import DespatchYield
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

class PrimalCuts:
    def __init__(self, date, connection_string):
        self.date = date
        self.connection_string = connection_string
    
    def color_negative_red(self, value):
        if value < 80 or value > 100:
            color = 'red'
        else:
            color = 'green'
        return 'color: %s' % color
    
    def get_data(self):
        # Get data from BoxDespatchSummary for the selected date
        box_summary = BoxDespatchSummary(delivery_date=self.date, connection_string=self.connection_string)
        box_df = box_summary.get_data()
        
        # Get data from DespatchYield for the selected date
        despatch_yield = DespatchYield(weigh_date=self.date, connection_string=self.connection_string)
        despatch_df = despatch_yield.get_data()
        
        # Merge the two dataframes on DeliveryNo and BatchNo columns
        merged_df = pd.merge(box_df[['DeliveryNo', 'KgsPerCut']], despatch_df[['BatchNo','ProductName', 'Cuts1','Kgs']], 
                             left_on='DeliveryNo', right_on='BatchNo')
        
        # Calculate the adjusted kgs column by multiplying KgsPerCut and Cuts columns
        merged_df['Adjusted_Kgs'] = merged_df['KgsPerCut'] * merged_df['Cuts1']
        
        # Multiply cuts by factor based on product name
        merged_df.loc[merged_df['ProductName'].str.contains('X2'), 'Adjusted_Kgs'] *= 2
        merged_df.loc[merged_df['ProductName'].str.contains('X 2'), 'Adjusted_Kgs'] *= 2
        merged_df.loc[merged_df['ProductName'].str.contains('X 4'), 'Adjusted_Kgs'] *= 4
        merged_df = merged_df[merged_df['Cuts1'] >= 30]
        merged_df['primal_yield'] = 100 - (((merged_df['Adjusted_Kgs'].astype(float) - merged_df['Kgs'].astype(float)) / merged_df['Adjusted_Kgs'].astype(float)))*100
        merged_df = merged_df.style.applymap(self.color_negative_red, subset=['primal_yield'])

        return merged_df

# weigh_date = '2023-04-04'
# report = PrimalCuts(weigh_date, connection_string)

# print(report.get_data())