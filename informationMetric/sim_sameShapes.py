import metricSimulations as ms
from numpy import *

cs = ms.citationSimulations()

shapeParams = 1.5 * ones (50)
journalSize = 100

cs.multiLogNormalSimulation(shapeParams, journalSize)