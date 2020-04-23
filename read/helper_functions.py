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
        filename_list (list): list containing the filenames as strings
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

def getMasksFromDir(mask_dir_path):
    """Loads all the masks in the given directory into sparse arrays
    and returns them as a dict along with their dimensions
    
    Args: 
        mask_dir_path (str): path to directory containing masks
        
    Returns:
        mask_dict (dict): dict containing mask name : sparse mask pairs
        original_dims (array): array of the mask dimensions formatted [z,y,x]
    """
    
    mask_dict = {}
    original_dims = 0
    
    # Iterate over all the masks in the directory, skipping any subdirectories
    mask_dir = os.fsencode(mask_dir_path)
    for mask_file in os.listdir(mask_dir):
        filename = os.fsdecode(mask_file)
        file_path = os.path.join(mask_dir_path, filename)
        mask_name = os.path.splitext(os.path.basename(file_path))[0]
        if os.path.isdir(file_path) == False:
            
            # Read in each mask as a boolean array 
            mask = si.io.imread(file_path).astype(bool)
            if original_dims==0:
                original_dims = mask.shape
            
            # Reshape the mask into a 2d array and save as a sparse array
            mask = sparse.coo_matrix(mask.reshape(mask.shape[0],-1))
            mask_dict.update({mask_name : mask})
    
    return mask_dict, original_dims

def trimIndexRange(coord, zyx_dims):
    """Given a nx3 array of indices and an array of [z,y,x] dimensions, trim
    the indices such that all are in a valid range according to the dimensions
    
    Args:
        coord (array): nx3 array with rows being 3d array indices
        zyx_dims (array_like): array of dimensions formatted [z,y,x]
        
    Returns:
        coord (array): idx_array trimmed to be in valid range"""
    
    # Get the dimensions in [x,y,z] order
    idx_cap = zyx_dims[::-1]
    
    # Rescale all high elements
    for i in range(coord.shape[1]):
        cap = idx_cap[i]
        coord[ coord[:,i]>=cap ] = cap-1
        # high_idxs = array[:,i]>=cap
        # array[high_idxs,i] = cap-1
    
    # Rescale all low elements    
    coord[coord<0] = 0
    
    return coord

def convertIndex(coord, zyx_dims):
    """Given nx3 array of 3d [x,y,z] coordinates, converts to be compatable
    with 2d sparse arrays reshaped from 3d arrays with dimensions [z,y,x]
    
    Args:
        coord (array): nx3 array of 3d coordinates
        zyx_dims (array_like): array of dimensions formatted [z,y,x]
        
    Returns: 
        new_coord (array): 2d coordinate that indexes the same value as the 
                           original 3d coordinate in the 2d sparse array
        """

    # Check if this is one coordinate or multiple and perform the conversion
    # accordingly
    if len(coord.shape) == 1:
        new_coord = np.array([ coord[2], coord[1]+zyx_dims[2]+coord[0] ]).T
        
    elif len(coord.shape) == 2:
        new_coord = np.array([ coord[:,2], coord[:,1]*zyx_dims[2]+coord[:,0] ]).T
    
    else: return None
    
    return new_coord
        

def choosePath():
    #TODO comment and document
    root = tkinter.Tk()
    root.withdraw()
    
    currdir = os.getcwd()
    chosendir = filedialog.askdirectory(parent=root, initialdir=currdir, 
                                        title='Please select a directory')
    if len(chosendir) > 0:
        print ("Selected Path: %s" % chosendir)
        
    return chosendir

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

def testPointCounts(mask, point_arr):
    vector = mask[point_arr[:,2],point_arr[:,1],point_arr[:,0]]
    
    return np.sum(vector)
        
        
