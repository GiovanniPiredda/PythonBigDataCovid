import mysql.connector


# Connection from MySQL database

def dbConnection():

    retry = True
    conn = None

    while retry:
        print()
        host = input("Please enter your MySQL host: ")
        user = input("Please enter your MySQL user: ")
        password = input("Please enter your MySQL password: ")

        try:
            # Connect to MySQL
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )
            retry = False  # Exit from loop if connection succeeded
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_HOSTNAME:
                print()
                print(f">>>Unknown MySQL server host '{host}'")
                print(">>>Please check your input and try again.")
            elif "user" in str(err):
                print()
                print(f">>>Access denied for user '{user}'")
                print(">>>Please check your user/password input and try again.")
            elif err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                if "password" in str(err):
                    print()
                    print(f">>>Access denied for user '{user}' (using password: {password})")
                    print(f">>>Error message: {err.msg}")  # Print specific error message
                    print(">>>Please check your user/password input and try again.")
                else:
                    print()
                    print(f">>>Access denied: {err}")
            else:
                print(f">>>Error: {err}")

            print()
            response = input("Do you want to exit? \n"
                             "If yes, please insert 'y'\n"
                             "Otherwise database connection will restart: ")
            if response.lower() in ('y', 'yes'):
                exit()  # Terminates the program
            #retry = True
    return conn


# Disconnection from MySQL database

def dbDisconnect(conn):
    try:
        if conn.is_connected():
            conn.close()
            #print("Disconnected from MySQL database.")
    except Exception as e:
        print(f"Error during disconnection: {e}")


def isCountryAvailable(conn, singleCountry):
    conn.database = "covid19_worldData"

    checkCountryQuery = f"""
        SELECT COUNT(*) as count
        FROM covid19
        WHERE location = '{singleCountry}'
    """

    cursor = conn.cursor()
    cursor.execute(checkCountryQuery)
    result = cursor.fetchone()
    cursor.close()

    return result[0] > 0

def isDateAvailable(conn, singleCountry, date):
    conn.database = "covid19_worldData"

    checkDataQuery = f"""
        SELECT COUNT(*) as count
        FROM covid19
        WHERE date = '{date}'
    """

    cursor = conn.cursor()
    cursor.execute(checkDataQuery)
    result = cursor.fetchone()
    cursor.close()

    return result[0] > 0
