# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 16:53:42 2022

@author: MetisVidere
"""

import pygame 
import numpy as np

from flicky import FlickyManager
from keyboard import generate_font, writePhrase
from CCA import CCA
from lab_stream_layer import lsl, write_marker, read_from_Enobio
from pylsl import StreamInfo, StreamOutlet, resolve_stream
# from keyboard import 
grid = ["ABCDEFGHI",
        "JKLMNOPQR",
        "STUVWXYZ0",
        "123456789"
        ]
phrase = "Result: " #this is used to store the string at the bottom of the interface
result = [] # to save the freq_index of each iteration, which is used to measure the correct rate 
# defines samples per second
SAMPLES_PER_SECOND = 500
# defines the window size for the cca computation
window_size_in_seconds = 3
refreshing_rate = 60
total_frames = window_size_in_seconds * refreshing_rate
waittime = 1000   #milliseconds
frames = 0  #to caculate framse
marker_number = 111111 # initial marker nunber
# saving path for bmp file
saving_file = "C:\\Users\\MetisVidere\\Desktop\\Bai_measurement\\letters\\"
# saving path for eeg data
sourcefile = 'C:\\Users\\MetisVidere\\Desktop\\Bai_measurement\\recordings\\20220208171101_lsl_test2.easy'
# saving path for cca result
savepath = 'C:/Users/MetisVidere/Desktop/Bai_measurement/'
# saving path for csv file
resultfile = 'D:\\KIT\\semester_3\\research_project\\21_12_03_SSVEP_Speller_3\\easy_result.csv'
info = StreamInfo('MarkerStream','Markers',1,0,'int32','AttentionLabels')
outlet = StreamOutlet(info)
# parameters for lab-streamig layer
End_test = False
write_marker(marker_number,outlet) # marker for begin
marker_number += 1 

while End_test==False: 

    # pygame.time.wait(3000) 
   
    write_marker(marker_number,outlet) #marker for ending
    marker_number += 1 
    # pygame.time.wait(3000)  #stop for certain milliseconds
    ############ Analysis ####################
    data = lsl(sourcefile)
    ##########################################
    frq_index, data = CCA(data, SAMPLES_PER_SECOND, 2) # determine the frequency of EEG
    # letters_to_be_typed = grid[frq_index]
    # phrase = phrase + letters_to_be_typed
    result.append(frq_index)
    #################################################
    write_marker(marker_number,outlet) # marker for begin
    marker_number += 1 
    frames = 0  

