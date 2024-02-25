import os, csv

#definition of the function
def singleData():
    path = (r"dataPerCountry")
    singleCountry = input('''>> Please insert a country: ''') + ".csv"
    dataDirectory = os.listdir(path)

#Check of the string inputted

    if singleCountry in dataDirectory:

        #Reading of the file content
        with open(path + "/" + singleCountry, 'r') as fileRead:
            reader = csv.reader(fileRead)
            for row in reader:
                print(row)
    else:
        print()
        print('''
        ========================================
        |                                      |
        |         Country not found!!!         |
        |                                      |
        ========================================
         ''')
        print()