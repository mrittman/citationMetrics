from numpy import *
from matplotlib import pyplot as plt
from scipy.stats import lognorm
import os
from metrics import metrics


class citationSimulations():
	''' class to run some simulations and generate output of metrics '''
	
	def __init__(self):
		
		self.metfn = metrics() # function to calculated maetrics
		
		# parameters to initialise the information metric
		self.infoMetShape = 1. # assumed shape for output
		self.metfn.initInfoMetric(self.infoMetShape)
		self.metfn.IMavgcite  = 5 # weighting for information function
		
		# parameters for calculating the information metric
		self.avgCitesPerPaper = 20
		self.totalPapers = 20000
		
		
	def saveCitations(self, filename):
		
		''' Save self.citations to file '''
		
		f = open(filename, 'w')
		
		for c in self.metfn.citations:
			f.write(str(c)+ '\n')
			
		f.close()
		
	
	def plotRange(self, minVal, maxVal, interval):
		''' plot values of metrics in a range '''
		
		# range of citation values
		xVals = arange(minVal, maxVal, interval)
		m = metrics()
		m.citations = xVals
	
		# initialise information metric
		
		m.initInfoMetric(self.infoMetShape, maxCites = maxVal)
		infoMet = m.informationMetric()

			
			
		print(infoMet)


		plt.plot(xVals, infoMet, 'rx')


		plt.show()
		
		
	def logNormalSimulation(self, shapeParameter, journalSize):
		''' simulate data using the log normal distribution and calculate metrics

			shapeParameter = parameter for lognormal distribution
			journalSize = number of 'papers' for which to generate number of citations

			returns a dictionary of metrics: information, impact factor, and random

		''' 
		
		# sample lognormal distribution to get number of citations
		self.metfn.citations = floor(lognorm.rvs(shapeParameter, size = journalSize))
		
		print(self.metfn.citations)
		
		# calcluate metrics
		metrics = self.metfn.allMetrics([2., 15000, 0.5], [1,10])
		
		return metrics
		
	def multiLogNormalSimulation(self, shapeParams, journalSize):
		''' Multiple simulations of log normal distributed citations and metric calculates 
		
			Inputs are set at the beginning of the function.
			
			Outputs are a file (multiLogSimulation.csv) containing details of each simulation and files containing citations simulated for each metric generated.
		
		'''
		
		#### run the simulations and save data
		
		## open file to write output to
		f = open('multiLogSimulations.csv', 'w')
		# first line (column headers)
		#f.write("shape parameter\tinformation\timpact factor\trandom\tjournal size\tInfoMet shape\tInfoMet avg cites\n")
		
		## calculate the metrics for each condition
		count = 0
		for s in shapeParams:
			metrics = self.logNormalSimulation(s, journalSize)
			
			metricNames = list(metrics.keys())
			print(metricNames)
			metricNames.sort()
			
			# write column headers
			if count == 0:
				line = "shape parameter"
				# assemble names of metrics
				for m in metricNames:
					line = line + '\t' + m
				line = line + '\n'
				f.write(line)
			
			
			lineout = str(s)
			
			
			for k in metricNames:
				lineout = lineout + '\t' + str(metrics[k])
			lineout = lineout + '\n'
			
			print(lineout)
			
			# save metrics			
			f.write(lineout)

			
			# save citations
			citationsFilename = 'citations ' + str(s) + ' ' + str(count) + '.txt'
			g = open(citationsFilename, 'w')
			for c in self.metfn.citations:
				g.write(str(c) + '\n')
				
			g.close()
			
			count = count + 1
			
		f.close()	
		
		
class metricCalculations():
	
	def __init__(self):
	
		# class instance to calcluate metrics
		self.metfn = metrics()
		self.metfn.citations = range(5)
		
	def loadData(self, citationfilename):
		''' Load data from a text file '''
		
		f = open(citationfilename, 'r')
		
		data = f.readlines()
		
		citations = []
		for d in data:
			citations.append(float(d))
			
		print(citations)
		
		self.metfn.citations = citations
		
	def calculateMetrics(self):
		''' Output various metrics '''
				
		metrics = {}
		
		# h index
		metrics['hindex'] = self.metfn.hindex()
		
		# impact factor
		metrics['impact factor'] = self.metfn.impactFactor()
		
		# information metric
		self.metfn.initInfoMetric(2.) # shape parameter is the variable
		metrics['information'] = self.metfn.informationMetric()
		
		# h0 metric
		metrics['h1'] = self.metfn.hlim(1)
		
		# h10 metric
		metrics['h10'] = self.metfn.hlim(10)
		
		print(metrics)
		
		return metrics
		
	def loadAndCalculate(self, folder, fileOut):
		''' load files from a folder and calculate metrics for each entry '''
		
		files = os.listdir(folder)
		print(files)
		
		g = open(fileOut, 'w')
		g.write('file\timpact factor\tinformation\th index\th1\th10\n')
		
		for file in files:
			
			if 'citations' in file:
				
				# load data
				longname = folder + '/' + file
				print(longname)
				f = open(longname, 'r')
				data = f.readlines()
				
				citations = []
				for d in data:
					citations.append(float(d))
					
				self.metfn.citations = citations
				
				f.close()
				
				# calculate metrics
				metrics = self.calculateMetrics()
				
				# save data
				g.write(folder + file + '\t' + str(metrics['impact factor']) + '\t' + str(metrics['information']) + '\t' + str(metrics['hindex']) + '\t' + str(metrics['h1']) + '\t' + str(metrics['h10']) + '\n')
	

	def varyInfoMetric(self, citationFilename, outputfilename):
		''' Look at the effect of varying the underlying PDF on the information metric using the same citation data '''
		
		# load the citation data
		self.loadData(citationFilename)
		
		# calculate different information metric values
		shapeParams = [0.10000, 1.17741, 1.48230, 1.66511, 1.79412, 1.89302, 1.97277, 2.03933, 2.09629, 2.14597, 2.18993, 2.22931, 2.26493, 2.29741, 2.32725, 2.35482, 2.38043, 2.40432, 2.42670, 2.44775]
		
		g = open(outputfilename, 'w')
		
		for s in shapeParams:
			self.metfn.initInfoMetric(s, maxCites = 1000)
			
			info = self.metfn.informationMetric()
			
			g.write(str(s) + '\t' + str(info) + '\n')
			
		g.close()
			


		# save to file


if __name__ == "__main__":  
	
	# m = metrics()
	
#	m.citations = arange(10)
#	print(m.citations)
#	
#	m.hindex()
#	
#	m.hlim(5)
	
	
	# m.hindexExpectation(2, [0, 10], 50)
	
	# impactfactor = m.impactFactor()
	# print(impactfactor)
		
	# m.initInfoMetric(2, avgCites = 10, maxCites = 1000)
	# info = m.informationMetric()
	# print(info)
	
	# randMet = m.randomCitation()
	# print(randMet)
	
	# cs = citationSimulations()
	
	# cs.plotRange(0,100,10)
	# cs.logNormalSimulation(1.5, 500)
	
 	#cs.saveCitations('citations.txt')
	#cs.multiLogNormalSimulation()

	mc = metricCalculations()
	
	mc.calculateMetrics()
	
#	folder = 'data/2019-06-28'
	
#	mc.loadAndCalculate(folder, 'additionalMetrics.txt')
	
	mc.varyInfoMetric('citations.txt', 'varyinfo.txt')
	
	
	
