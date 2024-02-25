from operations import (sourceData, syntheticData, databaseUtils,  singleCountryDetail)
from databaseUtils import dbConnection, dbDisconnect


def displayMenu():
    print()
    print("[0] Exit the program")
    print("[1] Refresh source data")
    print("[2] Synthetic global report")
    print("[3] Country details")
    print()

conn = None  # initialize conn with a default value

displayMenu()
option = (input("What do you want to do: "))

while option != '0':

    # Refresh source data
    if option == '1':
        print()
        print('''
        ========================================
        |                                      |
        |      Connection to database...       |
        |                                      |
        ========================================
         ''')
        if conn == None :
            conn = dbConnection()

        sourceData.updateData(conn)


    #Synthetic global report
    elif option == '2':
        print()
        print('''
        ========================================
        |                                      |
        |     Processing... (please wait)      |
        |                                      |
        ========================================
         ''')
        print()
        if conn == None:
            conn = dbConnection()
        syntheticData.getSyntheticData(conn)

        print()


    #Country details
    elif option == '3':
        if conn == None:
            conn = dbConnection()
        singleCountryDetail.extractData(conn)


    #Countries comparison
    elif option == '4':
        print()
        print('''
        ========================================
        |                                      |
        |  Not implemented yet. Coming soon :) |
        |                                      |
        ========================================
                 ''')
        print()

    #Invalid option message
    else:
        print()
        print('''
        ========================================
        |                                      |
        |     Please choose a valid option.    |
        |                                      |
        ========================================
                 ''')
        print()
    print()
    displayMenu()
    option = (input("What do you want to do: "))


print()
dbDisconnect(conn)
print('''
        ========================================
        |                                      |
        |     Thanks for using the program     |
        |             Good bye! :D             |          
        |                                      |
        ========================================
         ''')
