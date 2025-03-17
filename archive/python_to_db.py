import pyodbc
"exxample"

driver = "{SQL Server}"
server = "FETRI\\FETRISQL,1433;"
database = "test"
connection_string = (
    "DRIVER=" + driver +
    ";SERVER=" + server +
    ";DATABASE=" + database +
    ";Trusted_Connection=yes;" +
    "TrustServerCertificate=yes;"
)

# Connect to the database
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Insert a new row into MyTestTable (replace Column1, Column2 with your actual column names)
insert_query = """
    INSERT INTO MyTestTable (Column1, Column2)
    VALUES (?, ?)
"""
cursor.execute(insert_query, ("NewValue1", "NewValue2"))
conn.commit()

print("Row inserted successfully!")

cursor.close()
conn.close()
