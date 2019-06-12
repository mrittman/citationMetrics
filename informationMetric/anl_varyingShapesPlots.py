from numpy import *
import matplotlib.pyplot as plt


class plotVaryingData():

	def __init__(self):

		# parameters
		self.dataFileIn = 'varyingData.txt' # data from which to read data
		self.metrics = {}

	def loadData(self):


		## load data

		# get data from the file
		f = open(self.dataFileIn, 'r')
		data = f.readlines()

		# find the dictionary keys from first data row
		headings = data[0].split('\t')
		metricNames = headings[0:8]
		
		# initialize the output: dictionary containing metric data
		self.metrics = {}

		# initialize each dictionary entry
		for m in metricNames:
			self.metrics[m] = []

		# add data from each row
		for line in data[1:]:
			# turn row  into a list
			l = line.split('\t')[0:8]
			
			# add data from row to the output dictionary
			count = 0
			for m in metricNames:
				self.metrics[m].append(float(l[count]))
				
				count = count + 1
			
			
		return self.metrics


	def plotScatter(self, xName, yNames, saveFig = False):
		''' plot scatter plots of data

		Inputs:
		x = name from self.metrics to use as the x axis
		y = list of names from self.metric to use as y data
		saveFig = False or string giving filename to use

		'''
		
		plt.figure(figsize= [4,4])
	
		x = self.metrics[xName]
		y = []
		
		
		for n in yNames:
			plt.scatter(x, self.metrics[n], label=n, marker = "x")	

		# adjust parameters of plot
		plt.legend()
		
		plt.xlabel(xName)
		plt.ylabel("metric scores")
		plt.tight_layout()
		
		# save figures if necessary
		if saveFig != False:
			plt.savefig(saveFig + '.png', dpi = 600)
			

		
		plt.show()
		
	def getStats(self, labels, fileOut = False):
	
		if fileOut != False:
			f = open(fileOut, 'w')
	
		line = 'label\tmean\tstd dev\tvariance\tmedian\tmin\tmax'
		print(line)
		f.write(line + '\n')
		
		for l in labels:
			d = self.metrics[l]

			meanVal = mean(d)
			stdevVal = std(d)
			varVal = var(d)
			medianVal = median(d)
			minVal = min(d)
			maxVal = max(d)
			
			line = l + '\t' + str(meanVal) + '\t' + str(stdevVal) + '\t' + str(varVal) + '\t' + str(medianVal) + '\t' + str(minVal) + '\t' + str(maxVal)
			
			print(line)
			
			if fileOut!= False:
				f.write(line + '\n')
	
	
if __name__=="__main__":

	pvd = plotVaryingData()
	pvd.loadData()
	
	print(pvd.metrics.keys())
	
	pvd.plotScatter("expected avg cites", ["information", 'hindex', "hlim10", 'hlim1'], saveFig = "plot")
