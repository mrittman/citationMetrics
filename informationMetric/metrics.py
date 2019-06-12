#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 07:12:23 2019

@author: martyn

A script to calculate various kinds of citation metrics.

"""

from numpy import *
from scipy.stats import lognorm

class metrics():
	''' Class to calculate several types of metric from a list of citations '''	
	
	def __init__(self):
		''' initial settings '''
		
		self.citations = [] # list of citations from which to calculate metric
		self.citationweightings =[] # list of possible weightings of citations, probably not used
		
		# settings for information metric
		self.IMscores = [-1]
		self.IMavgcites = 0
		
	def allMetrics(self, infoParams, hlimValues):
		''' Calculate values of all metrics and return as a dictionary
			
			Inputs:
			
			infoParams = [shapeParam, maxCites, zeroPapers]
			hlimValues = tuple of values for which to calculate hlim
			
			Outputs:
			
			metrics = dictionary containing: 
				information
				impact factor
				h index
				hlimX where X is the values in hlimValues				

		'''
	
		metrics = {}
		
		self.initInfoMetric(infoParams[0], maxCites = infoParams[1], zeroPapers = infoParams[2])
		
		metrics['impact factor'] = self.impactFactor()
		metrics['information'] = self.informationMetric()
		metrics['random'] = self.randomCitation()
		metrics['hindex'] = self.hindex()
		
		for lim in hlimValues:
			name = 'hlim' + str(lim)
			
			metrics[name] = self.hlim(lim)
		
		return metrics
		
	
		
	def initInfoMetric(self, shapeParam, maxCites=50000, zeroPapers = 0.5):
		''' Find the lookup table for the information metric

		shapeParam = shape parameter for assumed log normal distribution
		maxCites = maximum number of citations for which lookup table is calculated
		zeroPapers = fraction of papers with no citations
		self.avgCites = average cites per paper, used for scaling; set to 0 for no scaling

		'''
		
		cites = arange(maxCites, dtype='float')
		
		# generate lognormal values for each
		citeProbabilities = lognorm.pdf(cites, shapeParam)
		
		# find ratios
		citeRatios = zeros(shape(citeProbabilities))
		citeRatios[2:] = citeProbabilities[2:]/citeProbabilities[1:-1]
		citeRatios[1] = 1. - zeroPapers
		
		# cumulative ratios
		information = zeros(shape(citeProbabilities))
		information[1:] = log2(1./citeRatios[1:])
		information[0] = 0.
		
		self.IMscores = cumsum(information)

		
		# scaling using avg cites per paper
		if self.IMavgcites != 0:
			self.IMscores = self.IMscores/self.IMscores[self.IMavgcites]

		
	def impactFactor(self):
		''' calculation of the impact factor a la Clarivate or Scopus '''
		
		metric = mean(self.citations) # calculate the average of the citations
		
		return metric
		
	def informationMetric(self):
		''' calculate a metric based on information theory 
		
			returns value of information metric
		
		'''
		
		if self.IMscores[0] == -1:
			print("run initInfoMetric before informationMetric")
			
			return -1

		scores = []
		for c in self.citations:
			# find probability by referencing the logNormal distribution ratios 
			scores.append(self.IMscores[int(c)])

		return mean(scores)
		
		
	def randomCitation(self):
		''' a metric that returns one number from the input array at random '''

		# Generate a random index from the input array		
		x = random.rand()*len(self.citations) # generate a random number
		x = int(x) # equivalent to floor function, finds index to choose as the metric output
		
		return self.citations[x] # return the value from the input array corresponding to the index generated


	def hindex(self):
		''' Calculate the h index '''
		
		# put into ascending order
		sortedCites = sort(self.citations)[::-1]
		
		count = 0
		while (count < sortedCites[count]):
		
			# simple iteration
			print(count, sortedCites[count])
			count = count + 1
			
			# case where the index runs out of citations
			if count == len(sortedCites - 1):
				count = len(sortedCites)
				break
		
		return count
		
	def hlim(self, limit):
		''' Calcualte the fraction of citations that are at least limit '''
		
		geq = greater_equal(self.citations, limit)
		
		metric = float(sum(geq))/float(len(geq))
		
		return metric
		
		
	def hlimExpectation(self, limit, shapeParameter):
		''' Calculate the expectation of the hlim metric using the cumulative log normal distribution density
		
		limit is the value used for the hlim function, i.e. calculated % of papers with 'limit' citations
		shapeParameter is the parameter of the log normal distribution.


		'''
		
		# survival function = 1 - cumulative probability
		prob = lognorm.sf(limit, shapeParameter) 
		
		return prob
		
	def hindexExpectation(self, shapeParameter, searchrange, journalSize):
		''' Looks in range to find the expected value of the h index given a log normal distribution 
		
		shapeParameter is the shape parameter of the log normal distribution
		searchrange is a tuple of integers [a,b] giving minimum/maximum possible values for the h index
		journalSize is the number of papers in the dataset
		
		'''
		
		values = range(searchrange[0], searchrange[1])
		
		# very simple search function to solve the equation
		for n in values:
			hfn = lognorm.sf(n, shapeParameter) - float(n)/float(journalSize)
			
			if hfn < 0:
				break
				
		print(n)
		return n



if __name__=="__main__":

	m = metrics()
	m.IMavgcites = 5

	m.initInfoMetric(1., maxCites = 10)