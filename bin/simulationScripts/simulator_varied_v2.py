# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 17:38:01 2016

@author: galileo
"""

import simulator_v2
import numpy as np

ds = simulator_v2.dataSimulator() 
 
# ========================================================

## variables

dataFolder = '/home/galileo/Dropbox/smart laptop/impactFactor/citationSimulator/bin/varied citations_2016-03-02/data/'

# output definitions
ds.citationLabels = []

ds.journalSizes = [100]
#ds.metricTypes = ['TR', 'MR1', 'MR2', 'EX1']
#ds.maxCitations = 500

# outputs for metrics
ds.folder = 'analysisOutput/'
ds.metricsFile = 'metricOutputsVaried.csv'

#ds.n = 100

#normMeans = np.arange(1., 10.1, 1.)
#ds.normSigma = 1.5
#logNormLocs = np.arange(0.2, 4.6, 0.2)
#ds.logNormSigma = 1.5
#paretoVals = np.arange(0., 3.1, 0.5)
#paretoVals[0] = 0.01
#flatMaxs = np.arange(5., 50.1, 5.)


# ========================================================
  
ds.simDataFromFolder(dataFolder)
# calculate metrics for various journal sizes
ds.getMetrics()
# save to file
ds.saveMetrics()