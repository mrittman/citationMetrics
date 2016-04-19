# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 18:23:52 2015

@author: galileo

Script to generate citations from various distributions and calculate metrics
for journals of various sizes. 

Distributions include: pareto, normal, log normal, uniform

Each distribution has parameters with default values:

mean of normal distribution: citationSimulatornormMean = 3.5
sd of the normal distribution: citationSimulatornormSigma = 1.67186077
paramter of the log normal distribution: citationSimulatorlogNormSigma = 1.67186077
location of the log normal distribution:  citationSimulatorlogNormLoc = 0.34723183
paramter of the pareto distribution: citationSimulatorparetoParam = 1.25
maximum for uniform citations (min is 0): citationSimulatorflatCitesMax = 8.


"""
# ========================================================

#### Load commands and functions

import numpy as np
from matplotlib import pyplot as plt
import citationGenerator
import scipy.stats as st
import pandas as ps
import impactFactor
import os
import extraMetrics
import os


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
    
        self.n = 10 # number of papers to simulate
        
        ## filenames for output of citation data (and input of stochastic data)
        self.folder = 'test/' # folder that data is saved to
        
        self.fstoch = 'testCites 0-3.txt' # stochastic input name
        self.flognorm = 'logNormalCitations.txt'  # log normal output name
        self.fpareto = 'paretoCitations.txt' # pareto output name
        self.fnormal = 'normalCitations.txt' # normal output name
        self.fflat = 'flat.txt' # uniform output name
        
        ## for the distribution models
        self.normMean = 3.5
        self.normSigma = 1.67186077
        self.logNormSigma = 1.67186077
        self.logNormLoc = 0.34723183
        self.paretoParam = 1.25
        self.flatCitesMax = 8.
        
        # output definitions
        self.citationLabels = ['stochastic', 'log normal', 'pareto', 'normal', 'uniform']
        self.maxCitations = 100 # max citations allowed per paper
        self.journalSizes = [10]
        self.metricTypes = ['TR', 'MR1', 'MR2', 'EX1']
        self.metricsFile = 'metrics_test.csv'

        # initialise results        
        self.impactFactors = {}
        self.citationData = []
        self.journals = []
        
        self.em = extraMetrics.extraMetrics()

    #### Data input and output
    
    def saveData(self, data, fname):
        ''' save an array to file. Used when generating citations.
        
        writes a text file with one number on each line, no header.
        
        !! NB: Automatically overwrites if the file already exists !!
        ''' 
          
        f = open(self.folder + fname, 'w')
        for d in data:
            f.write(str(d) + '\n')
        f.close()
        
    def loadData(self, fname):
        ''' load from a list of numbers.
        
        Can load data saved using self.saveData
        
        Returns: list of citations
        
        '''
        
        # open the file to write to
        try:
            f = open(fname)
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
        
        
    def loadStochasticData(self, fname, numArticles):
        ''' open stochastic data from a file

        input data should be generated from the stochastic simulator
        fname is the filename (string)
        numArticles (integer) is the number of articles in the journal, some of which may not be cited
        
        NB there's an assumption that articles are sequentially labelled with integers.
        
        returns: list of citations
        
        '''
        
        # read the file into a pandas array
        data = ps.read_csv(fname, header=0, sep=';')
                
        # Verify that the input number of articles isn't too small 
        m = np.max(data['cited article'])+1
        if m > numArticles:
            print('more articles found than expected')
            numArticles = m
            
        # initialise number of citations for each article
        cites = np.zeros(numArticles)

        # add citations for each article from the data    
        for d in range(data.shape[0]):
            # add citation to number 'cited article' (assumes articles are sequentially listed using integers starting at 0)
            article = data['cited article'][d]        
            cites[article] = cites[article] + 1
                
        # return list of citations (list)
        return cites
          
            
    # ========================================================
    
    
    #### get data points
    
    def simDataFromFile(self):
        ''' Simulate citations. Use this to load one data set for each 
        distribution type: log normal, pareto, normal, uniform, stochastic data set.
        
        Returns: list containing lists of citations in the order stochCites, logNormalCites, paretoCites, normCites, flatCites
        
        note that the order of the output is the same as the default for self.citationLabels
        
        '''
    
        # load stochastic citations
        stochCites = self.loadData(self.folder+ self.fstoch)
        logNormalCites = self.loadData(self.folder + self.flognorm)
        paretoCites = self.loadData(self.folder + self.fpareto)
        normCites = self.loadData(self.folder + self.fnormal)
        flatCites = self.loadData(self.folder + self.fflat)
        
        self.citationData = [stochCites, logNormalCites, paretoCites, normCites, flatCites]
                

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
                # save data
                self.citationData.append(data)
                # save data label from filename
                self.citationLabels.append(f)
            except:
                # output something if the loading doesn't work
                print(dataFolder + f + ' failed to load data')
                    
    
    # ========================================================

    def loadFromFile(self, filename):
        ''' load citation data from a csv file'''
        
        # open file
        f = open(filename)
        data = f.readlines()
        
        self.citationLabels = []
        count = 0

        # each row is one set of citations
        self.citationData = []        
        for d in data:
            cites = d.split(';')
            for c in range(len(cites)):
                cites[c] = int(cites[c])
                
                        
            self.citationData.append(cites)
            self.citationLabels.append(str(count))
            
            count=count+1
            
        # close file
        f.close()


    # ========================================================
    
    #### generate 30,000 data points from various disrubitions
    def generateCitations(self):
        
        # stochastic model
        fname = 'bin/data/testCites 0-3.txt' 
        #stochCites = loadStochasticData(fname, 0)
        stochCites = self.loadData(fname)

        # log normal        
        logNormalCites = self.generateLogNormalCites()
        self.saveData(logNormalCites, self.flognorm)
        
        # pareto
        paretoCites = self.generateParetoCites()
        self.saveData(paretoCites, self.fpareto)
        
        # normal 
        normCites = self.generateNormCites()
        self.saveData(normCites, self.fnormal)
        
        # flat [1,100]
        flatCites = self.generateFlatCites()
        self.saveData(flatCites, self.fflat)
        
        # collate all the data
        self.citationData = [stochCites, logNormalCites, paretoCites, normCites, flatCites]
        
    
    def generateAddCitations(self, citationType):
        ''' generate a single citation set and add to self.citationData '''

        # log normal        
        if citationType=='log normal':
            cites = self.generateLogNormalCites()
            self.saveData(cites, self.flognorm)
        
        elif citationType=='pareto':
            # pareto
            cites = self.generateParetoCites()
            self.saveData(cites, self.fpareto)
            
        elif citationType=='normal':
            # normal 
            cites = self.generateNormCites()
            self.saveData(cites, self.fnormal)
            
        elif citationType=='uniform':
            # flat [1,100]
            cites = self.generateFlatCites()
            self.saveData(cites, self.fflat)
        
        self.citationData.append(cites)
            
        
    def generateLogNormalCites(self):
        # log normal
        logNormalCites = np.random.lognormal(self.logNormSigma, self.logNormLoc, size = self.n)
        logNormalCites = np.round(logNormalCites)

        return logNormalCites

    def generateParetoCites(self):
        paretoCites = st.pareto.rvs(self.paretoParam, size=self.n)
        paretoCites = np.round(paretoCites)

        return paretoCites
        
    def generateNormCites(self):
        normCites = np.random.normal(self.normMean, self.normSigma, size = self.n)
        normCites = np.round(normCites)

        return normCites
        
    def generateFlatCites(self):
        flatCites = np.random.rand(self.n) * self.flatCitesMax
        flatCites = np.round(flatCites)

        return flatCites        
    
    # ========================================================
    
    ## Cut-off for large values
    def cutOffData(self):
        for data in self.citationData:
            for pt in range(len(data)):
                
                if data[pt]>self.maxCitations:
                    data[pt] = self.maxCitations
            
    
    # ========================================================
    
    ##### Sort into groups and calculate IFs
    def getMetrics(self):

        ifCount = 0
        
        # iterate sizes of journals
        for size in self.journalSizes:
        
            # iterate sources of citations
            for dataType in range(len(self.citationData)):
        
                ## split into journals    
                    
                # initialize journal sizes
                journals = []
        
                count = size
                while count<=len(self.citationData[dataType]):
                    
                    # fill a journal with papers (citation counts)
                    journals.append(self.citationData[dataType][count-size:count])
            
                    count = count+size
        
            
                ## calculate IFs for each journal
        
                metrics = {}
                
                for m in self.metricTypes:
                    metrics[m] = []
                
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
                    
                    print(vals[m])

                    self.impactFactors[str(ifCount)] = [[size, self.citationLabels[dataType], m], vals[m]]

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
   
    ds = dataSimulator() 
     
    # ========================================================

    # get the data
    ds.generateCitations()
    # cut off data at some limit (optional)
    ds.cutOffData()
    # calculate metrics for various journal sizes
    ds.getMetrics()
    # save to file
    ds.saveMetrics()