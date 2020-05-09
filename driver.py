#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 20:41:54 2020

@author: Zachary Miller
"""

import read.get_morphometry as read

NRN_PATH = '/home/zack/Desktop/Lab_Work/Data/neuron_morphologies/Zebrafish/aligned_040120/MPIN Neurons_z_brain'
MASK_PATH = '/home/zack/Desktop/Lab_Work/Data/masks/zbrain_mece_masks'
OUT_PATH = '/home/zack/Desktop/Lab_Work/Data/neuron_morphologies/Zebrafish/aligned_040120/zbrain_spatial_morphology.csv'

#%% Load test data

# Load test neurons
nrn_group = read.NeuronGroup()
nrn_group.loadNeurons(NRN_PATH, has_header=True)
nrn_group.getSpatialData(MASK_PATH)

nrn_group.morphometry_data.to_csv(OUT_PATH)
