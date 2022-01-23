# -*- coding: utf-8 -*-
"""Example program to demonstrate how to send a multi-channel time series to
LSL."""

import time
from random import random as rand

from pylsl import StreamInfo, StreamOutlet
import csv

# first create a new stream info (here we set the name to BioSemi,
# the content-type to EEG, 8 channels, 500 Hz, and float-valued data) The
# last value would be the serial number of the device or some other more or
# less locally unique identifier for the stream as far as available (you
# could also omit it but interrupted connections wouldn't auto-recover)
info = StreamInfo('LSLOutletStreamName', 'EEG', 8, 500, 'float32', 'dummy')

# next make an outlet
outlet = StreamOutlet(info)

sent_count = 0
# run through the easy files, parse each row and send the first 8 columns per lsl stream   
sourcefile = 'D:\\KIT\\semester_3\\research_project\\workspace\\02_EasyFile_to_LSL_Streamer\\20211203131700_E.easy' 
resultfile = 'D:\\KIT\\semester_3\\research_project\\workspace\\02_EasyFile_to_LSL_Streamer\\easy_result.csv'
with open(sourcefile, "r") as source:
    rdr= csv.reader( source,  delimiter='\t' )
    with open(resultfile, "w", newline='\n') as result:
        wtr= csv.writer( result,  delimiter='\t' )
        for r in rdr:
            sample = [float(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4]), float(r[5]), float(r[6]), float(r[7])]
            nic2_conversion_factor = 1000.0
            sample_in_microvolt = [x / nic2_conversion_factor for x in sample]
            #print(sample_in_microvolt)
            outlet.push_sample(sample_in_microvolt)
            time.sleep(0.001)
            # print(sent_count)
            sent_count = sent_count+1
            
            
            wtr.writerow( (r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]) )