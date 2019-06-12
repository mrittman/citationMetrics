#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 27 19:37:13 2019

@author: martyn

Test some properties of the log normal function


"""

from numpy import *
from scipy.stats import lognorm

shape = 1
n = 1000

for x in arange(0.1, 2.5, 0.1):


	lnMean = lognorm.mean(x)

	samples = floor(lognorm.rvs(x, size = n))
	lognorm(x)
	
	print(x, lnMean, mean(samples))


