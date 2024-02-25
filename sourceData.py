import pandas as pd
import mysql.connector
from io import StringIO
import requests

def updateData(conn):
    # URL CSV file
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"

    # Download CSV file
    response = requests.get(url)
    csv_data = StringIO(response.text)

    # Read CSV using pandas
    #df = pd.read_csv(csv_data)
    dtype_specification = {'tests_units': 'object'}
    df = pd.read_csv(csv_data, dtype=dtype_specification)

    # Fill NaN values in DataFrame with None
    df = df.where(pd.notna(df), None)

    print()
    print('''
        ========================================
        |                                      |
        |      Starting downloading data...    |
        |                                      |
        ========================================
     ''')

    # Create new database if it does not exist
    cursor = conn.cursor()
    create_database_query = "CREATE DATABASE IF NOT EXISTS covid19_worldData"
    cursor.execute(create_database_query)
    cursor.close()

    # Select new database
    conn.database = "covid19_worldData"

    # List tables in the database
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    cursor.close()

    # Check if table 'covid19' exists in database
    table_exists = any('covid19' in table for table in tables)

    # Create table in database MySQL if it doesn't exist
    cursor = conn.cursor()
    if not table_exists:
        create_table_query = f"""
        CREATE TABLE covid19 (
            iso_code VARCHAR(20),
            continent VARCHAR(20),
            location VARCHAR(40),
            date DATE,
            tests_units VARCHAR(20),
            {', '.join([f"{col} DECIMAL(30, 10)" for col in df.columns if col not in ['iso_code', 'continent', 'location', 'date', 'tests_units', 'total_vaccinations', 'population']])},
            population DECIMAL(30, 0),
            total_vaccinations DECIMAL(30, 10)
        )
        """
        cursor.execute(create_table_query)

    # Get the maximum number of dates in the table
    cursor.execute("SELECT MAX(date) FROM covid19")
    max_date = cursor.fetchone()[0]

    # Convert max_date to datetime.date (if not None)
    max_date = pd.to_datetime(max_date).date() if max_date is not None else None

    # Filter dataframe data based on the maximum date in the database
    if max_date is not None:
        df['date'] = pd.to_datetime(df['date']).dt.date
        df = df[df['date'] > max_date]

    for index, row in df.iterrows():
        # Convert NaN values in the row to None
        row = row.where(pd.notna(row), None)

        # Data insertion query
        columns = ', '.join([col for col in df.columns])
        values = ', '.join(['%s' for _ in range(len(df.columns))])
        insert_query = f"""
        INSERT INTO covid19 ({columns})
        VALUES ({values})
        """
        #print("Inserting row:", row)
        cursor.execute(insert_query, tuple(row))

    # Commit modifies and connection closure
    print()
    print('''
        ========================================
        |                                      |
        |     Data downloaded successfully!    |
        |                                      |
        ========================================
     ''')
    print()
    conn.commit()
    # conn.close()