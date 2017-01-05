'''

Simulating some metrics

Created 10 October 2016

Purpose:

Simulate some stochastic data and compare different initial conditions


'''

# load the function to simulate stochastic data
import metricCalculator
cg = metricCalculator.citationSimulator()

# load the function to calculate metrics
mc = metricCalculator.metricCalculator.metricCalculator()

# load plotting capabilities from matplotlib
from matplotlib import pyplot as plt



#### variables
dataFilename = 'stochasticTest.csv'

cg.numPapers = 500 # number of papers to generate citations for
cg.p = 5.       # 'power' of article: equivalent to quality
# cg.times = np.array([0.]) # array of times at which  to sample citations

## citation related variables
mc.metricTypes = ['TR1', 'MR1']


## Simulate stochastic data
#cg.multiCitations()
#cg.saveCitations(dataFilename)

mc.citations = [[1,2,3],[3,4,5],[3,4,5]]

mc.getMetrics()

## Show as a histogram



## Calculate and display some statistics about the data

# impact factor


# MR1 metrics

# MR2 metric

# mean

# median

# 10th percentile

# 90th percentile

# h index

# minimum

# maximum


