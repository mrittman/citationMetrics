# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 18:31:51 2015

@author: galileo

analysis of citation data. Calculates mean, standard deviation, minimum, maximum,
10th, 50th and 90th percentiles. 

Calculates ratios of citations with ratios 1, n, n**2, but this doesn't seem
like very useful information (Bradford zones)

Also makes box plots for each condition

"""

import string
import numpy as np
from matplotlib import pyplot as plt


class metricSet():
    ''' object to contain statistics for journals under one set of conditions ''' 
    
    def __init__(self):
        
        ''' define status of journals '''
        self.journalSize = 0
        self.dataType = 'Undefined'
        self.metricType = 'Undefined'
        self.vals = []
        
    def stats(self):
        ''' calculate and print statistics for a  set of journals'''
        
        # return if there is no data
        if len(self.vals)==0:
            print('no values')
            return
            
        # calculate metrics
        self.mean = np.mean(self.vals)
        self.std = np.std(self.vals)
        self.min = np.min(self.vals)
        self.max = np.max(self.vals)
        self.median = np.median(self.vals)
        self.tenPC = np.percentile(self.vals, 10)
        self.ninetyPC = np.percentile(self.vals, 90)
#        self.bradfordZones, self.bradfordRatios = em.bradfordEstimator(self.vals)
#        self.percentiles = em.percentiles(self.vals)
        
        # print metrics
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
        ''' make a whisker/box plot of the metric values '''
        
        plt.figure()
        plt.boxplot(self.vals)


class analysis():
    ''' class file for calculating statistics for metrics from a variety of conditions.
    
        Input should be a csv or text file with one condition per row separated by tabs
        The first three entries of a row are: journal size, distribution type, metric type
        The rest of the row entries are metric values
        
        e.g. 100 \t normal \t TR1 \t 1\ \t 1 \t 1\ \t 1 \t 1\ \t 1
    
    '''
    
    def __init__(self):

        # input file 
        self.inputfilename = ''

        # file for summary output
        self.outname = 'test.csv'
        # folder for plots to be saved to
        self.plotFolder = ''

    def getData(self):
        ''' load metrics from file each line has the journal size, distribution 
        type and metric type followed by a list of metric values 
        
        also calculates statistics for each dataset
        
        '''

        # open file
        f = open(self.inputfilename, 'r')
        data = f.readlines()

        # initialise container for data
        self.dataSets = []
        
        # iterate data (rows in input file)
        for l in data:
            # split by tabs            
            d = string.split(l, '\t')
            # strip line breaks
            while d[-1] in ['\n', '']:
                d = d[:-1]
                   
            # initialise metricSet object to hold data
            m = metricSet()
            # add conditions to metric set (size, distrbution type, metric type)
            m.journalSize = d[0]
            m.dataType = d[1]
            m.metricType = d[2]
            
            # add metric values
            d = d[3:]
            # convert data to floats
            for ind in range(len(d)):
                d[ind] = float(d[ind])
            # add to metric set   
            m.vals = d
                        
            # calculate stats about each dataset
            m.stats()
            print('\n')

            # add metric set to data
            self.dataSets.append(m)
            
        # close the input data file
        f.close()


    def writeSummaryFile(self):
        ''' write the stats for each dataset to file '''

        # open a file for output
        g = open(self.outname, 'w')
        print(self.outname)
        # write column headers
        g.write('journal size\tdata type\tmetric type\tmean\tstd dev\tmin\tmax\tmedian\t10th percentile\t90th percentile\n')
        # iterate data sets
        for d in self.dataSets:
            # parse parameters to string
            line = str(d.journalSize) + '\t' + str(d.dataType) + '\t' + str(d.metricType) + '\t' + str(d.mean) + '\t' + str(d.std) + '\t' + str(d.min) + '\t' + str(d.max) + '\t' + str(d.median) + '\t' + str(d.tenPC) + '\t' +  str(d.ninetyPC) + '\n'
            # write out
            g.write(line)
        
        # close outut file
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
            
            # add title
            plt.title(title)
            
            # save to file
            figname = self.plotFolder + d.dataType+d.metricType+'_'+str(d.journalSize) + '.png'
            plt.savefig(figname)

            # close the plot
            plt.close()            
            
            
if __name__=='__main__':            

    self.inputfilename = ''

    # file for summary output
    self.outname = 'test.csv'
    # folder for plots to be saved to
    self.plotFolder = ''
                    
    plt.show()
    