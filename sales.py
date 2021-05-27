"""
This is a simplified version to show how the main parts of
the program work.

For this program to work, have these installed using pip:
    pip install openpyxl (xlrd did not work)
    pip install numpy
    pip install pandas
    pip install matplotlib
    pip install scikit-learn
    pip install sklearn

    -- also this python file needs to be in the same
        directory as the excel file (retailsales.xlsx)

Note: If the program is quit using option "5", then the sqlite
database file does not need to be manually deleted before running
the program again.
    

"""

import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from matplotlib.pyplot import figure
from sklearn.linear_model import LinearRegression
import numpy as np

# First, make sure this py file is in the same folder
# as your excel file (retailsales.xlsx is the example file)
# Panda reads the excel file:
salesdata = pd.read_excel(r"retailsales.xlsx", sheet_name='Sheet1', header=0)

# create your database file
connection = sqlite3.connect("sales.db")
cursor = connection.cursor()

# The table fields need to match the ones in the excel file
cursor.execute("""
CREATE TABLE sales (
    Year INTEGER,
    USRetailSalesMil INTEGER,
    RetailNetIncomeMil INTEGER)""")

# Put excel data into database file
salesdata.to_sql('sales', connection, if_exists='append', index=False)

continueProgram = 'y'

# Menu
while (continueProgram == 'y'):
    print("Welcome to the Retail Sales Queryer")
    print("1. Display Retail Sales Data in the US")
    print("2. Display Graph of Retail Sales Data in the US")
    print("3. Quit")

    userInput = input("Please enter a menu item (eg 1): ")


    # Display retail sales
    if userInput == "1":
        print()
        print("Displaying US Retail Sales in Millions")

        con = sqlite3.connect("sales.db")
        cur = con.cursor()

        records = cur.execute("""SELECT Year, USRetailSalesMil, RetailNetIncomeMil FROM sales""")

        # Print table header
        print("{:12s}{:12s}{:12s}".format("Year", "Sales", "Net Income"))

        # Print table data
        for record in records:
            print("{:<12d}{:<12d}{:<12d}".format(record[0], record[1], record[2]))

        print()

    # Display graph of sales
    if userInput == "2":
        print()
        print("Creating graph of US Retail Sales")


        # fetch data to create graph
        records = cursor.execute(""" SELECT Year, USRetailSalesMil FROM sales """)

        # create empty lists that will be filled with the data
        year = []
        sales = []

        for record in records:
            year.append(record[0])
            sales.append(record[1])

        x = np.array(year)
        y = np.array(sales)

        # Calculate linear regression
        X = x[:, np.newaxis]
        model = LinearRegression(normalize=True)
        model.fit(X,y)
        coeff = model.coef_

        # Creating graph
        Data = {'Year': year, 'USRetailSalesMil': sales}
        title = "US Retail Sales Mil, Linear Reg Coeff: " + str(coeff)
        
        df = pd.DataFrame(Data, columns=['Year', 'USRetailSalesMil'])
        plt.figure(figsize=(8,8))
        plt.plot(df['Year'], df['USRetailSalesMil'], color='orange', marker = 'x')
        plt.title(title, fontsize=14)
        plt.xlabel('Year', fontsize=14)
        plt.ylabel('US Retail Sales Mil (1 x 10^6)', fontsize=14)
        plt.grid(True)
        plt.show()

        print()

    # Quit
    if userInput == "3":
        cursor.execute("""DROP TABLE sales""")
        print()
        print("DB deleted. Goodbye!")
        continueProgram = 'n'
