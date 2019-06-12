import anl_varyingShapesPlots as vsp

fn = vsp.plotVaryingData()

fn.dataFileIn = 'varyingData.txt'
fn.loadData()

xdata = "expected avg cites"
ydata = ['impact factor', 'hindex', 'hlim1', 'hlim10', 'information', 'random']
labels = ['impactfactor', 'h index', 'h1', 'h10', 'information', 'random']

## plot
ii = 0
for y in ydata:
	figureName = ' fig_vary_' + labels[ii]
	fn.plotScatter(xdata, [y], saveFig = figureName)

	ii = ii + 1
