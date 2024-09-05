import pyodbc

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=tcp:easysolutions-prd.database.windows.net;'
    'DATABASE=easysolutions;'
    'UID=easysolutions;'
    'PWD=$3nh@ES#2022'
)
cursor = conn.cursor()
cursor.execute('SELECT * FROM dbo.VW_NOTA_MANUTENCAO_HH')
for row in cursor:
    print(row)
