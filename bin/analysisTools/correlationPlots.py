# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 07:36:22 2016

@author: galileo

Plot metrics resulting from two user-defined conditions against each other.

use the functions in the order:

loadData
filterData
plot



"""

from string import split
from matplotlib  import pyplot as plt
import numpy as np


class correlationPlots():
    
    def __init__(self):        
        ''' initialise some stuff '''
        
        self.datafname = '/home/galileo/Dropbox/smart laptop/impactFactor/metricMetrics/bin/results analysis/similar/similarMetrics.txt'
        
            
    def loadData(self):
        ''' load data from file into a dictionary. It should have columns: journal size, distribution, statistical parameter, metric type, metric value 
        
        function copied from analysis_variedPlots_dict '''        

        # open file and read
        f = open(self.datafname)       
        data = f.readlines()
       
        # read data into dictionary one line at a time
        self.metricData = []
        for line in data:
            vals = {}
            d = split(line)
            vals['journalSize'] = int(d[0])
            vals['distribution'] = d[1]
#            vals['distributionValue'] = float(d[2])
            vals['metric'] = d[2]  
            
            # make metric values into string
            metricVals = []
            for x in d[4:]:
                metricVals.append(float(x))
            vals['metricValue'] = metricVals
            
            # save to data list
            self.metricData.append(vals)     
            
            
            
            
    def filterData(self, *args):
        ''' Select data based on two sets of conditions. Conditions have components:

            journalSize, distribution, metric
        
        '''

        self.filteredData = []
        
        # iterate conditions
        for a in args:
            # iterate data sets
            for d in self.metricData:
                include = False
                
                # iterate journalSize, distribution, metric
                ind=0
                for val in ['journalSize', 'distribution', 'metric']:
                    if d[val]==a[ind]:
#                        print(d[val], a[ind])
                        include=True

                    else:
                        include=False
                        break
                    
                    ind = ind + 1
                    
                if include:
#                    print(d)
#                    print('\n')
                    self.filteredData.append(d)
                    
    
    def plot(self, plotName = None):
        ''' plot correlation of two data sets '''        
                
        plt.figure(figsize=(3,3))         
                
        plt.plot(self.filteredData[0]['metricValue'], self.filteredData[1]['metricValue'], 'kx')
            
        plt.xlabel(self.filteredData[0]['metric'])
        plt.ylabel(self.filteredData[1]['metric'])

        # sort out x ticks        
        xt = plt.xticks()[0]
        # round the lowest number to 1 dp
        try:
            xmin = float(str(xt[0])[0:3])
        except IndexError:
            xmin = xt[0]
        
        # get the gaps
        xgap = (xt[-1]-xmin)/5.
        # round the gap to 1dp
        xgap = np.round(xgap, decimals=1)

        # modify the x ticks
        print(xt[0], xmin)
        plt.xticks(np.arange(xmin, xt[-1], xgap))
        
        yt = plt.yticks()[0]

        try:
            ymin = float(str(yt[0])[0:3])
        except IndexError:
            xmin = yt[0]

        ygap = (yt[-1]-ymin)/5.
        ygap = np.round(ygap, decimals=1)
        plt.yticks(np.arange(ymin, yt[-1], ygap))
            
        if plotName:
            plt.tight_layout()
            plt.savefig(plotName)
                    
        
if __name__=='__main__':
    
    cp = correlationPlots()
    
    cp.datafname = '/home/galileo/Dropbox/smart laptop/impactFactor/metricMetrics/bin/results analysis/similar/similarMetrics.txt'
    cp.loadData()
    
    cond1 = (100, 'pareto', 'MR2')
    cond2 = (100, 'pareto', 'TR')    
    
    cp.filterData(cond1, cond2)
    
    print(cp.filteredData)
        
    cp.plot(plotName='pareto_100_MR1_TR.png')
    
    
    plt.show()
