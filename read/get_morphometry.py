#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 14:44:00 2020

@author: Zachary Miller

Working with NeuroM version 1.4.15
Working with python version 3.6+
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
    """Primary object for handeling neurons"""
    
    def __init__(self):
        """Initializes an empty NeuronGroup object
        
        Args:
            None
        """
        
        # dict
        self.nrn_dict = {}
        self.morphometry_data = None
        
    def loadNeurons(self, dir_path, nrn_names=None):
        """Loads all neurons located in a directory into NeuronGroup.nrn_dict
        with key value pairs of the form {neuron name : swc file DataFrame}
        
        Args:
            dir_path (str): path to direcctory containing swc files
            nrn_names (list of strs): To be implimented later
            
        Returns:
            None
        """
        #TODO give option to specify neuron names
        
        # get all filenames
        filenames = my_func.getFilenames(dir_path)
        
        # Load all files into nrn_dict
        for filename in filenames:
            file_path = dir_path + '/' + filename
            nrn_name = os.path.splitext(filename)[0]
            nrn_df = pd.read_csv(file_path, header=None, comment='#',
                                 delim_whitespace=True)
            
            self.nrn_dict.update({nrn_name : nrn_df})
    
        return None
            
    def loadNeuron(self, file_path, nrn_name=None):
        """Load a single neuron into NeuronGroup.nrn_dict with a key value pair
        of the form {neuron name : swc file DataFrame}
        
        Args: 
            file_path (str): path to swc file to be loaded
            nrn_name (str): To be implimented later
            
        Returns:
            None"""
        #TODO give option to specify neuron name
        
        # Load neuron and add to nrn_dict
        nrn_name = os.path.splitext( os.path.basename(file_path) )[0]
        nrn_df = pd.read_csv(file_path, header=None, comment="#",
                         delim_whitespace=True)
        self.nrn_dict.update({nrn_name : nrn_df})
        
        return None
        
    def getLMeasureData():
        #TODO This should be a command that gets all of the L-measure morphometry
        # data for this NeuronGroup and returns a nice dataframe or combines
        # it by row name with an existing morphometry dataframe
        pass
    
    def getSpatialData(self, mask_dir_path, all_nrns=True, return_masks=False):
        """Gets all 'spatial' morphology measures. That is, the (xyz) coordinate
        of the soma along with the counts of how many of each neuron's neurites
        terminate each mask located in a directory. Results are put into 
        NeruonGroup.morphometry_data
        
        Args: 
            mask_dir_path (str): path to directory containing the masks
            all_nrns (bool): To be imoplimented later
            return_masks (bool): To be implimented later
            
        Returns:
            None"""
        #TODO add option to limit to a subset of neurons via a name list
        
        # Load masks
        print('Loading Masks...')
        mask_dict, zyx_dims = my_func.getMasksFromDir(mask_dir_path)
        print('Done\n')
        
        # Get soma df
        print('Finding soma points...')
        soma_df = getSomaPoints(self.nrn_dict)
        print('Done\n')
        
        # Get neurite counts for mask regions
        print('Calculating neurite termination counts by region...')
        neurite_region_count_df = getNeuriteTerminationCounts(self.nrn_dict, 
                                                              mask_dict, zyx_dims)
        print('Done\n')
        
        # Combine the data into one df
        spatial_df = pd.concat([soma_df, neurite_region_count_df], axis=1, sort=False)
        
        # Update morphometry data
        print('Updating morphometry data...')
        if self.morphometry_data == None:
            self.morphometry_data = spatial_df
            
        else:
            new_df = pd.concat([self.morphometry_data, spatial_df], axis=1, sort=False)
            self.morphometry_data = new_df
        print('Done')
            
        return None
        
    def loadExternalMorphometry():
        #TODO write a function that allows users to either set the morphometry
        # data to be an external dataframe (if morphometry_data==None) or 
        # combine the external morphometry data with the current morphometry
        # data by row name
        pass
    
    def saveMorphometryData():
        #TODO make a funciton for saving morphometry data to various file
        # formats
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
    soma_point = np.mean(soma_rows, axis=0)[2:5]
    
    return soma_point

def getSomaPoints(nrn_dict):
    """Should return a data frame of soma points for a dict of neurons"""
    #TODO document
    soma_point_dict = {}
    
    for key in nrn_dict.keys():
        nrn_df = nrn_dict[key]
        soma_point = getSomaPoint(nrn_df)
        soma_point_dict.update({key : soma_point})
        
    col_lbls = ['SomaX','SomaY','SomaZ']
    soma_point_df = pd.DataFrame.from_dict(soma_point_dict, orient='index',
                                           columns=col_lbls)
        
    return soma_point_df
    

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
    in each of the mask regions for every neuron, and stores into a dataframe
    
    Args:
        nrn_dict (dict): a dictionary of neurons
        mask_dict (dict): a dictionary of masks
        zyx_dims (array_like): an array contiaing the dimensions of the mask
                               volumes formated [z,y,x]
                               
    Returns:
        NTC_df (DataFrame): pandas DataFrame with rows being individual neurons
                            and columns being the number of neurites terminating
                            in that columns mask region
        """
    
    # Create an empty dataframe
    NTC_df = pd.DataFrame(np.nan, index=list(nrn_dict.keys()),
                          columns=list(mask_dict.keys()))
    
    # Get a dict of all neuron names and end points
    end_point_dict = {}
    for key in nrn_dict.keys():
        end_points = getNeuriteTerminationPoints(nrn_dict[key])
        end_points = np.around(end_points).astype(int)
        
        # Limit indexing to the dimensions of the image so index errors are not
        # thrown for poorly registered neurons, alternatively can clean all 
        # neuron files before hand so no bad ones make it, but this may bias
        # for neurons that are not near the edges of the image
        end_points = my_func.trimIndexRange(end_points, zyx_dims)    
        end_point_dict.update({key : end_points})
        
    # Iterate over each mask and add the resulting values to a dataframe
    #TODO use map or something to optimize this for speed
    for mask_key in mask_dict.keys():
        mask_arr = mask_dict[mask_key]

        for end_points_key in end_point_dict.keys():
            end_points = end_point_dict[end_points_key]
            point_count = getMaskPointCounts(end_points, mask_arr, zyx_dims)
            NTC_df.at[end_points_key, mask_key] = point_count
    
    return NTC_df    

#%% Functionality when run as a script
# if __name__ == '__main__':
#     ap = argparse.ArgumentParser()
#     ap.add_argument('-d', '--neuron_directory', required=False,
#                     help='path to folder containing neuron .swc files')
#     ap.add_argument('-c', '--config_file', required=False,
#                     help="path to desired NeuroM config .yaml file")
#     ap.add_argument('-o', '--output_file', required=False,
#                     help='''path to the output file, including the file name
#                     (do not include file extension)''')
#     args = vars(ap.parse_args())
    
#     if args['neuron_directory'] == None:
#         args['neuron_directory'] = my_func.choosePath()
        
#     if args['config_file'] == None:
#         args['config_file'] = my_func.choosePath()
        
#     if args['output_file'] == None:
#         args['output_file'] = my_func.choosePath()
        
        
#TODO decide on standard behavior of this file and impliment it
        
        
        