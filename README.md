The connection string to the database is provided, along with Streamlit configuration settings to set the page title, page icon, layout, sidebar state, and font and layout size. The app allows the user to select a date and a table from a dropdown menu, and retrieves data from the selected table for the selected date using the appropriate class from the custom modules. The retrieved data is displayed in a DataFrame using Streamlit.

Here's a possible documentation for this code:


#Box Despatch Summary Streamlit App


This is a Streamlit app that connects to a SQL Server database and displays data from the Box Despatch Summary, Despatch Yield, or Giveaway Yield table for a selected delivery/weigh date.
Dependencies

This project relies on the following dependencies:

    pyodbc
    datetime
    pandas
    numpy
    streamlit
    dependencies.database_connector.DatabaseConnector
    dependencies.box_despatch_summary.BoxDespatchSummary
    dependencies.despatch_yield.DespatchYield
    dependencies.giveaway_fordash.Giveaway

Installation

To install the dependencies, you can use pip:

    pip install pyodbc datetime pandas numpy streamlit

Usage

To run the Streamlit app, open the command prompt, navigate to the project directory, and type:


    
    streamlit run app.py

The app will launch in your web browser. Use the date input widget to select a delivery/weigh date, and use the dropdown menu to select a table. The app will retrieve data from the selected table for the selected date and display it in a DataFrame.
Examples

Here are some examples of how to use the app:

To view the Box Despatch Summary for today, select "Box Despatch Summary" from the dropdown menu, and leave the date input widget at its default value.
To view the Despatch Yield for yesterday, select "Despatch Yield" from the dropdown menu, and change the date input widget to yesterday's date.
To view the Giveaway Yield for a specific date, select "Giveaway Yield" from the dropdown menu, and choose the desired date using the date input widget.

Troubleshooting

If you encounter any issues with the connection to the SQL Server database, check the connection string in the code and make sure it is correct.
If you encounter any issues with the custom modules from the dependencies folder, make sure they are installed and imported correctly.

Conclusion

This Streamlit app provides an easy-to-use interface for viewing data from the Box Despatch Summary, Despatch Yield, and Giveaway Yield tables in a SQL Server database. By selecting a delivery/weigh date and a table, users can quickly retrieve and analyze relevant data.
