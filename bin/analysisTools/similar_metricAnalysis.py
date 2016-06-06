# -*- coding: utf-8 -*-
"""
Created on Tue May 10 15:57:36 2016

@author: galileo
"""

import metricAnalysis

ma = metricAnalysis.analysis()
folder = "/home/galileo/Dropbox/smart laptop/impactFactor/metricMetrics/bin/results analysis/similar/"
ma.plotFolder = folder + 'plots/'
ma.outname = folder + 'similarMetricAnalysis.txt'

ma.inputfilename = folder + "similarMetrics.txt"

ma.getData()
ma.writeSummaryFile()
ma.boxPlots()