#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 14:44:00 2020

@author: Zachary Miller

Working with NeuroM version 1.4.15
Wroking with python version 3.6+
"""

import numpy as np
import pandas as pd
from scipy import sparse

import os
import argparse
import timeit


import helper_functions as my_func

class NeuronGroup:
    def __init__(self):
        self.nrn_dict = {}
        self.morphometry_data = None
        
    def loadNeurons(self, dir_path, nrn_names=None):
    #TODO give option to specify neuron names
    #TODO document
    
        filenames = my_func.getFilenames(dir_path)
        
        for filename in filenames:
            file_path = dir_path + '/' + filename
            nrn_name = os.path.splitext(filename)[0]
            nrn_df = pd.read_csv(file_path, header=None, comment='#',
                                 delim_whitespace=True)
            self.nrn_dict.update( {nrn_name : nrn_df} )
            
    def loadNeuron(self, file_path, nrn_name=None):
        #TODO give option to specify neuron name
        #TODO document
        nrn_name = os.path.splitext(os.path.basename(file_path))[0]
        nrn_df = pd.read_csv(file_path, header=None, comment="#",
                         delim_whitespace=True)
        self.nrn_dict.update( {nrn_name : nrn_df} )
        
    def getLMeasureData():
        #TODO This should be a command that gets all of the morphometry
        # data for this NeuronGroup and returns a nice dataframe or combines
        # it by row name with an existing morphometry dataframe
        pass
    
    def getSpatialData():
        pass
        
    def loadExternalMorphometry():
        #TODO write a function that allows users to either set the morphometry
        # data to be an external dataframe (if morphometry_data==None) or 
        # combine the external morphometry data with the current morphometry
        # data by row name
        pass

        
    
def getSomaPoint(nrn_df):
    """Returns the average (x,y,z) coordinate for the soma of a neuron swc file
    dataframe
    
    Args:
        file_path (str): path to the swc file

    Returns:
        list: numpy array formatted as [x,y,z]
    
    """
    
    # Get all rows containing soma points and find the average of the points
    soma_rows = nrn_df.loc[nrn_df.iloc[:,1] == 1].values
    soma_point = np.mean(soma_rows, axis=0)[2:5]
    
    return soma_point

def getNeuriteTerminationPoints(nrn_df):
    #TODO document
    values = nrn_df.values
    sample_nums = values[:,0]
    parent_nums = values[:,6]
    
    end_point_rows = np.setdiff1d(sample_nums, parent_nums)
    end_point_idxs = np.nonzero(np.in1d(sample_nums, end_point_rows))[0]
    end_points = values[end_point_idxs, 2:5]
    
    return end_points    

def getNeuriteTerminationCounts(nrn_dict, mask_dict, dims):
    # take in a nrn_dict and a mask_dict and find the number of termination
    # points in each part of the mask, and add that to a df
    
    # Get a dict of neurite terminations points embedded into a sparse matrix
    # this is wayyyyy to slow. Also, it looks like either I am doing something
    # wrong with pixel/real space coordinate differences, or 
    end_point_img_dict = {}
    for key in nrn_dict.keys():
        #print(key)
        end_points = getNeuriteTerminationPoints(nrn_dict[key])
        end_points = np.around(end_points).astype(int)
        end_point_img = np.zeros((dims))
        print(end_points)

        #end_point_img[end_points[:,2], end_points[:,1], end_points[:,0]] += 1
            
        end_point_img = sparse.coo_matrix(end_point_img.reshape(dims[0],-1))
        end_point_img_dict.update( {key : end_point_img} )
    
    return None
    

#%% Functionality when run as a script
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
        args['neuron_directory'] = my_func.choosePath()
        
    if args['config_file'] == None:
        args['config_file'] = my_func.choosePath()
        
    if args['output_file'] == None:
        args['output_file'] = my_func.choosePath()
        
        
        
        
        