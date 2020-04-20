#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 18:23:20 2020

@author: zack
"""

import read.get_morphometry as read
import read.helper_functions as read_funcs

TEST_NRN_PATH = 'test_data/test_neurons'
TEST_MASK_PATH = 'test_data/test_masks_(michael_MPIN)'

#%% Load test data

# Load test neurons
test_nrns = read.NeuronGroup()
test_nrns.loadNeurons(TEST_NRN_PATH)
test_nrn_dict = test_nrns.nrn_dict

# Load test masks
test_mask_dict, test_dims = read_funcs.getMasksFromDir(TEST_MASK_PATH)

#%% Test functions on the loaded data 
test_soma_df = read.getSomaPoints(test_nrn_dict)
test_neurite_counts_df = read.getNeuriteTerminationCounts(test_nrn_dict, test_mask_dict,
                                                 test_dims)

