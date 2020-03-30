#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 14:44:00 2020

@author: Zachary Miller

Working with NeuroM version 1.4.15
"""

import numpy as np
import pandas as pd

import os
import sys
import argparse

import tkinter
from tkinter import filedialog

import helper_functions as my_func

class NeuronGroup:
    def __init__(self):
        self.nrn_df_list = []
        
    def loadNeurons(self, dir_path):
    #TODO document
    
        filenames = my_func.getFilenames(dir_path)
        
        for filename in filenames:
            file_path = dir_path + '/' + filename
            nrn_df = pd.read_csv(file_path, header=None, comment='#',
                                 delim_whitespace=True)
            self.nrn_df_list.append(nrn_df)
            
    def loadNeuron(self, file_path):
        #TODO document
        
        nrn_df = pd.read_csv(file_path, header=None, comment="#",
                         delim_whitespace=True)
        self.nrn_df_list.append(nrn_df)

        

def loadNeuron(file_path):
    #TODO document
    
    # Read in the swc file as a dataframe
    nrn_df = pd.read_csv(file_path, header=None, comment="#",
                         delim_whitespace=True)
    
    return nrn_df

def loadNeurons(dir_path):
    #TODO document
    
    filenames = my_func.getFilenames(dir_path)
    nrn_df_list = []
    
    for filename in filenames:
        file_path = dir_path + '/' + filename
        nrn_df = pd.read_csv(file_path, header=None, comment='#',
                             delim_whitespace=True)
        nrn_df_list.append(nrn_df)
        
    return nrn_df_list
        
    
def getSomaLoc(nrn_df):
    """Returns the average (x,y,z) coordinate for the soma of a swc file
    
    Args:
        file_path (str): path to the swc file

    Returns:
        list: numpy array formatted as [x,y,z]
    
    """
    
    # Get all rows containing soma points and find the average of the points
    soma_rows = nrn_df.loc[nrn_df.iloc[:,1] == 1].values
    soma_point = np.mean(soma_rows, axis=0)[2:5]
    
    return soma_point

def getNeuriteTerminationPoints(file_path):
    return None

def choosePath():
    #TODO comment and document
    root = tkinter.Tk()
    root.withdraw()
    
    currdir = os.getcwd()
    chosendir = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
    if len(chosendir) > 0:
        print ("Selected Path: %s" % chosendir)
        
    return chosendir

def loadNeuronMorphometry():
    return None

def loadNeuronsMorphometry():
    return None

#%%
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--neuron_directory', required=False,
                    help='path to folder containing neuron .swc files')
    ap.add_argument('-c', '--config_file', required=False,
                    help="path to desired NeuroM config .yaml file")
    ap.add_argument('-o', '--output_file', required=False,
                    help='''path to the output file, including the file name
                    (do not include file extension)''')
    args = vars(ap.parse_args())
    
    if args['neuron_directory'] == None:
        args['neuron_directory'] = choosePath()
        
    if args['config_file'] == None:
        args['config_file'] = choosePath()
        
    if args['output_file'] == None:
        args['output_file'] = choosePath()
        
        
        
        
        