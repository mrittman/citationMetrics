# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 17:27:15 2015

@author: Martyn Rittman

Generate a citation history for some papers

According to Golovosky ??

It combines several functions:

P = probability that a secondary paper cites a primary one
m = mean citation rate
M = number of primary references in a given year
r = average number of the first-generation citing papers cited by a second-generation citing paper

"""

from matplotlib import pyplot as plt
import numpy as np
import pandas as ps

class citationGenerator():
    
    def __init__(self):
        
        self.numPapers = 1 # number of papers to generate citations for
        self.p = 5.       # 'power' of article: equivalent to quality
        self.times = np.array([0.]) # array of times at which  to sample citations
        
        self.alpha_M = 0.046 # parameter for function M (primary references)
        self.beta_M = 0.02   # parameter for function M (primary references)
        self.gamma = 0.064   # per year
        self.Nratio = 1.5   # N = M/'N ratio'
        
        self.citations = []
        

    def multiCitations(self, filePrefix = 'citation'):
        ''' get citations for a number of papers '''

        rawCitations = []
        citations = []
        for n in range(self.numPapers):
#            fname = filePrefix + '_' + str(n) + '.txt'
            print(n)
            cites = self.getCitations()
            rawCitations.append(cites)
            citations.append(np.sum(cites))
            
#            f = open(fname,'w')
#            for c in cites:
#                f.write(str(c) + '\n')
#            f.close()
            
            
        self.citations = rawCitations
        return citations, rawCitations
        


    def getCitations(self):
        ''' main function for generating citations '''
        
        # ADD A CHECK THAT IT'S AN ARRAY
        times = self.times

        p = self.p #np.random.rand()

        # terms
        P0 = function_P0(times) # probability that a secondary paper cites a primary one
        m = function_m_interp(times) #, a_m) # mean citation rate
        M = function_M(times, self.alpha_M, self.beta_M, m) # number of primary references in a given year
        N = M/self.Nratio
        
        # records
        citations = [0]
        indirConts = [0]
        dirConts = [0]

        for t_ind in range(len(times)):
            
            t = times[t_ind]
            if t_ind ==0: 
                delta_t = times[0]
            else:
                delta_t = times[t_ind] - times[t_ind-1]
            
            directContribution = p * m[t_ind]
            # need to add variability in c - iterative

            # indirect contribution
            indirectContribution = 0.
            for s_ind in range(t_ind-1):
                s = times[s_ind]
                
#                lamdaA =  \sum_{\tau=0}^{t} P_{0}(k^{A}) e^{-\gamma(t-\tau)} N(t_ind-s) * citations[s]
                indirectContribution = delta_t * P0[s_ind] * np.exp(-self.gamma * (t-s)*delta_t) * N[t_ind-s_ind] * citations[s_ind]
#                indirectContribution = indirectContribution + add
                
       
            lamda = directContribution + indirectContribution
                    
#            # put a maximum limit on lamda
#            if lamda>100.:
#                lamda = 100.
            
#            print('lamda = ', lamda)
            citations.append(np.random.poisson(lamda))

            # record
            indirConts.append(indirectContribution)
            dirConts.append(directContribution)
            
        # save data if there is none
        if self.citations == []:
            self.citations = [citations]
            
        return citations
        
    def saveCitations(self, filename, pubDates = [], journalNames = []):
        ''' Save citations to file with columns:
        'date of citation'
            'date of publication'
            'journal' : journal of cited article, or equivalent corpus identifier
            'cited article' : ID of cited article, e.g. doi number'''
            
        # first line
        lines = [['date of citation', '\t', 'date of publication','\t', 'journal', '\t', 'cited article', '\n']]
        
        # prep for data if none entered
        
        # publication dates (of cited papers), all  set to 0
        if pubDates == []:
            pubDates = np.zeros(np.shape(self.citaions))
            
        # name of journal (all identical)
        if journalNames == []:
            journalNames = ['journal'] * np.shape(self.citations)[0]
        
        # put data to write into a list
        paperIndex = 0
        # iterate cited papers
        for paper in self.citations:
            # iterate time
            for t in range(len(self.times)):
                # iterate citations
                for cite in range(paper[t]):
                
                    # add a citation to the file
                    line = [ self.times[t], '\t', pubDates[paperIndex], '\t', journalNames[paperIndex], '\t', paperIndex, '\n']
                    
                    lines.append(line)
                
            paperIndex = paperIndex + 1
            
        # write to file
        f = open(filename, 'w')
        for l in lines:
            for d in l:
                f.write(str(d))
                
        f.close()
        
    
def function_T(x, T0, gamma):
    
    ''' number of indirect references brought in by each direct reference 
    
        x is an array, T0 and gamma are floats. 
        
        From Golovosky, T0=6.6, gamma = 0.64 per year
    
    '''
    
    T = T0 * np.exp(-gamma * (x-1))
    
    
    return T
    
    
def function_M(x, alpha, beta, m):

    ''' M is the number of primary references in a given year
    
        x is an array, alpha and beta are floats. 
    
        From Golovosky, alpha=0.046, beta = 0.02 for physics papers
        
    '''

    m = function_m_interp(x)
    M = m * np.exp(-(alpha+beta)*x)
    
    return M
    
    
def function_r(x):
    
    ''' 1 + 0.11 log k + 0.033(log k) 2

    an average number of the first-generation citing papers cited by a
    second-generation citing paper
    
    '''
    
    r = 1. + 0.11*np.log(x) + 0.033*np.log(x)**2

    # make sure the first step has no contribution
    r[0]=0    
    
    return r
    
def function_m(times, s, c, r):
    
    ''' mess around to find a good esimation
    
    x = time
    c = ?? some parameter
    
    '''
    
#    x = times
    
#    # Novelty
#    n = 3
#    N = 1./(x+1)**n  
   
    
    # "findability"
#    s = 0.7
    F1 = 1./(x+1)**s # new and interesting, so top of the results, but fades with time
#    r = 1.
    F2 = r-r*np.exp(-(x)/c) # gradual increase of interest with time
    
    m = F2*F1
    
    return m
    

def function_m_interp(x):
    
    ''' method for calculating m by interpolating data from Golobosky
    
        x is times '''
    
    g_vals = ps.read_csv('Citation_rate_physics_1984.csv', sep=';')
    
    y = np.interp(x, g_vals['year after publication'], g_vals['direct cite rate'])
    
    return y
    
    
def function_P0(x):
    
    ''' the probability that a second generation citing paper cites the parent paper (indirectly) '''
    
    a = 0.16
    b = 3.
    r = function_r(x)    
    
    P0 = a * (1. + b*(r - 1.))
    
    return P0

        
if __name__=='__main__':
    
    x = np.arange(0., 5.)
    
#    m = function_m(1, x)
#    T = function_T(x, 6.6, 0.64)
#    M = function_M(x, 0.046, 0.02)
#    r = function_r(x)
#    m = function_m(x,1.1)
#    P0 = function_P0(x)
#    m_int = function_m_interp(x)
#    
#    plt.plot(x,m, color='black')
#    plt.plot(x, T)
#    plt.plot(x, M)
#    plt.plot(P0)
#    plt.plot(r)
#    plt.plot(x, m_int)
    
    cg = citationGenerator()
    cg.times = x
    cg.numPapers = 30000
    cg.p = 3.
#    cites = cg.getCitations()
    cites, rawCites = cg.multiCitations()
    print(cites)

    # equally spaced publication dates    
    maxDate = 3.
    gap = maxDate/(cg.numPapers-1)
    pubDates = np.arange(0., maxDate + gap/2., gap)
    
    cg.saveCitations('cites.txt', pubDates = pubDates)
    
#    plt.plot(x, cites)  
#    plt.figure()     
#    plt.plot(cites, 'bx')
    plt.figure()
    plt.hist(cites)
#    
#    
    # write to file
    f = open('testCites.txt', 'w')
    for d in cites:
        line = str(d)  + '\n'
        f.write(line)
    f.close()
#    

#    
#    # write raw data to file
    
    
    ## interpolationCheck
#    interpVals = function_m_interp(x)
#    
#    g_vals = ps.read_csv('Citation_rate_physics_1984.csv', sep=';')
#
#    plt.figure()
#    plt.plot(x, interpVals)
##    plt.plot(x, g_vals, 'rx')
#
    plt.show()









