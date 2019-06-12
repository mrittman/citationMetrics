import metricSimulations as ms
from numpy import *

m = ms.metrics()

m.citations = arange(10., dtype='float')


metrics = m.allMetrics([1.0, 100, 0.5],[1])

vals = metrics.keys()

for k in vals:

	print(k, metrics[k])
	
	

