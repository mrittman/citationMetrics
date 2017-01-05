# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 20:25:25 2014

@author: galileo

This is code for generating various citation metrics from data. The input data
is in a file, and lists citations to a corpus of articles.

There are two methods for generating the metrics, dependent on the input file:

1. impactfactor.getIF
The citation file should be a csv file (seperator semi-colon) with headers:
            'date of citation'\\
            'date of publication'\\
            'journal' : journal of cited article, or equivalent corpus identifier\\
            'cited article' : ID of cited article, e.g. doi number

    Data can be filtered by date of citation and publication.


2. impactfacor.simpleIF
Calculates from a list of citations. In this case there is no filtering possible.


"""

import pandas as ps
import numpy as np
#from string import split
import math
#import extraMetrics

class metrics():


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


        # variables for MR2
        ht = 0.5 # the Nth citation has this value
        N = 10. # N (defn of ht)
        # calculate value of d
        self.d = ht**(1./(N-1.))

        # initialise citations
        self.citations = [] # used by all metric functions except getIF()


    #### Main calculation of Impact Factor (from stochastic data)

    def getIF(self, citationFile, journal, numPapers, metricType='TR'):
        ''' calculate the impact factor

        citationFile: string - name of file containing a list of citations
        journal: string - name of 'journal' you want to calculate metric for
        numPapers: integer - total number of papers published in journal in timeframe
        timeFile: dictionary - parameters for timeFilter
        metricType: string - method for calculating the citation metric

        Available methods are:
            TR - the Thomson Reuters impact factor
            MR1 - with discretized scoring of citations
            MR2 - scaling of citations (continuous scaling function)

        The citation file should be a csv file (seperator semi-colon) with headers:
            'date of citation'
            'date of publication'
            'journal' : journal of cited article, or equivalent corpus identifier
            'cited article' : ID of cited article, e.g. doi number

        NB filtering by journal not yet active

        '''

        # read in citation data from a csv file using Pandas
        data = ps.read_csv(citationFile, sep = ';', header = 0)
        print(data.keys())

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

        # Get values of any additional functions needed
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

        elif metricType == 'H':
            print('h index')

            self.em.citations = options['citations per article']
            metric = self.em.hindex()

        elif metricType == 'median':
            print('median')

            metric = np.percentile(self.citations, options['citations per article'])

        else:
            print('invalid metric defined')
            metric = 0

        print('calculated impact factor: ', metric)

        ## output
        self.metric = metric

        return metric




    def getMetric(self, numPapers=-1, metricType = 'TR', percentiles=[50]):
        ''' Calculate impact factor from a list of citations per paper '''

        # make sure the data is in array form
        dataIn = np.array(self.citations)

        # set the number of papers to the number of citations, if not defined
        if numPapers == -1:
            numPapers = len(dataIn)

        # Thompson Reuters impact factor
        if metricType =='TR':
            print('Thomson Reuters type metric')

            metric = sum(dataIn)/float(numPapers)

        # Banded scoring system
        elif metricType == 'MR1':
            print('Rittman metric 1')

            citationScores = dataIncore(dataIn)
            metric = float(sum(citationScores))/float(numPapers)

        # Graduated scoring system
        elif metricType == 'MR2':
            print('Rittman metric 2')

            citationScores = self.citationScore2(dataIn)
            metric = float(sum(citationScores))/float(numPapers)
            metric = self.citationScore2Inv(metric)

        # 'Extreme' metrics, takes the value of the first citation
        elif metricType == 'EX1':
            print('Extreme metric')

            metric = dataIn[0]

        # H index
        elif metricType == 'H':
            print('h index')

            metric = self.hindex()

        # median citations
        elif metricType == 'median':
            print('median')

            metric = np.percentile(self.citations, 50)

        # percentiles: 10, 25, 50, 75, 90
        elif metricType == 'percentiles':
            print('percentiles')

            metric = self.percentiles()

        else:
            print('invalid metric defined')
            metric = 0

        ## output
        self.metric = metric

        return metric


    #### Functions to filter and modify input

    def applyFilter(self, dataIn, filtertype='default', options = []):
        ''' Apply some kind of crazy filter '''

        # top hat filter (1 between bounds and zero elsewhere)
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

        # calculate the number of citations for each paper
        if 'number of citations' in optionsRequired:

            # get number of citations per article
            try:
                options['citations per article']  = dataIn['cited article'].value_counts()
                print(type(options['citations per article']))
            except:
                options['citations per article'] = ps.DataFrame([])

        return options


    def citationScore(self, cites):
        ''' score citations on a graduated scale, roughly logarithmic

        used by the MR1 metric '''

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

             used by the MR2 metric

        '''


        if self.d==1.:
            print('d==1 in citationScore2')

            return cites

        # calculate scores
        scores = (self.d**(cites) - 1.)/(self.d-1.)


        return scores

##       Working for the finite sum of a geometric progresion
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

        can be used by the MR2 metric

        '''

        # number to log
        rawNum = num * (self.d-1.) + 1.

        # return 0 if this value is 0
        if rawNum==0:
            return 0.

        # calculate the inverse
        val = math.log(rawNum, self.d)

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





    #### Some statistical properties of the citation set


    def bradfordEstimator(self):

        ''' find the zone boundaries fitting Bradford's law '''

        # put values in order (smallest to largest)
        citations = np.sort(self.citations)
        totalCites = np.sum(citations)

        # find first zone: number of articles accounting for a third of the citations
        n = -1
        cites = -1
        while cites<totalCites/3:

            n = n+1
            cites = cites + self.citations[n]

        # record values
        bradfordLim1 = n
#        citationLim1 = cites

        # find second zone: number of articles accounting for second third of citations
        while (cites < 2*totalCites/3) & (n<(len(self.citations)-1)):

            n = n+1

            cites = cites + self.citations[n]

        # record values
        bradfordLim2 = n
#        citationLim2 = cites

        # find the 'bradford multiplier', n: ratio of bddry values shoudl be approximately 1:n:n**2
        length = float(len(self.citations))
        try:
            ratios = [float(bradfordLim2)/float(bradfordLim1), length/float(bradfordLim2)]
        except ZeroDivisionError:
            ratios = [0,0]

    #    bradfordPc = [float(bradfordLim1)/length * 100., float(bradfordLim2)/length * 100.]

        return [bradfordLim1, bradfordLim2], ratios


    def hindex(self):

        ''' find the h index of a set of citations '''

        # arrange in order (largest to smallest)
        citations = np.sort(self.citations)
        citations = citations[::-1]

        # go through to the find h index
        n=0
        while (citations[n]>=n):
            n = n+1
            if n==len(citations):
                n = n+1
                break

        # return the correct value
        n = n-1
        return n

    def percentiles(self):
        ''' find and return some percentiles: 10, 25, 50, 75, 90 '''

        pcs = []
        # for a set of percentile values
        for pc in [10, 25,  50, 75, 90]:

            # find percentile
            pcs.append(np.percentile(self.citations, pc))

        return pcs


def strip(s):
    ''' Remove odd characters from the beginning and end of a string '''

    # characters to be removed
    ls = ['\n','\t', ' ']

    # remove from the beginning
    while s[0] in ls:
        s = s[1:]

    # remove from the end
    while s[-1] in ls:
        s = s[:-1]


    return s



if __name__=='__main__':

    ifc = impactFactor()

    fname = 'testIF.txt'
    numberOfPapersPublished = 10
    ifc.readData(fname)
    ifc.importDataFrame(fname)


    ifc.getIF(fname, 'journal', numberOfPapersPublished, metricType='TR')
    ifc.getIF(fname, 'journal', numberOfPapersPublished, metricType='MR1')
    ifc.getIF(fname, 'journal', numberOfPapersPublished, metricType='MR2')

    cites = [0,1,5,3,0,6,9,4,0]

    ifc.simpleIF(cites, len(cites), metricType = 'TR')
    ifc.simpleIF(cites, len(cites), metricType = 'MR1')
    ifc.simpleIF(cites, len(cites), metricType = 'MR2')
