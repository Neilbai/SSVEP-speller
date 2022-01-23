"""
Example CCA-from Marius
"""

import time
import numpy as np
import os
import glob
import csv
import matplotlib.pyplot as plt

from canonicalca import calc_cca
# from trca import trca

# Info.
# / is the path separator on Unix and Unix-like systems.
# Modern Windows can generally use both \ and / interchangeably for filepaths,
# but Microsoft has advocated for the use of \ as the path separator for decades.
# rootdir = 'D:/KIT/semester_3/research_project/21_12_03_SSVEP_Speller_2/recordings/group1'
# # filepaths = os.getcwd() + '/*.easy'  #return the current directory 
# filepaths = os.path.dirname(rootdir) + '/*.easy'
# filelist = glob.glob(filepaths)     #get all easyfiles
file = 'D:/KIT/semester_3/research_project/workspace/03_CCA_analysis/database/21_12_03_SSVEP_Speller_2/recordings/20211203131851_N.easy'
savepath = 'D:/KIT/semester_3/research_project/workspace/03_CCA_analysis/database/21_12_03_SSVEP_Speller_2/result/N_32/'
if not os.path.exists(savepath):
    os.mkdir(savepath)
# defines samples per second
SAMPLES_PER_SECOND = 500
# defines the window size for the cca computation
window_size_in_seconds = 4;


# function for reading the csv file into a numpy array
def read_easy(file):
    with open(file) as csv_file:
        values = np.array(list(csv.reader(csv_file, delimiter='\t')))
        print('Read file and found values with shape:', values.shape)
    return values


# run this for every file in the loop
# for file in filelist:

    # read data and convert to float values
data = read_easy(file)
data = data.astype('float64')

# find markers and note where they are not zero
marker_channel = data[:, 11]
marker = np.where(marker_channel != 0)[0][1:-1]

# clip eeg channels of used electrodes
useful_channels = data[:, [0, 1, 2, 3, 4, 5, 6, 7]]
# frqeucies = [12, 12.25, 12.5, 11.75]
freq = [np.linspace(8,16,9),
        np.linspace(8.25,16.25,9),
        np.linspace(8.5,16.5,9),
        np.linspace(8.75,16.75,9)]
freq = np.array(freq).transpose()
frqeucies = freq.flatten()

for frqeucy in frqeucies:
    
    # do the cca
    xs, result_sum, result_max, score_sum, score_max, sin = calc_cca(useful_channels, SAMPLES_PER_SECOND, frqeucy, amount_of_sec=window_size_in_seconds)
    
    # plot the wanted results
    """
    The CCA signal gets shifted by the window size of the CCA because that's
    the time when the result of the CCA was computed. With this shift we can 
    plot the marker at their original position in the CCA-plot.
    """
    window_size_in_samples = window_size_in_seconds * SAMPLES_PER_SECOND
    plt.plot(xs+window_size_in_samples, result_max)
    plt.ylim(0, 1.0)
    plt.title('Result max'+ str(frqeucy))

    #plot all markers
    # for m in marker:
    #     plt.axvline(x=m, color='red')
        
    # plot result
    # plt.show()
    
    ## save under the same path and name, but as an svg
    plt.save = file[:-5]
    plt.savefig(savepath+ 'pltsave' + str(frqeucy) + '.svg', format='svg', dpi=1200)

    # clear the plot for next iterration
    plt.clf()
