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



class plotMarker():
    
    def __init__(self):
        ''' initialise stuff '''
        
        a = 1
        self.inputfile = ''
        
    
    def loadData(self):
        ''' load data from file. It should have columns: journal size, distribution, statistical parameter, metric type, metric value '''        
        
        f = open(self.inputfile)       
        self.metricData = ps.read_csv(self.inputfile, sep='\t')
        
        
    def filterData(self, filterOptions):
        ''' filter by a dictionary
        columns are: journalSize, distribution, metric, metricValue'''
        
        data = self.metricData
        for f in filterOptions:
            data = data[data[f]==filterOptions[f]]
            
        self.filteredData = data
        
        print(self.filteredData)
            
    def plotData(self, title):
        ''' plot filtered Data '''
        
        plt.figure()
        
        # when metric only has one value
        plt.plot(self.filteredData['distributionValue'], self.filteredData['metricValue'], 'gx')
        
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
    print(pm.metricData)
    filterOptions = {'metric':'MR1', 'distribution':'flat'}
    pm.filterData(filterOptions)
#    pm.plotData('plot')
    pm.fitData()

        
#    print(pm.metricData)
    
    plt.show()
        
        