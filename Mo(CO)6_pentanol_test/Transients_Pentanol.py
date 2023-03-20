import numpy as np
import matplotlib.pyplot as plt

from matplotlib.ticker import (MultipleLocator)
from matplotlib import pylab

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ------------------------------Define layout--------------------------------------------------------
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

plt.rc('font', size=16)  # controls default text sizes
plt.rc('axes', titlesize=16)  # font-size of the axes title
plt.rc('axes', labelsize=16)  # font-size of the x and y labels
plt.rc('axes', linewidth=2)  # line-thickness of axes
plt.rc('xtick', labelsize=16)  # font-size of the xtick labels
plt.rc('ytick', labelsize=16)  # font-size of the tick labels
plt.rc('legend', fontsize=16)  # font-size of legend
plt.rc('figure', titlesize=14)  # font-size of the figure title
plt.rc('lines', linewidth=2)  # line-thickness
plt.rc('lines', markersize=6)  # size of markers
pylab.rcParams['xtick.major.pad'] = '10'  # increases the distance from the ticks from the respective axis
pylab.rcParams['ytick.major.pad'] = '10'  # increases the distance form the ticks from the respective axis

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ------------------------------Import Data----------------------------------------------------------
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# ++++++++++++Initialize Variables++++++++++

wavenumber = []
delays = []
Delta_mOD = []

# +++++++++Open Delay Axis and split the single strings+++++++
path = "Processed_Data/Mo(CO)6_in_Pentanol_averaged.csv"
path_delayaxis = "Processed_Data/MoCO6_in_Pentanol_Time_Axis.txt"

delays = np.genfromtxt(path_delayaxis)

# ++++++++++++++++Convert Delay Axis to so zero is zero+++++++++++

convert_delay_axis = input("Do you want to want to shift the delay axis so zero is zero? (y/n) ")

if convert_delay_axis == 'y':
    tmp_delay_axis = delays
    time_zero = -542999.7226
    i = 0
    for element in tmp_delay_axis:
        tmp_delay_axis[i] = element - time_zero
        i = i + 1
    delays = tmp_delay_axis

# Check if Delays were correctly loaded
# print(delays)

# ++++++++++++++++Want to convert delay axis from fs to ps?+++++++++++++++++

convert_fs = input("Do you want to convert the delay axis from fs to ps? (y/n) ")
i = 0
if convert_fs == 'y':
    for element in delays:
        delays[i] = element / 1000
        i = i + 1
    # print(delays)

# +++++++++++Get Time axis and DeltaOD+++++++++

tmp = np.genfromtxt(path, delimiter=',')
# Drop header
if True:
    tmp = np.delete(tmp, 0, axis=0)

# print(tmp)

# ++++++++++Extract Delay Axis++++++++++++++

wavenumber = tmp[:, 0]
# print(wavenumber[:5])      # Shows the first 5 elements of this array

# ++++++++++Extract Delta mOD+++++++++++++++

Delta_mOD = tmp[:, 1:]
# print(Delta_mOD)

# print(len(Delta_mOD[0,:]))

# ++++++++Remove every second column++++++++
odd_numbers = np.arange(1, 351, 2)  # Arange an array with all the odd columns which contain the errors
# print(odd_numbers)

Delta_mOD_error_removed = np.delete(Delta_mOD, odd_numbers, axis=1)
# print(Delta_mOD_error_removed)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ------------------------------Plotting-------------------------------------------------------------
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# +++++++++++Use automatically generate colors for lines plotted+++++++++++++

colors_inverted = input('Do you want to use the inverted color sequence? (y/n) ')
if colors_inverted == "n":  # If not wanted -> False and add color manually
    colors = (
        'blue', 'red', 'lime', 'orange')
elif colors_inverted == "y":
    colors = (
        'orange', 'lime', 'red', 'blue')

# +++++++++++Define size of the plot++++++++++++++++

fig, ax = plt.subplots(figsize=(7.8, 6))  # Ratio: 1.3
ax.set_prop_cycle(color=colors)  # Colors of the plot cycle through input colors, #otherways default

# +++++++++++Define data range to be shown+++++++++++

plt.ylim(-2.5, 7.5)
plt.xlim(-157, 1550)

# +++++++++++Get input which time delays should be plotted+++++++++++

indices = []
index = input('Input the indices of wavenumbers you want to have plotted: ')
for elements in index:
    indices = index.split()
indices = [int(x) for x in indices]
print(indices)

# ++++++++++++++Customize Y-Axis and X-Axis Tick rate+++++++++++++++

# Custom Y-Axis Tick rate?
custom_Y_tick_rate = input('Do you want to use the custom Y-Axis Tick rate? (y/n) ')
# Custom X-Axis Tick rate?
custom_X_tick_rate = input('Do you want to use the custom X-Axis Tick rate? (y/n) ')

# ++++++++++++++Plot Transients+++++++++++++++++++++++

if convert_fs == 'n':
    i = 0
    for element in indices:  # Loop over all indices given by user
        label_index = round(wavenumber[indices[i]])  # rounds the delay axis to the closest integer value
        plt.plot(delays, Delta_mOD_error_removed[indices[i], :], 'o', mfc='none',
                 label=str(label_index) + " $\mathrm{cm^{-1}}$")
        i = i + 1
elif convert_fs == 'y':
    i = 0
    for element in indices:  # Loop over all indices given by user
        label_index = round(wavenumber[indices[i]])  # rounds the delay axis to the closest integer value
        plt.plot(delays, Delta_mOD_error_removed[indices[i], :], 'o', mfc='none',
                 label=str(label_index) + " $\mathrm{cm^{-1}}$")
        i = i + 1

# +++++++++++++Define label and legend+++++++++++++++++++++++++++++

if convert_fs == 'n':
    plt.xlabel("Delay / fs")
elif convert_fs == 'y':
    plt.xlabel("Delay / ps")
plt.ylabel(r"$\Delta$mOD")
plt.legend(loc="lower right", frameon=False, labelspacing=0.4,
           labelcolor='linecolor', handletextpad=1.0, handlelength=0.0)

# ++++++++++++Define tick parameters++++++++++++++++++++++++++++++

plt.tick_params(which="major", direction='in', length=8, width=2, bottom=True, top=True, left=True, right=True)
plt.tick_params(which="minor", direction='in', length=4, width=2, bottom=True, top=True, left=True, right=True)

# ++++++++++++Locate major and minor ticks+++++++++++++++++++++++

# X-AXIS
if custom_X_tick_rate == "y":
    ax.xaxis.set_major_locator(MultipleLocator(250))
    ax.xaxis.set_minor_locator(MultipleLocator(125))
else:
    print('Using standard X-tick rate.')

# Y-AXIS
if custom_Y_tick_rate == "y":
    ax.yaxis.set_major_locator(MultipleLocator(2.5))
    ax.yaxis.set_minor_locator(MultipleLocator(1.25))
else:
    print('Using standard Y-ticks rate.')

# Define labels of ticks
plt.tick_params(labelbottom=True, labeltop=False, labelleft=True, labelright=False)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ------------------------------Show and save Plot---------------------------------------------------
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


plt.show()
