#NOTE DI DEBUG: PARE CI SIA UN PROBLEMA NELLA REFERENZA DELLE CARTELLE.
#CAMBIARE REFERENZE CON I NUOVI PATH, CONSIDERANDO CHE SI CARICHERÁ IN GITHUB
#

from operations import sourceData, syntheticData, singleCountryDetail



def displayMenu():
    print()
    print("[0] Exit the program")
    print("[1] Refresh source data")
    print("[2] Synthetic global report")
    print("[3] Country details")
    print()

displayMenu()
option = int(input("What do you want to do: "))

while option != 0:

    #Refresh source data
    if option == 1:
        print()
        print('''
        ========================================
        |                                      |
        |      Starting downloading data...    |
        |                                      |
        ========================================
         ''')
        sourceData.updateData()
        print()
        print('''
        ========================================
        |                                      |
        |     Data downloaded successfully!    |
        |                                      |
        ========================================
         ''')
        print()

    #Synthetic global report
    elif option == 2:
        print()
        print('''
        ========================================
        |                                      |
        |     Processing... (please wait)      |
        |                                      |
        ========================================
         ''')
        print()
        syntheticData.getSyntheticData()
        print()
        print()

    #Country details
    elif option == 3:
        #print("Not implemented yet. Coming soon :)")
        singleCountryDetail.singleData()


    #Countries comparison
    elif option == 4:
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
    option = int(input("What do you want to do: "))

print("Thanks for using the program.\nGood bye! :D")