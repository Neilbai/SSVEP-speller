# -*- coding: utf-8 -*-
"""Example program to demonstrate how to send a multi-channel time series to
LSL."""

import time
from pylsl import StreamInfo, StreamOutlet
import csv

def lsl(sourcefile, resultfile):
    info = StreamInfo('LSLOutletStreamName', 'EEG', 8, 500, 'float32', 'dummy')
    
    # next make an outlet
    outlet = StreamOutlet(info)
    
    sent_count = 0
    # run through the easy files, parse each row and send the first 8 columns per lsl stream   

    with open(sourcefile, "r") as source:
        rdr= csv.reader( source,  delimiter='\t' )
        with open(resultfile, "w", newline='\n') as result:
            wtr= csv.writer( result,  delimiter='\t' )
            for r in rdr:
                sample = [float(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4]), float(r[5]), float(r[6]), float(r[7])]
                nic2_conversion_factor = 1000.0
                sample_in_microvolt = [x / nic2_conversion_factor for x in sample]
                outlet.push_sample(sample_in_microvolt)
                time.sleep(0.001)
                sent_count = sent_count+1
                wtr.writerow( sample_in_microvolt )