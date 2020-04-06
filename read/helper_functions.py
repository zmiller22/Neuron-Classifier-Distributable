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
from scipy import sparse

import skimage as si
import skimage.io

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

def getMasks(mask_dir_path):
    #TODO document
    
    mask_dict = {}
    original_dims = 0
    
    # Iterate over all the masks in the directory, skipping and subdirectories
    mask_dir = os.fsencode(mask_dir_path)
    for mask_file in os.listdir(mask_dir):
        filename = os.fsdecode(mask_file)
        file_path = os.path.join(mask_dir_path, filename)
        mask_name = os.path.splitext(os.path.basename(file_path))[0]
        if os.path.isdir(file_path) == False:
            
            # Read in each mask as a boolean array 
            mask = si.io.imread(file_path).astype(bool)
            dims = mask.shape
            
            # Store the mask as a sparse matrix, reshaping first if necessary
            if len(dims) == 3:
                mask = sparse.coo_matrix(mask.reshape(dims[0],-1))
                
            else: 
                print("Error: Invalid Image Dimensions")
                return None
            
            #TODO trim the file extension off of filename
            mask_dict.update( {mask_name : mask } )
            
    original_dims = dims     
    
    return mask_dict, original_dims

def choosePath():
    #TODO comment and document
    root = tkinter.Tk()
    root.withdraw()
    
    currdir = os.getcwd()
    chosendir = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
    if len(chosendir) > 0:
        print ("Selected Path: %s" % chosendir)
        
    return chosendir

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped
