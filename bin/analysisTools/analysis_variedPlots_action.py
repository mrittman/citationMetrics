# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 12:50:59 2016

@author: galileo
"""

import analysis_variedPlots_dict as avp

pm = avp.plotMarker()

folder = '/home/galileo/Dropbox/smart laptop/impactFactor/metricMetrics/bin/results/varied/'    
figFolder = folder + 'plots_jsize100/'
pm.inputfile = folder + 'variedMetrics100.txt'
outputfile = folder + 'varied_values.csv'
pm.loadData()

filterOptions = [{'distribution':'flat', 'metric':'BF1'},
{'distribution':'lognorm', 'metric':'BF1'},
{'distribution':'mean', 'metric':'BF1'},
{'distribution':'pareto', 'metric':'BF1'},
{'distribution':'stoch', 'metric':'BF1'},
{'distribution':'stoch_varied', 'metric':'BF1'},
{'distribution':'flat', 'metric':'BF2'},
{'distribution':'lognorm', 'metric':'BF2'},
{'distribution':'mean', 'metric':'BF2'},
{'distribution':'pareto', 'metric':'BF2'},
{'distribution':'stoch', 'metric':'BF2'},
{'distribution':'stoch_varied', 'metric':'BF2'},
{'distribution':'flat', 'metric':'BR1'},
{'distribution':'lognorm', 'metric':'BR1'},
{'distribution':'mean', 'metric':'BR1'},
{'distribution':'pareto', 'metric':'BR1'},
{'distribution':'stoch', 'metric':'BR1'},
{'distribution':'stoch_varied', 'metric':'BR1'},
{'distribution':'flat', 'metric':'BR2'},
{'distribution':'lognorm', 'metric':'BR2'},
{'distribution':'mean', 'metric':'BR2'},
{'distribution':'pareto', 'metric':'BR2'},
{'distribution':'stoch', 'metric':'BR2'},
{'distribution':'stoch_varied', 'metric':'BR2'},
{'distribution':'flat', 'metric':'EX1'},
{'distribution':'lognorm', 'metric':'EX1'},
{'distribution':'mean', 'metric':'EX1'},
{'distribution':'pareto', 'metric':'EX1'},
{'distribution':'stoch', 'metric':'EX1'},
{'distribution':'stoch_varied', 'metric':'EX1'},
{'distribution':'flat', 'metric':'H'},
{'distribution':'lognorm', 'metric':'H'},
{'distribution':'mean', 'metric':'H'},
{'distribution':'pareto', 'metric':'H'},
{'distribution':'stoch', 'metric':'H'},
{'distribution':'stoch_varied', 'metric':'H'},
{'distribution':'flat', 'metric':'MR1'},
{'distribution':'lognorm', 'metric':'MR1'},
{'distribution':'mean', 'metric':'MR1'},
{'distribution':'pareto', 'metric':'MR1'},
{'distribution':'stoch', 'metric':'MR1'},
{'distribution':'stoch_varied', 'metric':'MR1'},
{'distribution':'flat', 'metric':'MR2'},
{'distribution':'lognorm', 'metric':'MR2'},
{'distribution':'mean', 'metric':'MR2'},
{'distribution':'pareto', 'metric':'MR2'},
{'distribution':'stoch', 'metric':'MR2'},
{'distribution':'stoch_varied', 'metric':'MR2'},
{'distribution':'flat', 'metric':'P50'},
{'distribution':'lognorm', 'metric':'P50'},
{'distribution':'mean', 'metric':'P50'},
{'distribution':'pareto', 'metric':'P50'},
{'distribution':'stoch', 'metric':'P50'},
{'distribution':'stoch_varied', 'metric':'P50'},
{'distribution':'flat', 'metric':'TR'},
{'distribution':'lognorm', 'metric':'TR'},
{'distribution':'mean', 'metric':'TR'},
{'distribution':'pareto', 'metric':'TR'},
{'distribution':'stoch', 'metric':'TR'},
{'distribution':'stoch_varied', 'metric':'TR'}]



#fitVals = []
for f in filterOptions:
    pm.filterData(f)
    title = f['distribution'] + ' ' + f['metric']
    print(title)
    pm.plotData(title)
    avp.plt.savefig(figFolder + title + '.png')
    
#    (grad, err) = pm.fitData()
#    fitVals.append([title, grad, err])    
#    
#print(fitVals)

#g = open(outputfile, 'w')
#print(outputfile)
#g.write('name' + '\t' + 'gradient' + '\t' + 'error' +  '\n')
#for v in fitVals:
#    line = v[0] + '\t'+ str(v[1]) + '\t' + str(v[2]) + '\n'
#    g.write(line)
    
    
g.close()
    
  