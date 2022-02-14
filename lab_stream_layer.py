# -*- coding: utf-8 -*-
"""Example program to demonstrate how to send a multi-channel time series to
LSL."""

import numpy as np
import tailer
from pylsl import StreamInfo, StreamOutlet, StreamInlet
import csv
from collections import deque
from io import StringIO
import pandas as pd

def lsl(sourcefile):
    # 8 data chanels plus 1 marker channels
    # info = StreamInfo('LSLOutletStreamName', 'EEG', 9, 500, 'float32', 'dummy')
    # next make an outlet
    # run through the easy files, parse each row and send the first 8 columns per lsl stream   
    data = []
    with open(sourcefile, "r") as source:
        # q = deque(source, num_of_lines)
        # last_lines = pd.read_csv(StringIO(''.join(q)), header=None)
        # last_lines = tailer.tail(source, num_of_lines)
        df = pd.read_csv(StringIO('\n'.join(source)), delimiter='\t', header=None)
        
        #trace back each character of your file in a loop   
        for i in range(df.shape[0]):
            # read the data[0:7] plus markers[11]
            sample = [float(df.iat[i,0]), float(df.iat[i,1]), float(df.iat[i,2]), float(df.iat[i,3]), \
                      float(df.iat[i,4]), float(df.iat[i,5]), float(df.iat[i,6]), float(df.iat[i,7])] 
            marker = [float(df.iat[i,11])]
            nic2_conversion_factor = 1000.0
            sample_in_microvolt = [x / nic2_conversion_factor for x in sample]
            sample_with_marker = sample_in_microvolt + marker
            data.append(sample_with_marker)
    data = np.array(data)
    return data



def write_marker(mkr,outlet):
    # info = StreamInfo('MarkerStream','Markers',1,0,'int32','AttentionLabels')
    # outlet = StreamOutlet(info)
    vec = []
    vec.append(mkr)
    outlet.push_sample(vec) 
    print(mkr)
    
def read_from_Enobio(stream_name, streams):
    try:
    	for i in range (len(streams)):

    		if (streams[i].name() == stream_name):
    			index = i
    			print ("NIC stream available")

    	inlet = StreamInlet(streams[index])   

    except NameError:
    	print ("Error: NIC stream not available\n\n\n")

    while True:
        sample, timestamp = inlet.pull_sample()
    return sample
