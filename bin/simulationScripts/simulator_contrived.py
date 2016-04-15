# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 17:38:01 2016

@author: galileo
"""

import simulator

ds = simulator.dataSimulator() 
 
# ========================================================

## variables
filename = 'bin/testCitations.csv'


# output definitions
ds.citationLabels = []

ds.journalSizes = [11]
ds.metricTypes = ['TR', 'MR1', 'MR2', 'EX1']

# outputs for metrics
ds.metricsFile = 'metricOutputsContrived.csv'


# ========================================================

## run the simulation

# get the data
ds.loadFromFile(filename)

for d in ds.citationData:
    print(d)
print(ds.citationLabels)

## calculate metrics for various journal sizes
ds.getMetrics()
## save to file
ds.saveMetrics()