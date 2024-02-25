from datetime import datetime, timedelta
import mysql.connector

def getSyntheticData(conn):
    try:
        # Connection to "covid19_worldData" database
        conn.database = "covid19_worldData"

        # Define yesterday date (YYYY-MM-DD)
        #today_date = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


        # Check if there is data for today
        check_data_query = f"""
            SELECT COUNT(new_cases)
            FROM covid19
            WHERE date = '{yesterday}' AND
                  location NOT IN (
                      'Africa', 'Asia', 'Europe', 'European Union', 'Oceania', 'International',
                      'North America', 'South America', 'World', 'High income', 'Low income',
                      'Lower middle income', 'Upper middle income'
                  )
        """
        cursor = conn.cursor()
        cursor.execute(check_data_query)
        data_count = cursor.fetchone()[0]

        if data_count == 0:
            print()
            print("No new cases available for yesterday in database.")
            print()
        else:
            countries = []

            # Find countries with the highest new_cases values
            max_new_cases_query = f"""
                SELECT location, new_cases, population
                FROM covid19
                WHERE date = '{yesterday}' AND
                      location NOT IN (
                          'Africa', 'Asia', 'Europe', 'European Union', 'Oceania', 'International',
                          'North America', 'South America', 'World', 'High income', 'Low income',
                          'Lower middle income', 'Upper middle income'
                      )
                      AND new_cases = (SELECT MAX(new_cases) FROM covid19 WHERE date = '{yesterday}'
                      AND location NOT IN (
                          'Africa', 'Asia', 'Europe', 'European Union', 'Oceania', 'International',
                          'North America', 'South America', 'World', 'High income', 'Low income',
                          'Lower middle income', 'Upper middle income'
                          )
                      )
            """
            cursor.execute(max_new_cases_query)
            max_new_cases_data = cursor.fetchall()

            for country_data in max_new_cases_data:
                country, new_cases, population = country_data
                countries.append(country)

            max_new_cases_value = max(max_new_cases_data, key=lambda x: x[1])[1]
            max_new_cases_percentage = (max_new_cases_value / max(max_new_cases_data, key=lambda x: x[2])[2]) * 100

            # Print Output Highest Values

            print()
            print(f"Here the countries with the highest number of covid-19 new cases for yesterday ({yesterday}): {', '.join(countries)}, with {int(max_new_cases_value)} new cases, corresponding to {max_new_cases_percentage:.2f}% of population.")
            print()


            # Find countries with the lowest new_cases values
            min_new_cases_query = f"""
                SELECT location, new_cases, population
                FROM covid19
                WHERE date = '{yesterday}' AND
                      location NOT IN (
                          'Africa', 'Asia', 'Europe', 'European Union', 'Oceania', 'International',
                          'North America', 'South America', 'World', 'High income', 'Low income',
                          'Lower middle income', 'Upper middle income'
                      )
                      AND new_cases = (SELECT MIN(new_cases) FROM covid19 WHERE date = '{yesterday}'
                      AND location NOT IN (
                          'Africa', 'Asia', 'Europe', 'European Union', 'Oceania', 'International',
                          'North America', 'South America', 'World', 'High income', 'Low income',
                          'Lower middle income', 'Upper middle income'
                          )
                      )
            """
            cursor.execute(min_new_cases_query)
            min_new_cases_data = cursor.fetchall()

            countries = []

            for country_data in min_new_cases_data:
                country, new_cases, population = country_data
                countries.append(country)

            min_new_cases_value = min(min_new_cases_data, key=lambda x: x[1])[1]
            min_new_cases_percentage = (min_new_cases_value / max(min_new_cases_data, key=lambda x: x[2])[2]) * 100

            # Print Output Lowest Values

            print()
            print(f"Here the countries with the lowest number of covid-19 new cases for yesterday ({yesterday}): {', '.join(countries)}, with {int(min_new_cases_value)} new cases, corresponding to {min_new_cases_percentage:.2f}% of population.")
            print()


    except Exception as e:
        print(f"Error: {e}")

    else:
        # Reset the countries list
        countries = []

        # Find the country with the highest historical total_cases
        max_total_cases_query = f"""
                    SELECT location, population, MAX(lastDate) AS max_lastDate,
                    MAX(total_cases) AS max_cases,
                    (MAX(total_cases) / population * 100) AS maxCasesPerc
                    FROM covid19
                    WHERE location NOT IN (
                        'Africa', 'Asia', 'Europe', 'European Union', 'Oceania', 'International',
                        'North America', 'South America', 'World', 'High income', 'Low income',
                        'Lower middle income', 'Upper middle income'
                    )
                    AND total_cases IS NOT NULL
                    GROUP BY location, population;
               """

        cursor.execute(max_total_cases_query)
        max_total_cases_data = cursor.fetchall()

        # Find the country with the highest historical total_cases
        max_total_cases_value = max(max_total_cases_data, key=lambda x: x[3])[3]


        for country_data in max_total_cases_data:
            country, population, lastDate, total_cases, percTotalCases = country_data
            if total_cases == max_total_cases_value:
                countries.append(country)
                histPercent = (percTotalCases)




        #max_total_cases_percentage = (max_total_cases_value / max(max_total_cases_data, key=lambda x: x[2])[2]) * 100

        # Print Output Highest Total Cases

        print()
        print(f"Here the countries with the highest historical number of covid19 cases: {str(countries)}, with {int(max_total_cases_value)} cases corresponding to {round(histPercent, 4)}% of the population.")
        print()



        countries = []

        # Find the country with the lowest historical total_cases
        minTotalCasesValue = min(max_total_cases_data, key=lambda x: x[3])[3]
        for country_data in max_total_cases_data:
            country, population, lastDate, total_cases, percTotalCases = country_data
            if total_cases == minTotalCasesValue:
                countries.append(country)
                histPercent = (percTotalCases)


        # Print Output Highest Total Cases

        print()
        print(f"Here the countries with the lowest historical number of covid19 cases: {str(countries)}, with {int(minTotalCasesValue)} cases corresponding to {round(histPercent, 4)}% of the population.")
        print()



    ###############################################################
    ###############################################################
    ###############################################################
    ###############################################################

        # Calcola il valore minimo e massimo della differenza tra "max_cases" e "value_last_month"
        min_max_difference_query = f"""
            SELECT
                location,
                MAX(lastDate) AS lastDate,
                MAX(total_cases) - MAX(total_cases_30_days_ago) AS difference
            FROM (
                SELECT
                    location,
                    lastDate,
                    total_cases,
                    LAG(total_cases, 30) OVER (PARTITION BY location ORDER BY lastDate) AS total_cases_30_days_ago
                FROM covid19
                WHERE location NOT IN (
                    'Africa', 'Asia', 'Europe', 'European Union', 'Oceania', 'International',
                    'North America', 'South America', 'World', 'High income', 'Low income',
                    'Lower middle income', 'Upper middle income'
                )
                AND total_cases IS NOT NULL
            ) AS subquery
            GROUP BY location;
        """

        cursor.execute(min_max_difference_query)
        delta30Day = cursor.fetchall()

        countries = []
        delta30d = max(delta30Day, key=lambda x: x[2])[2]
        for countryData in delta30Day:
            country, lastDate, delta = countryData
            if delta == delta30d:
                countries.append(country)


        print()
        print(f"Here the countries with the highest increment of covid data in the last month: {str(countries)}, with an increment of {int(delta30d)} total cases.")
        print()


        countries = []
        delta30d = min(delta30Day, key=lambda x: x[2])[2]
        for countryData in delta30Day:
            country, lastDate, delta = countryData
            if delta == delta30d:
                countries.append(country)


        print()
        print(f"Here the countries with the lowest increment of covid data in the last month: {str(countries)}, with an increment of {int(delta30d)} total cases.")
        print()



    #finally:
    #    cursor.close()

    ###############################################################
    ###############################################################
    ###############################################################
    ###############################################################







