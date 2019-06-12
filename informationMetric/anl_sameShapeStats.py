import anl_varyingShapesPlots as vsp

fn = vsp.plotVaryingData()

fn.dataFileIn = "data_sameShape.csv"
fn.loadData()

fn.getStats(['impact factor', 'hindex', 'hlim1', 'hlim10', 'information', 'random\n'], fileOut = 'stats_sameShape.txt')