# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 18:31:51 2015

@author: galileo

analysis of citation data

"""

import string
import numpy as np
from matplotlib import pyplot as plt
#import extraMetrics as em

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
        self.tenPC = np.percentile(self.vals, 10)
        self.ninetyPC = np.percentile(self.vals, 90)
#        self.bradfordZones, self.bradfordRatios = em.bradfordEstimator(self.vals)
#        self.percentiles = em.percentiles(self.vals)
        
        print('journal size' +' '+ str(self.journalSize))
        print('data type' +' '+ str( self.dataType))
        print('metric type' +' '+ str( self.metricType))
        
        print('mean' +' '+ str( self.mean))
        print('std dev' +' '+ str( self.std))
        print('min' +' '+ str( self.min))
        print('max' +' '+ str( self.max))
        print('median' +' '+ str( self.median))
        print('percentiles' + ' ' + str(self.tenPC) + ' ' +  str(self.ninetyPC))
        print('\n')
        
    def plot(self):
        ''' make a cat and mouse plot '''
        
        plt.figure()
        plt.boxplot(self.vals)


class analysis():
    
    def __init__(self):

#fname = 'citationSimulator/citationData/citation data 2016-02-04 v1/metricOutputs.csv'
#    self. fname = 'citationSimulator/data 2016-03-17 varied v2_1/metrics_varied_v2_1.csv'
        # file containing citation metrics
        self.fname = ''

        # file for summary output
        self.outname = 'test.csv'
        # folder for plots to be saved to
        self.plotFolder = ''

    def getData(self):
        ''' load metrics from file each line has he journal size, distribution 
        type and metric type followed by a list of metric values 
        
        also calculates statistics for each dataset
        
        '''

        # open file
        f = open(self.fname)
        data = f.readlines()

        # initialise output
        self.dataSets = []
        
        for l in data:
            
            d = string.split(l, '\t')
            
            while d[-1] in ['\n', '']:
                d = d[:-1]
                   
            m = metricSet()
            m.journalSize = d[0]
            m.dataType = d[1]
            m.metricType = d[2]
            
            d = d[3:]
            
            for ind in range(len(d)):
                d[ind] = float(d[ind])
                
            m.vals = d
                    
            self.dataSets.append(m)
            
            # calculate stats about each dataset
            m.stats()
            
            print('\n')
            
        f.close()


    def writeSummaryFile(self):
        ''' write the stats for each dataset to file '''

        g = open(self.outname, 'w')
        g.write('journal size\tdata type\tmetric type\tmean\tstd dev\tmin\tmax\tmedian\t10th percentile\t90th percentile\n')
        for d in self.dataSets:
            
            line = str(d.journalSize) + '\t' + str(d.dataType) + '\t' + str(d.metricType) + '\t' + str(d.mean) + '\t' + str(d.std) + '\t' + str(d.min) + '\t' + str(d.max) + '\t' + str(d.median) + '\t' + str(d.tenPC) + '\t' +  str(d.ninetyPC) + '\n'
            
            g.write(line)
        
        g.close()

    def boxPlots(self):
        ''' make a box plot for each dataset '''

        # box plots for each condition
        for d in self.dataSets:
            d.plot()
            title = d.dataType + ', '  + d.metricType + ', size=' + str(d.journalSize)
            
            # set to standardised x and y limits for easy comparison
            if plt.ylim()[1]<10:
                plt.ylim(0, 10)
            elif plt.ylim()[1]<20:
                plt.ylim(0, 20)
            
            plt.title(title)
            
            figname = self.plotFolder + d.dataType+d.metricType+'_'+str(d.journalSize) + '.png'
            
            plt.savefig(figname)
            plt.close()
            
            
            
if __name__=='__main__':            

    self.fname = ''

    # file for summary output
    self.outname = 'test.csv'
    # folder for plots to be saved to
    self.plotFolder = ''
                    
    plt.show()
    