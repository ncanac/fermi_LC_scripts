"""

Performs a likelihood analysis for one time bin.

"""

import sys
import os
import gt_apps as apps
from UnbinnedAnalysis import *
from qC_utils import readConfig

def runFit(basename,directory,model,irfs,srcName,Emin,Emax):
    """
    Performs the fit using maximum likelihood estimation.
    """
    evtfile = directory + "/" + basename + "_filtered_gti.fits"
    SC = basename + "_SC.fits"
    expmap = directory + "/" + basename + "_expMap.fits"
    ltcube = directory + "/" + basename + "_ltcube.fits"
    
    obs = UnbinnedObs(eventFile=evtfile, scFile=SC, expMap=expmap,
    		expCube=ltcube, irfs=irfs)
    analysis = UnbinnedAnalysis(obs, srcModel=model, optimizer='NEWMINUIT')
    likeObj = pyLike.NewMinuit(analysis.logLike)
    analysis.fit(verbosity=0,covar=True,optObject=likeObj)
    num = int(directory[directory.find('bin')+3:])
    
    return "{:8d}{:14.4e}{:14.4e}{:10.4f}{:12.4f}{:12.2f}".format(num, \
    			analysis.flux(srcName,emin=100,emax=300000), \
                                analysis.fluxError(srcName,emin=100,emax=300000), \
                                analysis.model[srcName].funcs['Spectrum'].getParam('Index').value(), \
                                analysis.model[srcName].funcs['Spectrum'].getParam('Index').error(), \
                                analysis.Ts(srcName))

def main():
    basename = sys.argv[1]
    START_BIN = int(sys.argv[2])
    STOP_BIN = int(sys.argv[3])

    commonDict,analysisDict,likeDict,plotDict,curveDict = readConfig(basename)
    	
    cwd = os.getcwd()
    dirs = [dirname for dirname in os.listdir(cwd) if (os.path.isdir(os.path.join(cwd,dirname)) \
    		and "quickCurve" in dirname)][START_BIN:STOP_BIN]
    f = open('lc_results_' + str(START_BIN) + '-' + str(STOP_BIN-1) + '.txt','w')
    for directory in dirs:
    	f.write(runFit(basename,directory,curveDict['model'],commonDict['irfs'],likeDict['sourcename'], \
    	    analysisDict['emin'],analysisDict['emax']) + '\n')
    f.close()

if __name__ == '__main__':
    main()
