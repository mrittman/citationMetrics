# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 20:25:25 2014

@author: galileo

This is code for generating various citation metrics from data. The input data 
is in a file, and lists citations to a corpus of articles. 


"""

import pandas as ps
import numpy as np
#from string import split
import math

class impactFactor():
    
    
    def __init__(self):
        ''' initial settings '''
              
        
        self.journalName = 'journal' # name of journal that IF is calculated for        
        self.metric = -1      # value of impact factor (-1 if no calculation made, or error)

        # options for filter of publication dates
        self.pubFilterType = 'top hat'
        self.pubFilterOptions = {'upperBound': 3, 'lowerBound': -1, 'height': 1}    

        # options for filtering of citation dates
        self.citeFilterType = 'top hat'
        self.citeFilterOptions = {'upperBound': 10, 'lowerBound': -1, 'height': 1}    

        # options for filter of difference between citation and publication dates
        self.diffFilterType = 'top hat'
        self.diffFilterOptions = {'upperBound': 5, 'lowerBound': 0, 'height': 1}          
        
            
    #### Main calculation of Impact Factor        
        
    def getIF(self, citationFile, journal, numPapers, metricType='TR'):
        ''' calculate the impact factor
        
        citationFile: string - name of file containing a list of citations\\
        journal: string - name of 'journal' you want to calculate metric for\\
        numPapers: integer - total number of papers published in journal in timeframe\\
        timeFile: dictionary - parameters for timeFilter\\
        metricType: string - method for calculating the citation metric
        
        Available methods are:
            TR - the Thomson Reuters impact factor\\
            MR1 - with discretized scoring of citations\\
            MR2 - scaling of citations (continuous scaling function)
      
        The citation file should be a csv file (seperator semi-colon) with headers:
            'date of citation'\\
            'date of publication'\\
            'journal' : journal of cited article, or equivalent corpus identifier\\
            'cited article' : ID of cited article, e.g. doi number
            
        NB filtering by journal not yet active
                
        '''

        # read in citation data from a csv file using Pandas
        data = ps.read_csv(citationFile, sep = ';', header = 0)
        print(data.keys())
#        print('input data', data)
                
        # calculate time between publication and citation
        # NB types after here are arrays
        citationTimeDiff = data['date of citation'] - data['date of publication']
        citationTimeDiff = np.array(citationTimeDiff)
        pubDates = np.array(data['date of publication'])
        citeDates = np.array(data['date of citation'])
        
        # filter by journal
#        journalIndices = data['cited journal'].where(data['cited journal'] == journal)
#        data = data[journalIndices]
#        filteredJournal = data['cited journal'].where('cited journal' = journal)
                
        # filter time differences between publication and citation
        filteredTimes = self.applyFilter(citationTimeDiff, filtertype=self.diffFilterType, options = self.diffFilterOptions)
        
        # filter publication dates
        filteredPubDates = self.applyFilter(pubDates, filtertype=self.pubFilterType, options =self.pubFilterOptions)        
        
        # filter citation dates
        filteredCites = self.applyFilter(citeDates, filtertype=self.citeFilterType, options = self.citeFilterOptions)
                
        # apply filters to data
        # convolve pub dates and times
        conv = filteredTimes * filteredPubDates * filteredCites
                        
        # apply filters  - there is probably a quicker way to do this
        filteredData = ps.DataFrame([]) 
        for ind in range(data.shape[0]):           
            # check if data should be included
            if conv[ind] !=0:
#                # apply journal filtering
#                if data['journal'][ind]==journal:
                filteredData = filteredData.append(data[ind:ind+1])
                                        
        # Get values of any additiional functions needed
        options = self.getOptions(filteredData, optionsRequired = ['all'])
              
        ## ===========
              
        ## calculate the metric 
        
        if metricType =='TR':
            print('Thomson Reuters type metric')  
            
            metric = float(filteredData.shape[0])/float(numPapers)
            
        elif metricType == 'MR1':
            print('Rittman metric 1')
            
            citationScores = self.citationScore(options['citations per article'])                                  
            metric = float(sum(citationScores))/float(numPapers)
            
        elif metricType == 'MR2':
            print('Rittman metric 2')
            
            citationScores = self.citationScore2(options['citations per article'])           
            metric = float(sum(citationScores))/float(numPapers)  
            metric = self.citationScore2Inv(metric)
  
        else:
            print('invalid metric defined')
            metric = 0

        print('calculated impact factor: ', metric)

        ## output        
        self.metric = metric
            
        return metric

    
    def simpleIF(self, dataIn, numPapers, metricType = 'TR'):
        ''' Calculate impact factor from a list of citations per paper '''
    
        dataIn = np.array(dataIn)
        
        if metricType =='TR':
            print('Thomson Reuters type metric')  
            
            metric = sum(dataIn)/float(numPapers)
            
        elif metricType == 'MR1':
            print('Rittman metric 1')
            
            citationScores = self.citationScore(dataIn)
            metric = float(sum(citationScores))/float(numPapers)
            
        elif metricType == 'MR2':
            print('Rittman metric 2')
            
            citationScores = self.citationScore2(dataIn)          
            metric = float(sum(citationScores))/float(numPapers)  
            print(metric)
            metric = self.citationScore2Inv(metric)
            
        elif metricType == 'EX1':
            print('Extreme metric')
            
            metric = dataIn[0]
            
        else:
            print('invalid metric defined')
            metric = 0

#        print('calculated impact factor: ', metric)

        ## output        
        self.metric = metric
            
        return metric


    #### Functions to filte and modify input        
        
    def applyFilter(self, dataIn, filtertype='default', options = []):
        ''' Apply some kind of crazy filter '''
        
        if filtertype=='top hat':
            # options: lowerBound, upperBound, height
            dataOut = self.topHatFilter(dataIn, options)
            
        else:
            print('no filter defined')
            dataOut = dataIn
            
        return dataOut        

        
    def getOptions(self, dataIn, optionsRequired):
        ''' get some extra input for filters

        dataIn: dataFrame of input data
        optionsRequired: list of stuff to ouptut can include 'number of citations'
        
        '''        
        # set status for 'all'
        if 'all' in optionsRequired:
            optionsRequired = ['number of citations']
  
        # initialise output
        options = {}
  
        if 'number of citations' in optionsRequired:
            
            # get number of citations per article
            try:
                options['citations per article']  = dataIn['cited article'].value_counts()
                print(type(options['citations per article']))
            except:
                options['citations per article'] = ps.DataFrame([])
            
        return options
        
        
    def citationScore(self, cites):
        ''' score citations on a roughly log scale '''

        scores = []        
        for c in cites:
            if c==0:
                scores.append(0)
            
            elif c<=5:
                scores.append(1)
                
            elif c<=10:
                scores.append(2)
                
            elif c<=20:
                scores.append(3)
                
            elif c<=40:
                scores.append(4)
                
            elif c<=80:
                scores.append(5)
                
            else:
                scores.append(6)
                
        return scores
                
    def citationScore2(self, cites):
        ''' turn cites into scores in a more sophisticated manner.
        
             Scoring is so that the the first citation has a value of 1, and the
             Nth citation has a value of ht. Note that's it a sum of a finite
             geometric progression. ht should be less than 1.
             
        '''        
        
        ht = 0.5 # the Nth citation has this value
        N = 10. # N (see above)

        d = ht**(1./(N-1.))
        
        if d==1.:
            print('d==1 in citationScore2')
            
            return cites
        
        # calculate scores
        scores = (d**(cites) - 1.)/(d-1.) 
        
        
        return scores
        
#        s = (1 + d + d**2 + ... + d**(N-1)
#         sd = d + d**2 + ... + d**(N)
#         sd = s-1 + d**(N+1)
#         s(1-d) = 1 - d**(N+1)
        
#        s = (d**(N+1)-1)/(d-1)
#        
#        s = 1/(d-1) * (1 - 1/Nd) = (Nd - 1)/[Nd(d-1)]
#          = (1- 1/[Nd])/(d-1)
      
    def citationScore2Inv(self, num):
        '''         
        turn a scaled number into an 'unscaled' value, i.e. correct for weighting from the metric        
                
        '''

        ht = 0.5 # the Nth citation has this value
        N = 10. # N (see above)

        d = ht**(1./(N-1.))

        val = math.log(num * (d-1.) + 1., d)
        print(d, num * (d-1.) + 1.)
        print(num)
        
        # a logarithm missing here
        
        return val
  
  
  
    #### Filters
        
    def topHatFilter(self, data, options):
        ''' top hat filter. Input is the data to be filtered, and a dictionary containing:
 
        height: height of top hat (optional)
        lowerBound: min cutoff
        uppperBound: max cutoff
        
        '''
        print('top hat applied')
        # get options
        minVal = options['lowerBound']
        maxVal = options['upperBound']
        try:
            setVal = options['height']
        except:
            setVal = 1
                
        # filter by max and min values
        dout = (data>minVal)*(data<maxVal)
        # make the heights equal
        dout = (dout!=0) * setVal
        
        return dout
        
      
def strip(s):
    ''' Remove odd characters from a string '''
    
    ls = ['\n','\t', ' ']
    
    while s[0] in ls:
        s = s[1:]
        
    while s[-1] in ls:
        s = s[:-1]
        
    return s
      
    
if __name__=='__main__':

    ifc = impactFactor()

    fname = 'citationSimulator/bin/data/testCites0-2.txt' 
    numberOfPapersPublished = 500
#    ifc.readData(fname)
#    ifc.importDataFrame(fname)
        

#    ifc.getIF(fname, 'journal', numberOfPapersPublished, metricType='TR')     
#    ifc.getIF(fname, 'journal', numberOfPapersPublished, metricType='MR1')     
#    ifc.getIF(fname, 'journal', numberOfPapersPublished, metricType='MR2')     

    cites = [0,1,5,3,0,6,9,4,0]
    
    ifc.simpleIF(cites, len(cites), metricType = 'TR')
    ifc.simpleIF(cites, len(cites), metricType = 'MR1')
    ifc.simpleIF(cites, len(cites), metricType = 'MR2')
