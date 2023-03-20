import numpy as np
import pandas as pd

"""
In this script the reformated data will get averaged and exported in userfriendly format. 
Futhermore, it gets transposed so facilitate some plotting in another script.
"""

"""
Load Data from local repository
"""

# Get the column names
restructured_Data = pd.read_csv("Restructured_Data/MoCO6_in_Pentanol_{}.csv".format(1),
                                sep=';')
column_names = restructured_Data.columns
# print(column_names)

# Load the first run into a temporary Dataframe which will be used to average the data
restructured_Data = np.genfromtxt("Restructured_Data/MoCO6_in_Pentanol_{}.csv".format(1),
                                  delimiter=';', skip_header=True)
tmp = restructured_Data

# Give the number of scans to be averaged --- Do not include 1 as it already used to generate the tmp DataFrame
scan_number = np.arange(2, 11, 1)
# print(scan_number)

# Add up the Dataframs on top of each other --> just get the sum of all measurements
for scan in scan_number:
    restructured_Data = np.genfromtxt("Restructured_Data/MoCO6_in_Pentanol_{}.csv".format(scan),
                                      delimiter=';', skip_header=True)
    tmp = tmp + restructured_Data

# Average the DataFrame
average_Data = tmp / (len(scan_number) + 1)

# Assign the correct column names for this data frame
average_Data = pd.DataFrame(average_Data, columns=column_names)
average_Data = average_Data.rename(columns={'Wavenumber': ''})

# Export the Dataframe to a .csv file
average_Data.to_csv("Averaged_Data/Averaged_Data_Mo(CO)6_in_Pentanol.csv", sep=';', index=False)

# Transpose Dataset
transposed_average_Data = average_Data.transpose()

# Export transposed Dataframe to a .csv file and drop header as this is the index and it is not relevant for futher analysis
transposed_average_Data.to_csv("Averaged_Data/Averaged_Data_transposed_Mo(CO)6_in_Pentanol.csv", sep=';', header=False)
