'''
- manage exceptions (date not available, data wrong format, Wrong Country) ---> To-Do
'''

import pandas as pd
from tabulate import tabulate
import mysql.connector
import warnings
from operations import databaseUtils


def extractData(conn):
    # Ignora gli avvisi di tipo UserWarning durante l'esecuzione di questa funzione
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)

        conn.database = "covid19_worldData"

        #singleCountry = input('''>> Please insert a country (ex. France): ''')
        #print()

        while True:
            singleCountry = input('''\n>> Please insert a country (ex. France): ''')
            print()

            if not databaseUtils.isCountryAvailable(conn, singleCountry):
                print(f"Error: Country '{singleCountry}' does not exist in the database. \n"
                      f"Please try again remembering that the name of the country must be written in English. ")
            else:
                break
        print()


        while True:
            date = input('''(In case you want to extract data from a specific date, \ninsert the same date as the initial and final date) \n\n>> Please insert an initial date ("YYYY-MM-DD" format): ''')

                            

            if not databaseUtils.isDateAvailable(conn, singleCountry, date):
                print(f"Error: Date '{date}' is not available in the database. \n"
                      f"Please try again remembering to enter a date after 2020-01-01. \n"
                      f"Please also remember to input the date in the correct format (YYYY-MM-DD). \n")
            else:
                dateI = date
                break

        while True:
            date = input(
                '''(In case you want to extract data from a specific date, \ninsert the same date as the initial and final date) \n\n>> Please insert an initial date ("YYYY-MM-DD" format): ''')

            if not databaseUtils.isDateAvailable(conn, singleCountry, date):
                print(f"Error: Date '{date}' is not available in the database. \n"
                      f"Please try again remembering to enter a date before today. \n"
                      f"Please also remember to input the date in the correct format (YYYY-MM-DD). \n")
            else:
                dateF = date
                break

        singleCountryQuery = f"""
                SELECT *
                FROM covid19
                WHERE date BETWEEN '{dateI}' AND '{dateF}'
                AND location = '{singleCountry}'
                ORDER BY date DESC
            """

        # Dataframe Pandas Creation
        df = pd.read_sql(singleCountryQuery, conn)

        #Set no limit for data visualization
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 10000)

        # Print Dataframe
        print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))