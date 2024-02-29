This is a program for the analysis of worldwide data related to covid-19.

The "our world in data" organization (https://ourworldindata.org/; now referred to as the "organization") 
provides daily data on covid-19 virus cases for all countries that are members of the organization.

The program was written entirely in Python.

The program aims to create and use a database with MySQL that replicates the report provided by the organization. 
Such a database will be stored locally.

The program is a more streamlined version of the project called "ProjectBigDataCovid_MVP", 
which instead of creating a database, was intended to download the .csv file provided by the organization and create one csv file per country, 
so that the original information would be divided into many other csv files.

The program currently has 3 different functions that can be consulted through a menu that will respond to the following inputs:

    - 0 close the program.
    - 1 create/update the database.
    - 2 Get a synthetic overview on the whole world (regarding new daily cases, historical cases, previous month total cases increment).
    - 3 Get data about a specific country in a specific time frame.

Prerequisites:

In order to use the program you must have python installed on your machine 
with the following libraries/modules: "pandas", "datatime", "tabulate", "mysql.connector", "io", "requests".

You will also need to have MySQL installed on your device with an active local instance. 
The connection data to the MySQL server (host, user, password) will be required by the program itself.
