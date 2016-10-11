# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 18:23:52 2015

@author: galileo

Finds metrics for citation data.

Metrics are:

 - impact factor
 - MR1: step-wise scoring
 - MR2: scaled scoring
 - h-index
 - EX1: value of the first citation

 - median
 - 10th percentile
 - 90th percentile
 - mean


"""
# ========================================================

#### Load commands and functions

import numpy as np
#from matplotlib import pyplot as plt
import scipy.stats as st
import pandas as ps
import impactFactor
import os
import extraMetrics


# ========================================================

class citationSimulator():
    
    def __init__(self):
        ''' initialise variables 
        
        some variables:
        n: (integer) number of papers to simulate 
        journalSizes: (list of integers) sizes of journals to simulate metrics for
        metricTypes: (list of strings) metrics from 'impactFactor' to simulate
        metricsFile: (string) output filename to save metrics to
        
        File names for data from each distribution and distribution parameters are also set from here.
              
        '''
        
        #### Variables
            
        ## filenames for input of citation data
        self.folder = 'test/' # folder that data is stored in
        
        self.fstoch = 'test/stochasticTest.txt' # stochastic input name
        self.flognorm = 'logNormalCitations.txt'  # log normal input name
        self.fpareto = 'paretoCitations.txt' # pareto input name
        self.fnormal = 'normalCitations.txt' # normal input name
        self.fflat = 'flat.txt' # uniform input name
        
        ## for the distribution models
        self.normMean = 3.5
        self.normSigma = 1.67186077
        self.logNormSigma = 1.67186077
        self.logNormLoc = 0.34723183
        self.paretoParam = 1.25
        self.flatCitesMax = 8.
        
        # output definitions
        self.citationLabels = ['stochastic', 'log normal', 'pareto', 'normal', 'uniform'] # default order of outputs; redefined in some functions
        self.maxCitations = 100 # max citations allowed per paper, not automatically applied
        self.journalSizes = [10] # sizes of journals for analysis. The total number of papers is split into bins of each size.
	# Available options for metrics:
	#	'TR1' = Traditional impact factor
	#	'MR1' = Step-wise weighted metric
	#	'MR2' = Continuously varying weighted metric: each subsequent citation is weighted slightly less than the previous one
	#	'EX1' = An 'extreme' metric, takes the number of citations of the first paper in the journal.
        self.metricTypes = ['TR', 'MR1', 'MR2', 'EX1'] 
        self.metricsFile = 'metrics_test.csv' # filename to save output metrics to

        # initialise results        
        self.impactFactors = {}
        self.citationData = []
        self.journals = []
        
        self.em = extraMetrics.extraMetrics()

    #### Data input and output
    
        
    def loadData(self, fname):
        ''' load from a list of numbers.
        
        Can load data saved using citationSimulator.saveData
        
        Returns: list of citations
        
        '''
        
        # open the file to write to
        try:
            f = open(fname, 'r')
        except:
            print('file failed to open ' + fname)
            return []
        
        # read from file
        data = f.readlines()
        # initialise output
        dataOut = []
        for d in data:
            dataOut.append(float(d))
            
        # return list of citations
        return dataOut
        
        
                

    def simDataFromFolder(self, dataFolder):
        ''' Load data saved in the same folder. The folder should ideally only 
        contain citation files, it doesn't do a thorough check for file types 
        and format.
        
        self.citationsLabels are regenerated from the file names
        
        returns: None
        
        Sets: self.citationData, self.citationLaels
        
        '''
        
        # get list of filenames
        fnames = os.listdir(dataFolder)
        
        # reset citation labels
        self.citationLabels =[]

        # initialise output
        self.citationData = [] 
        
        # iterate files
        for f in fnames:
            # open each file in turn
            try:
                # load data from file
                data = self.loadData(dataFolder + f)
                print(f)
                # save data
                self.citationData.append(data)
                # save data label from filename
                self.citationLabels.append(f)
            except:
                # output something if the loading doesn't work
                print(dataFolder + f + ' failed to load data')
                    

    def loadFromFile(self, filename):
        ''' load citation data contained in a single csv file. 
        One data set per row, and the data separator is a semi-colon
        
        citation labels are integers

        return: None
        
        sets: self.citationData, self.citationLabels
        
        '''
        
        # open file
        f = open(filename)
        data = f.readlines()
        
        # initialise citation labels and names (count)
        self.citationLabels = []
        count = 0

        # each row is one set of citations
        self.citationData = []        
        for d in data:
            # parse data
            cites = d.split(';')
            for c in range(len(cites)):
                cites[c] = int(cites[c])
                        
            # save data
            self.citationData.append(cites)
            # save data name
            self.citationLabels.append(str(count))
            
            count=count+1
            
        # close file
        f.close()


    
    # ========================================================

    #### Post-simulation functions
    
    ## Cut-off for large values
    def cutOffData(self):
        ''' Cut off citation data at a maximum value (self.maxCitations) '''
        
        for data in self.citationData:
            for pt in range(len(data)):
                
                if data[pt]>self.maxCitations:
                    data[pt] = self.maxCitations
            
    
    # ========================================================
    
    ##### Metric functions
    
    def getMetrics(self):
        ''' 

	Split the data sets in self.citationData into journals of given sizes and calculate metrics.

        Uses the following settings:
        self.journalSizes (list of integers): journal sizes to split each data set into
        self.metricTypes (list of strings): metrics from impactfactor.py to use
        
        Sets the values of self.impactFactors
        
        '''        

        ifCount = 0
        
        # iterate sizes of journals
        for size in self.journalSizes:
        
            # iterate sources of citations
            for dataType in range(len(self.citationData)):
        
                ## split into journals    
                    
                # initialize journal sizes
                journals = []
        
                count = size # counter for papers
                while count<=len(self.citationData[dataType]):
                    
                    # fill a journal with papers (citation counts)
                    journals.append(self.citationData[dataType][count-size:count])
            
                    count = count+size
        
        
                ## calculate IFs for each journal
        
		# initialise the dictionary of metrics
#                metrics = {}
#                for m in self.metricTypes:
#                    metrics[m] = []
                
		# load metric calculator
                ifc = impactFactor.impactFactor()

                # iterate version of the metric
                for m in self.metricTypes:

                    # iterate journals
                    metricVals = []
                    for j in journals:
                        
                        # calculate the metric
                        metricVal = ifc.simpleIF(j, len(j), metricType=m)
                        # add the data to list for the metric
                        metricVals.append(metricVal)
                    
                    # record data
                    print(ifCount, size, self.citationLabels, dataType)
                    self.impactFactors[str(ifCount)]  = [[size, self.citationLabels[dataType], m], metricVals]
                    ifCount = ifCount + 1
                    
                # find other metrics
                    
                vals = {}
                for j in journals:
                    
                    em = extraMetrics.extraMetrics()
                    em.citations = j
                    
                    # bradford boundary and ratios, h index and various percentiles
                    exVals = em.findAllMetrics()

                    # record the Bradford zones and ratios, h index and median
                    count = 0
                    for m in ['BF1', 'BF2', 'BR1', 'BR2', 'H', 'P50']:
                        try:
                            vals[m].append(exVals[count])
                        except KeyError:
                            vals[m] = [exVals[count]]

                        count = count+1
                        
                for m in ['BF1', 'BF2', 'BR1', 'BR2', 'H', 'P50']:
                    
                    try:
                        self.impactFactors[str(ifCount)] = [[size, self.citationLabels[dataType], m], vals[m]]
                    except KeyError:
                        pass

                    ifCount = ifCount + 1
                    
                    
    
#        self.journals = journals
        
    
    def saveMetrics(self):
            
        # save metrics to file
        f = open(self.folder + self.metricsFile, 'w')         
        for ifv in self.impactFactors:
                        
            line = ''
        
            for a in self.impactFactors[ifv][0]:
                line = line + str(a) + '\t'
            for a in self.impactFactors[ifv][1]:
                line = line + str(a) + '\t'
            line = line[:-1] + '\n'
            
            f.write(line)
            
        f.close()
        
        print('data saved as ' + self.folder + self.metricsFile)


if __name__=='__main__':
    
        # ========================================================
   
    ds = citationSimulator() 
     
    # ========================================================

    # get the data
    ds.generateCitations()
    print('citationdata', ds.citationData)
    # cut off data at some limit (optional)
    ds.cutOffData()
    # calculate metrics for various journal sizes
    ds.getMetrics()
    # save to file
    ds.saveMetrics()
