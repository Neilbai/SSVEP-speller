# -*- coding: utf-8 -*-
"""
The cca Programs integrated in the SSVEP speller
"""
import time
import numpy as np

from canonicalca import calc_cca, read_easy

def CCA(file, savepath, SAMPLES_PER_SECOND, window_size_in_seconds):
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
    frqeucies = [12, 12.25, 12.5, 11.75]
    # freq = [np.linspace(8,16,9),
    #         np.linspace(8.25,16.25,9),
    #         np.linspace(8.5,16.5,9),
    #         np.linspace(8.75,16.75,9)]

    # freq = np.array(freq).transpose()
    # frqeucies = freq.flatten()
    CCA_result = []
    for frqeucy in frqeucies:
        
        # do the cca
        xs, result_sum, result_max, score_sum, score_max, sin = calc_cca(useful_channels, SAMPLES_PER_SECOND, frqeucy, window_size_in_seconds)
        max_value = max(result_max)
        CCA_result.append(max_value)
    tmp = max(CCA_result)
    frq_index = CCA_result.index(tmp)
    return frq_index