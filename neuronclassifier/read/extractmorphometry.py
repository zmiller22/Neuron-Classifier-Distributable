#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 14:44:00 2020

@author: Zachary Miller
"""

import numpy as np
import os
import pandas as pd
import sys
import argparse
import functions as my_func

def extractNeuroMData(input_dir, config_file, output_file):
    #TODO add documentation
    ## Extract morphometrics with NeuroM and store in json file
    com = ('morph_stats ' + input_dir + ' -I \'SomaError\' -C ' + config_file
           +' -o ' + output_file + '.json') 
    os.system(com)
    
    ## Handle JSON file issues with Pandas and return the dataframe
    nm_df = pd.read_json(output_file + '.json', orient="index")
    
    # Unpack the column containing a dict and drop any rows containing NaN
    nm_df = nm_df.iloc[:,0].apply(pd.Series).dropna()
    
    # Check for any remaining non-numeric values
    if np.sum(~nm_df.applymap(np.isreal).values) != 0:
        print("Error: Morphometry DataFrame contains non-numeric values")
        return None
    else:
        return nm_df

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--neuron_directory", required=False,
                    help="path to folder containing neuron .swc files")
    ap.add_argument("-c", "--config_file", required=False,
                    help="path to desired NeuroM config .yaml file")
    ap.add_argument("-o", "--output_file", required=False,
                    help="path to the output file (do not include file extension)")
    args = vars(ap.parse_args())
    
    if args["neuron_directory"] == None:
        args["neuron_directory"] = my_func.choosePath()
        
    if args["config_file"] == None:
        args["config_file"] = my_func.choosePath()
        
    if args["output_file"] == None:
        #TODO find a way to let this choose a file location and name
        args["output_file"] = my_func.choosePath()
        
        
        
        
        