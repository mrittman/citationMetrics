import metricSimulations as ms

cs = ms.citationSimulations()

shapeParams = [0.10000, 1.17741, 1.48230, 1.66511, 1.79412, 1.89302, 1.97277, 2.03933, 2.09629, 2.14597, 2.18993, 2.22931, 2.26493, 2.29741, 2.32725, 2.35482, 2.38043, 2.40432, 2.42670, 2.44775]
journalSize = 100

cs.multiLogNormalSimulation(shapeParams, journalSize)