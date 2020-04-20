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

import skimage as si
import skimage.io

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import read.helper_functions as my_func

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
        
        ## Get soma xyz coord
        
        ## Get mask termination point counts
        # Read in the masks
        # 
        
        # 
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
        nrn_df (DataFrame): pandas DataFrame of a swc file

    Returns:
        soma_point (array): numpy array formatted as [x,y,z]
    """
    
    # Get all rows containing soma points and find the average of the points
    soma_rows = nrn_df.loc[nrn_df.iloc[:,1] == 1].values
    print(soma_rows)
    soma_point = np.mean(soma_rows, axis=0)[2:5]
    
    return soma_point

def getNeuriteTerminationPoints(nrn_df):
    """Returns an nx3 array of the (x,y,z) coordinates for all neurite end
    points of a neuron swc file dataframe
    
    Args:
        nrn_df (DataFrame): pandas DataFrame of a swc file
        
    Returns:
        end_points (array): nx3 numpy array of point coordinates
    """
    
    # Get all parent and child nodes
    values = nrn_df.values
    sample_nums = values[:,0]
    parent_nums = values[:,6]
    
    # Find all nodes with no child and get their coordinates
    end_point_rows = np.setdiff1d(sample_nums, parent_nums)
    end_point_idxs = np.nonzero(np.in1d(sample_nums, end_point_rows))[0]
    end_points = values[end_point_idxs, 2:5]
    
    return end_points    

def getMaskPointCounts(point_arr, mask, zyx_dims):
    """Returns the number of points located in a specific mask.
    
    Args:
        point_arr (array): nx3 array of (x,y,z) coordinates
        mask (COO sparse array): sparse array of mask values
        zyx_dims (1x3 iterable): iterable of original 3d mask dimensions in 
                                 reverse order (z,y,x)
                                 
    Returns:
        point_count (int): number of points in the mask region
        
        """
    # Given an nx3 array of points and a mask, gets the count of points in the mask
    # where the mask is a scipy coo sparse matrix
    
    # Convert mask to csr and convert 3d coordinates to be compatable with
    # indexing 2d reshaped sparse array
    mask = mask.tocsr()
    coords = my_func.convertIndex(point_arr, zyx_dims)

    point_count = np.sum(mask[coords[:,0],coords[:,1]])
    
    return point_count

def getNeuriteTerminationCounts(nrn_dict, mask_dict, zyx_dims):
    """Given a dictionary of neurons, a dictionary of masks, and the [z,y,x]
    dimensions of the mask volumes, calculates the number of neurites terminating
    in each of the mask regions for every neuron, and stores into """
    #TODO document and comment
    # take in a nrn_dict and a mask_dict and find the number of termination
    # points in each part of the mask, and add that to a df
    
    # Get a dict of neurite terminations points embedded into a sparse matrix
    # this is wayyyyy to slow. Also, it looks like either I am doing something
    # wrong with pixel/real space coordinate differences. 
    
    # Create an empty dataframe
    NTC_df = pd.DataFrame(np.nan, index=list(nrn_dict.keys()),
                          columns=list(mask_dict.keys()))
    
    test_list = []
    # Get a dict of all neuron names and end points
    end_point_dict = {}
    for key in nrn_dict.keys():
        end_points = getNeuriteTerminationPoints(nrn_dict[key])
        end_points = np.around(end_points).astype(int)
        test_list.append(end_points.shape[0])
        
        # Limit indexing to the dimensions of the image so index errors are not
        # thrown for poorly registered neurons, alternatively can clean all 
        # neuron files before hand so no bad ones make it, but this may bias
        # for neurons that are not near the edges of the image
        end_points = my_func.trimIndexRange(end_points, zyx_dims)
        #print(end_points)
        
        end_point_dict.update( {key : end_points} )
        
    # Iterate over each mask and add the resulting values to a dataframe
    i=0
    #TODO use map or something to optimize this for speed
    for mask_key in mask_dict.keys():
        mask_arr = mask_dict[mask_key]
        for end_points_key in end_point_dict.keys():
            i+=1
            end_points = end_point_dict[end_points_key]
            point_count = getMaskPointCounts(end_points, mask_arr, zyx_dims)
            print(f'iteration {i}')
            #print(point_count)
            NTC_df.at[end_points_key, mask_key] = point_count
    
    return NTC_df, test_list

def plotMaskWithNeuronPoints(nrn_df, mask_path=None):
    
    if mask_path==None:
        pass
    
    else:
        # Get nonzero mask coordinates
        mask = si.io.imread(mask_path).astype(bool)
        zyx_dims = mask.shape
        z,y,x = np.where(mask==1)
        mask_coords = np.vstack( (x,y,z) ).T
        print(mask_coords)
        
        # Get proccessed neurite point coordinates
        neurite_points = getNeuriteTerminationPoints(nrn_df)
        neurite_points = np.around(neurite_points).astype(int)
        neurite_points = my_func.trimIndexRange(neurite_points, zyx_dims)
        
        all_coords = np.vstack( (mask_coords, neurite_points) )
        all_coords_num = all_coords.shape[0]
        unique_coords_num = np.unique(all_coords, axis=0).shape[0]

        total_points = all_coords_num-unique_coords_num
        
        
        
    
    return total_points

def loadTestData():
    nrn_group = NeuronGroup()
    nrn_group.loadNeurons('/home/zack/Desktop/Lab_Work/Data/neuron_morphologies/Zebrafish/aligned_040120/test_neurons')
    nrn_dict = nrn_group.nrn_dict
    nrn_dict_keys = list(nrn_dict.keys())
    mask_dict, zyx_dims = my_func.getMasksFromDir('/home/zack/Desktop/Lab_Work/Data/masks/mpin_michael_masks')
    test_df, test_list = getNeuriteTerminationCounts(nrn_dict, mask_dict, zyx_dims)
    
    return nrn_dict, nrn_dict_keys, test_df, test_list
# def testNeuronPointFunctions(mask_dir, neuron_path):
    
#     # Load a neuron group object
#     nrn_group = NeruonGroup()
#     nrn_group.loadNeurons(neuron_dir)
#     nrn_dict = nrn_group.nrn_dict
#     nrn_keys = list(nrn_dict.keys())
    
#     pass
    

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
        
        
## Notes
# Neuron projection counts are incorrect for some neurons because they are being
# truncated and moved towards the border of the image. Either I have something
# wrong with my dimensions/truncating function or the neurons are not alligned
# well
        
        
        
        