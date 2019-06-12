#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 07:16:07 2019

@author: martyn
"""

import anl_varyingShapesPlots as fn
import numpy as np

vsp = fn.plotVaryingData()

## variables

vsp.dataFileIn = "data_sameShape.csv"
xdata = 'index'
ydata = ['impact factor', 'hindex', 'hlim1', 'hlim10', 'information', 'random\n']


## load data and plot
vsp.loadData()

## plot
figureName = ' fig_same_all'
vsp.plotScatter(xdata, ydata, saveFig = figureName)
