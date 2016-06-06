# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 17:39:18 2016

@author: galileo
"""

import correlationPlots

cp = correlationPlots.correlationPlots()

# load similar data
cp.datafname = '/home/galileo/Dropbox/smart laptop/impactFactor/metricMetrics/bin/results analysis/similar/similarMetrics.txt'
cp.loadData()

folderOut = 'similarCorrelationFigs/'

# set conditions
cond1 = (100, 'pareto', 'MR2')
cond2 = (100, 'pareto', 'TR')    
cp.filterData(cond1, cond2) 
cp.plot(plotName=folderOut + 'pareto_100_MR1_TR.png')

# set conditions
cond1 = (100, 'pareto', 'EX1')
cond2 = (100, 'pareto', 'TR')    
cp.filterData(cond1, cond2) 
cp.plot(plotName=folderOut + 'pareto_100_EX_TR.png')

# set conditions
cond1 = (100, 'pareto', 'MR1')
cond2 = (100, 'pareto', 'TR')    
cp.filterData(cond1, cond2) 
cp.plot(plotName=folderOut + 'pareto_100_MR_TR.png')

# set conditions
cond1 = (100, 'pareto', 'MR1')
cond2 = (100, 'pareto', 'TR')    
cp.filterData(cond1, cond2) 
cp.plot(plotName=folderOut + 'pareto_100_MR_TR.png')


#correlationPlots.plt.show()