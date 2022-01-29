# -*- coding: utf-8 -*-
"""Example program to demonstrate how to send a multi-channel time series to
LSL."""

import time
from pylsl import StreamInfo, StreamOutlet
import csv

def lsl(sourcefile, resultfile):
    # 8 data chanels plus 1 marker channels
    info = StreamInfo('LSLOutletStreamName', 'EEG', 9, 500, 'float32', 'dummy')
    
    # next make an outlet
    outlet = StreamOutlet(info)
    
    sent_count = 0
    # run through the easy files, parse each row and send the first 8 columns per lsl stream   

    with open(sourcefile, "r") as source:
        rdr= csv.reader( source,  delimiter='\t' )
        with open(resultfile, "w", newline='\n') as result:
            wtr= csv.writer( result,  delimiter=',' )
            for r in rdr:
                sample = [float(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4]), float(r[5]), float(r[6]), \
                          float(r[7])] # read the data[0:7] plus markers[11]
                marker = [float(r[11])]
                nic2_conversion_factor = 1000.0
                sample_in_microvolt = [x / nic2_conversion_factor for x in sample]
                sample_with_marker = sample_in_microvolt + marker
                outlet.push_sample(sample_with_marker)
                time.sleep(0.001)
                sent_count = sent_count+1
                wtr.writerow( sample_with_marker )

def marker(mkr):
    info = StreamInfo('MyMarkerStream','Markers',1,0,'int32','myuniquesourceid23443')
    outlet = StreamOutlet(info)
    vec = []
   	# time.sleep(random.randint(0,3))
    vec.append(mkr)
    outlet.push_sample(vec) 
