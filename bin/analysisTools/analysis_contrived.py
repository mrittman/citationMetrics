# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 18:31:51 2015

@author: galileo

analysis of citation data

"""

import string
import numpy as np
from matplotlib import pyplot as plt

class metricSet():
    
    def __init__(self):
        
        self.journalSize = 0
        self.dataType = 'Undefined'
        self.metricType = 'Undefined'
        self.vals = []
        
    def stats(self):
        
        if len(self.vals)==0:
            print('no values')
            return
            
        self.mean = np.mean(self.vals)
        self.std = np.std(self.vals)
        self.min = np.min(self.vals)
        self.max = np.max(self.vals)
        self.median = np.median(self.vals)
        
        print('journal size' +' '+ str(self.journalSize))
        print('data type' +' '+ str( self.dataType))
        print('metric type' +' '+ str( self.metricType))
        
        print('mean' +' '+ str( self.mean))
        print('std dev' +' '+ str( self.std))
        print('min' +' '+ str( self.min))
        print('max' +' '+ str( self.max))
        print('median' +' '+ str( self.median))
        print('\n')
        
    def plot(self):
        ''' make a cat and mouse plot '''
        
        plt.figure()
        plt.boxplot(self.vals)


## load data

#fname = 'citationSimulator/citationData/citation data 2016-02-04 v1/metricOutputs.csv'
fname = 'data/textCitations.csv'
outname = 'analysis_contrived.csv'

f = open(fname)
data = f.readlines()

dataSets = []

for l in data:
    
    d = string.split(l, '\t')
    
    while d[-1] in ['\n', ' ', ';']:
        d = d[:-1]
           
    m = metricSet()
    m.journalSize = d[0]
    m.dataType = d[1]
    m.metricType = d[2]
    
    d = d[3:]
    
    for ind in range(len(d)):
        d[ind] = float(d[ind])
        
    m.vals = d
            
    dataSets.append(m)
    
    m.stats()
    
    print('\n')
    
f.close()


#g = open(outname, 'w')
#g.write('journal size\tdata type\tmetric type\tmean\tstd dev\tmin\tmax\tmedian\n')
#for d in dataSets:
#    
#    line = str(d.journalSize) + '\t' + str(d.dataType) + '\t' + str(d.metricType) + '\t' + str(d.mean) + '\t' + str(d.std) + '\t' + str(d.min) + '\t' + str(d.max) + '\t' + str(d.median) + '\n'
#    
#    g.write(line)
#
#g.close()

# box plots for each condition
for d in dataSets:
    d.plot()
    title = d.dataType + ', '  + d.metricType + ', size=' + str(d.journalSize)
    
    if plt.ylim()[1]<10:
        plt.ylim(0, 10)
    elif plt.ylim()[1]<20:
        plt.ylim(0, 20)
    
    plt.title(title)
    
    figname = 'analysisPlots/' + d.dataType+d.metricType+'_'+str(d.journalSize) + '.png'
    
    plt.savefig(figname)
    plt.close()
    
plt.show()
    