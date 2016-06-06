# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 16:47:38 2016

@author: galileo

make plots of metric against statistical parameter for various metrics and distributions

"""

import pandas as ps
from matplotlib import pyplot as plt
#import matplotlib.rcParams as pltParams
import numpy as np
import scipy as sc
from string import split


class plotMarker():
    
    def __init__(self):
        ''' initialise stuff '''
        
        a = 1
        self.inputfile = ''
        
    
    def loadData(self):
        ''' load data from file into a dictionary. It should have columns: journal size, distribution, statistical parameter, metric type, metric value '''        

        # open file and read
        f = open(self.inputfile)       
        data = f.readlines()
       
        # read data into dictionary one line at a time
        self.metricData = []
        for line in data:
            vals = {}
            d = split(line)
            vals['journalSize'] = int(d[0])
            vals['distribution'] = d[1]
            vals['distributionValue'] = float(d[2])
            vals['metric'] = d[3]  
            
            # make metric values into string
            metricVals = []
            for x in d[4:]:
                metricVals.append(float(x))
            vals['metricValue'] = metricVals
            
            # save to data list
            self.metricData.append(vals)
        
        
        
        
    def filterData(self, filterOptions):
        ''' filter by a dictionary
        columns are: journalSize, distribution, metric, metricValue

        e.g. filterOptions = {'metric':'MR1', 'distribution':'flat'}
             pm.filterData(filterOptions)
        
        
        '''
        
        data = self.metricData
        for f in filterOptions:
            dataTemp = []
            
            for d in data:
                if d[f] == filterOptions[f]:
                    dataTemp.append(d)
            
            data = dataTemp[:]
        
        
        self.filteredData = data
        for f in self.filteredData:
            print(f)
        
        print(self.filteredData)
            
    def plotData(self, title, style='gx', newFig = True):
        ''' plot filtered Data '''
        
        if newFig:
            plt.figure()
        
        # plot one point at a time (probably a better way to do this)        
        for f in self.filteredData:
            y = f['metricValue']
            x = [f['distributionValue']]*len(y)
            plt.plot(x, y, style)
        
        # standardize the y limits for comparison
        if plt.ylim()[1] <10:
            plt.ylim([0., 10.])
            
        elif plt.ylim()[1] <20:
            plt.ylim([0., 20.])
            
        elif plt.ylim()[1]>200:
            plt.ylim([0., 200.])
            title = title + ' some points out of range'
        
        plt.title(title)
        plt.xlabel('distribution parameter')
        plt.ylabel('metric value')
    
    def fitData(self):
        ''' linear fit to data '''

        p = np.polyfit(self.filteredData['distributionValue'], self.filteredData['metricValue'], 1, full=True)

        polyVals = p[0]
        error = p[1]        
        
        print(p)        
        
        # return the gradient and the error
        return (p[0][0], p[1][0])
        
            

if __name__=='__main__':
    
    pm = plotMarker()
    
    folder = '/home/galileo/Dropbox/smart laptop/impactFactor/metricMetrics/bin/results/varied/'    
    pm.inputfile = folder + 'variedMetrics10.txt'
    
    pm.loadData()
    print(pm.metricData, '\n')
    filterOptions = {'metric':'MR2', 'distribution':'stochastic'}
    pm.filterData(filterOptions)
    pm.plotData('plot')
    
    filterOptions = {'metric':'TR', 'distribution':'stochastic'}
    pm.filterData(filterOptions)
    pm.plotData('plot', style='r+')
    
    plt.savefig(folder + 'plot.png')



    
#    pm.fitData()
#
#        
##    print(pm.metricData)
#    
#    plt.show()
#        
        