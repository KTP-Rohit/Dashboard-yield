import pyodbc
class DatabaseConnector:
    def __init__(self, connection_string):
        self.connection_string = connection_string
    
    def __enter__(self):
        self.connection = pyodbc.connect(self.connection_string)
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()