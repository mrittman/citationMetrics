# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 17:33:09 2016

@author: galileo

Done with more sensible value for Pareto parameter

"""

import simulator_v2


ds = simulator_v2.dataSimulator() 
ds.folder = 'data 2016-03-17 varied v2_1/'
ds.n = 30000
#ds.journalSizes = [1000]
ds.journalSizes = [10, 100, 1000, 10000, 30000]
 
# ========================================================


ds.stochname = 'testCites 0-3.txt' # for input
ds.fstoch = 'stochasticCitations.txt'
ds.flognorm = 'logNormalCitations.txt'
ds.fpareto = 'paretoCitations.txt'
ds.fnormal = 'normalCitations.txt'
ds.fflat = 'flat.txt'

## for the distribution models
ds.normMean = 3.5
ds.normSigma = 1.67186077
ds.logNormSigma = 1.67186077
ds.logNormLoc = 0.34723183
ds.paretoParam = 1.25
ds.flatCitesMax = 8.

# output definitions
ds.citationLabels = ['stochastic', 'log normal', 'pareto', 'normal', 'uniform']
ds.maxCitations = 100 # max citations allowed per paper
ds.metricTypes = ['TR', 'MR1', 'MR2', 'EX1']
ds.metricsFile = 'metrics_varied_v2_1.csv'


# ========================================================


# get the data
#ds.generateCitations()
## cut off data at some limit (optional)
#ds.cutOffData()
ds.simDataFromFile()
# calculate metrics for various journal sizes
ds.getMetrics()
# save to file
ds.saveMetrics()