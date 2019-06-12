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
labels = ['impactfactor', 'h index', 'h1', 'h10', 'information', 'random']

figureName = 'fig_IF'

## load data and plot
vsp.loadData()

## plot
ii = 0
for y in ydata:


	figureName = ' fig_same_' + labels[ii]
	vsp.plotScatter(xdata, [y], saveFig = figureName)

	ii = ii + 1
