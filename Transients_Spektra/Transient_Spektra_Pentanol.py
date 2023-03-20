import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from matplotlib.ticker import (MultipleLocator)
from matplotlib import pylab


"""
The script uses the previously processed data to plot them as time resolved spectra.
It uses several user inputs.
1) shift the delay axis so that time zero for the pump probe experiment is actually time zero.
2) Put in the indices of delay times which should be displayed
3) Define custom plotting
"""

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ------------------------------Define layout--------------------------------------------------------
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

plt.rc('font', size=16)                     # controls default text sizes
plt.rc('axes', titlesize=16)                # font-size of the axes title
plt.rc('axes', labelsize=16)                # font-size of the x and y labels
plt.rc('axes', linewidth=2)                 # line-thickness of axes
plt.rc('xtick', labelsize=16)               # font-size of the xtick labels
plt.rc('ytick', labelsize=16)               # font-size of the tick labels
plt.rc('legend', fontsize=16)               # font-size of legend
plt.rc('figure', titlesize=14)              # font-size of the figure title
plt.rc('lines', linewidth=2)                # line-thickness
plt.rc('lines', markersize=14)              # size of markers
pylab.rcParams['xtick.major.pad'] = '10'    # increases the distance from the ticks from the respective axis
pylab.rcParams['ytick.major.pad'] = '10'    # increases the distance form the ticks from the respective axis

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ------------------------------Import Data----------------------------------------------------------
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# ++++++++++++Initialize Variables++++++++++

wavenumber = []
delays = []
Delta_mOD = []

# +++++++++Open Delay Axis and split the single strings+++++++

path = "Averaged_Data/Averaged_Data_Mo(CO)6_in_Pentanol.csv"
path_delayaxis = "Averaged_Data/Averaged_Data_transposed_Mo(CO)6_in_Pentanol.csv"

# Extract Delay Axis from Dataframe
delays = np.genfromtxt(path_delayaxis, delimiter=';')
delays = delays[:, 0]
delays = np.delete(delays, 0)

# ++++++++++++++++Convert Delay Axis to so time zero is time zero+++++++++++

convert_delay_axis = input("Do you want to want to shift the delay axis so time zero is time zero? (y/n) ")

if convert_delay_axis == 'y':
    tmp_delay_axis = delays
    time_zero = -542999.7226
    i = 0
    for element in tmp_delay_axis:
        tmp_delay_axis[i] = element - time_zero
        i = i + 1
    delays = tmp_delay_axis

# ++++++++++++++++Want to convert delay axis from fs to ps?+++++++++++++++++

convert_fs = input("Do you want to convert the delay axis from fs to ps? (y/n) ")
i = 0
if convert_fs == 'y':
    for element in delays:
        delays[i] = element / 1000
        i = i + 1

# +++++++++++Get Wavenumber axis and +++++++++

tmp = np.genfromtxt(path, delimiter=";", skip_header=True)

# ++++++++++Extract Wavenumber Axis++++++++++++++

wavenumber = tmp[:, 0]

# ++++++++++Extract Delta mOD+++++++++++++++

Delta_mOD = tmp[:, 1:]

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ------------------------------Plotting-------------------------------------------------------------
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# +++++++++++Use automatically generate colors for lines plotted+++++++++++++

colors_inverted = input('Do you want to use the inverted color sequence? (y/n) ')
if colors_inverted == "n":  # If not wanted -> False and add color manually
    colors = (
        '#0d036b', '#0d0df2', '#006ed9', '#0df2f2', '#9fdd24', '#ffdb17', 'fa8a00', '#f00500', '#ba0026', '#f00400',
        '#d90bb5')
elif colors_inverted == "y":
    colors = (
        '#ba0026', '#f00500', 'fa8a00', '#ffdb17', '#9fdd24', '#0df2f2', '#006ed9', '#0d0df2',
        '#0d036b')

# +++++++++++Define size of the plot++++++++++++++++

fig, ax = plt.subplots(figsize=(7.8, 6))  # Ratio: 1.3
ax.set_prop_cycle(color=colors)  # Colors of the plot cycle through input colors, #otherways default

# +++++++++++Define data range to be shown+++++++++++

plt.ylim(-14.0, 6.0)
plt.xlim(wavenumber[0], wavenumber[-1])

# +++++++++++Get input which time delays should be plotted+++++++++++

indices = []
index = input('Input the indices of delays you want to have plotted: ')
for elements in index:
    indices = index.split()
indices = [int(x) for x in indices]
print(indices)

# ++++++++++++++Customize Y-Axis and X-Axis Tick rate+++++++++++++++

# Custom Y-Axis Tick rate?
custom_Y_tick_rate = input('Do you want to use the custom Y-Axis Tick rate? (y/n) ')
# Custom X-Axis Tick rate?
custom_X_tick_rate = input('Do you want to use the custom X-Axis Tick rate? (y/n) ')

# ++++++++++++++Plot Time-resolved Spectra+++++++++++++++++++++++

if convert_fs == 'n':
    i = 0
    for element in indices:  # Loop over all indices given by user
        label_index = round(delays[indices[i]], 1)           # rounds the delay axis to e.g 4.4 ps
        plt.plot(wavenumber, Delta_mOD[:, indices[i]], ls="-", label=str(label_index) + " fs")
        i = i + 1
elif convert_fs == 'y':
    i = 0
    for element in indices:  # Loop over all indices given by user
        label_index = round(delays[indices[i]], 1)      # rounds the delay axis to the closest integer value
        plt.plot(wavenumber, Delta_mOD[:, indices[i]], ls="-", label=str(label_index) + " ps")
        i = i + 1

# +++++++++++++Define label and legend+++++++++++++++++++++++++++++

plt.xlabel("Wavenumber / $\mathrm{cm^{-1}}$")
plt.ylabel(r"$\Delta$mOD")
plt.legend(loc="lower right", frameon=False, labelspacing=0.4,
           labelcolor='linecolor', handletextpad=0.0, handlelength=0.0)

# ++++++++++++Define tick parameters++++++++++++++++++++++++++++++

plt.tick_params(which="major", direction='in', length=8, width=2, bottom=True, top=True, left=True, right=True)
plt.tick_params(which="minor", direction='in', length=4, width=2, bottom=True, top=True, left=True, right=True)

# ++++++++++++Locate major and minor ticks+++++++++++++++++++++++

# X-AXIS
if custom_X_tick_rate == "y":
    ax.xaxis.set_major_locator(MultipleLocator(50))
    ax.xaxis.set_minor_locator(MultipleLocator(25))
else:
    print('Using standard X-tick rate.')

# Y-AXIS
if custom_Y_tick_rate == "y":
    ax.yaxis.set_major_locator(MultipleLocator(2.0))
    ax.yaxis.set_minor_locator(MultipleLocator(1.0))
else:
    print('Using standard Y-ticks rate.')

# Define labels of ticks
plt.tick_params(labelbottom=True, labeltop=False, labelleft=True, labelright=False)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ------------------------------Show and save Plot---------------------------------------------------
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

plt.show()