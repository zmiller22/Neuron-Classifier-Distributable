#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 15:00:07 2020

@author: Zachary Miller

Contains a collection of helper functions for extracting morphometry
from .swc files.
"""

import numpy as np
import pandas as pd
import os
import tkinter
from tkinter import filedialog

def getSomaLoc(file_path):
    """Returns the average (x,y,z) coordinate for the soma of a swc file
    
    Args:
        file_path (str): path to the swc file

    Returns:
        list: list formatted as [x,y,z]
    
    """
    # Read in the swc file as a dataframe
    nrn_df = pd.read_csv(file_path, header=None, comment="#",
                         delim_whitespace=True)
    
    # Get all rows containing soma points and find the average of the points
    soma_rows = nrn_df.loc[nrn_df.iloc[:,1] == 1].values
    soma_point = np.mean(soma_rows, axis=0)[2:5]
    
    return list(soma_point)

def choosePath():
    #TODO comment and document
    root = tkinter.Tk()
    root.withdraw()
    
    currdir = os.getcwd()
    chosendir = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
    if len(chosendir) > 0:
        print ("Selected Path: %s" % chosendir)
        
    return chosendir