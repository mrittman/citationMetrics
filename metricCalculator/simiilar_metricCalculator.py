# -*- coding: utf-8 -*-
"""
Created on Mon May 30 17:49:41 2016

@author: galileo
"""

import citationSimulator as cs

mc = cs.citationSimulator()
mc.fstoch = "testCites 0-3.txt"

mc.journalSizes = [10, 100, 500, 1000, 5000]

mc.folder = "/home/galileo/Dropbox/smart laptop/impactFactor/metricMetrics/bin/results data/similar/"
mc.metricsFile = "similarMetrics.txt"

mc.simDataFromFile()
mc.getMetrics()
mc.saveMetrics()