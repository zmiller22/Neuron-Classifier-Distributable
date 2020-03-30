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

def getFilenames(dir_path, remove_file_ext=False):
    """Returns a list of filenames within a directory
    
    Args: 
        dir_path (str): path to the directory
        remove_file_ext (boolean): option to remove the file extentions
        from the filenames (default=Fase)
        
    Returns:
        list: list containing the filenames as strings
    """
    filename_list = []
    
    dir_obj = os.fsencode(dir_path)
    for file in os.listdir(dir_obj):
        filename = os.fsdecode(file)
        if remove_file_ext: filename = os.path.splitext(filename)[0]
        
        file_path = os.path.join(dir_path, filename)
        
        if os.path.isdir(file_path) == False:
            filename_list.append(filename)
            
    return filename_list


def choosePath():
    #TODO comment and document
    root = tkinter.Tk()
    root.withdraw()
    
    currdir = os.getcwd()
    chosendir = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
    if len(chosendir) > 0:
        print ("Selected Path: %s" % chosendir)
        
    return chosendir