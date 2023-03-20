import numpy as np
import pandas as pd

"""
Load Data from local repository
"""

scan_number = np.arange(1, 11, 1)
print(scan_number)

for scan in scan_number:
    no_Delays = pd.read_csv("Raw_Data/MoCO6_in_Pentanol.txt",
                            sep="\t", names=['Delays', 'deltaOD', 'deltaODstd'])

    raw_Data = pd.read_csv("Raw_Data/MoCO6_in_Pentanol_{}.txt".format(scan),
                            sep='\t', names=["Delay", "Wavenumber", "Delta_OD", "Delta_OD_std"])

    # Check the structure of the Dataframes
    # print(no_Delays.head())
    # print(raw_Data.head())

    """
    --- Restructure Data to get a nice map ---
    To do so, all the measurements are sorted by their delay time, this is really inconvenient for plotting.
    Therefore the dataset will be split after each delay 'block'. The first column corresponds then to the wavenumber axis.
    All of those datasets will get merged on this wavenumber axes for all delay times. As the data give always the delta_OD and its STD
    but we are only interested in the delta_OD values, the STD will be dropped.
    """

    raw_Data = raw_Data.drop(columns=['Delay'])
    raw_Data = np.array_split(raw_Data, len(no_Delays.axes[0]))
    merged_df = raw_Data[0].merge(raw_Data[1], how='right', on='Wavenumber')
    print(merged_df.head(10))

    # Loop over all dataframe fragments and merge them to the large data frame
    i = 2
    while i < len(no_Delays.axes[0]):
        merged_df = merged_df.merge(raw_Data[i], how='right', on='Wavenumber')
        i = i + 1

    # print(merged_df)
    delay_axis = list(no_Delays['Delays'])
    first_index = "Wavenumber"
    delay_axis.insert(0, first_index)
    # print(delay_axis)

    # Drop axis with STD values
    merged_df.drop(columns=['Delta_OD_std_x', 'Delta_OD_std_y', 'Delta_OD_std'], inplace=True)
    # print(merged_df)

    # Replace the wrong column names with the correct delay times
    merged_df.columns = delay_axis
    print(merged_df)

    merged_df.to_csv("Restructured_Data/MoCO6_in_Pentanol_{}.csv".format(scan), sep=";", index=False)