# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 18:23:52 2015

@author: galileo
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

class dataSimulator():
    
    def __init__(self):
        
        #### Variables
    
        self.n = 10 # number of papers to simulate
        
        ## filenames for output of citation data
        self.folder = 'test/'
        
        self.stochname = 'testCites 0-3.txt' # for input
        self.fstoch = 'stochasticCitations.txt'
        self.flognorm = 'logNormalCitations.txt'
        self.fpareto = 'paretoCitations.txt'
        self.fnormal = 'normalCitations.txt'
        self.fflat = 'flat.txt'
        
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

#### Custom functions
    
    def saveData(self, data, fname):
        ''' save an array to file''' 
        
        print(data)
        print(np.shape(data))    
        
        f = open(self.folder + fname, 'w')
        for d in data:
    #        d = data[dind]
            f.write(str(d) + '\n')
            
        f.close()
        
    def loadData(self, fname):
        ''' load from a list of numbers '''
        
        try:
            f = open(fname)
        except:
            print('file failed to open ' + fname)
            return []
                
        data = f.readlines()
        dataOut = []
        for d in data:
            dataOut.append(float(d))
            
        return dataOut
        
        
    def loadStochasticData(self, fname, numArticles):
        ''' open stochastic data from a file '''
        
        data = ps.read_csv(fname, header=0, sep=';')
        print(data.keys())
        
    #    cites = {}
    #    
    #    for d in range(data.shape[0]):
    #        if data['cited article'][str(d)] in cites:
    #            
    #            data['cited article'][str(d)] = data['cited article'][str(d)] + 1
    #            
    #        else:
    #            data['cited article'][str(d)] = 1
                
        m = np.max(data['cited article'])+1
        if m > numArticles:
            print('more articles found than expected')
            numArticles = m
        cites = np.zeros(numArticles)
    
        for d in range(data.shape[0]):
            article = data['cited article'][d]
            
            cites[article] = cites[article] + 1
                
        return cites
        
    #def loadStochasticData2(folder):
    #    ''' load stochastic data from separate files '''
    #    
    #    files = os.listdir(folder)
    #    
    #    for f in files:
            
        
    
    # ========================================================
    
    
    #### get data points
    
    def simDataFromFile(self):
    
        stochCites = self.loadData(self.folder+ self.stochname)
        logNormalCites = self.loadData(self.folder + self.flognorm)
        paretoCites = self.loadData(self.folder + self.fpareto)
        normCites = self.loadData(self.folder + self.fnormal)
        flatCites = self.loadData(self.folder + self.fflat)
        
        self.citationData = [stochCites, logNormalCites, paretoCites, normCites, flatCites]
                

    def simDataFromFolder(self, dataFolder):
        
        fnames = os.listdir(dataFolder)
        
        self.citationLabels =[]

        self.citationData = []        
        for f in fnames:
            try:
                data = self.loadData(dataFolder + f)
                self.citationData.append(data)
                self.citationLabels.append(f)
            except:
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