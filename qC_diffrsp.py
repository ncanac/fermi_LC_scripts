"""

Calculates the expected photon distribution for a given source model.
This distribution is the convolution of the source mode with the instrument
response function.

"""

import sys
import os
from multiprocessing import Pool
import gt_apps as apps
from qC_utils import readConfig

def rundiffResps(params):
    """
    Calculates the expected photon distribution using Fermi tool gtdiffrsp.
    params[0] = directory
    params[1] = xml model file
    params[2] = instrument response functions
    params[3] = basename
    """
    basename = params[3]
    apps.diffResps['evfile'] = params[0] + "/" + basename + "_filtered_gti.fits"
    apps.diffResps['scfile'] = basename + "_SC.fits"
    apps.diffResps['srcmdl'] = params[1]
    apps.diffResps['irfs'] = params[2]
    apps.diffResps['chatter'] = 0
    apps.diffResps.run()

def main():
    basename = sys.argv[1]
    commonDict,analysisDict,likelihoodDict,plotDict,curveDict = readConfig(basename)
    
    cwd = os.getcwd()
    dirs = [dirname for dirname in os.listdir(cwd) if (os.path.isdir(os.path.join(cwd,dirname)) and "quickCurve" in dirname)]
    params = zip(dirs,[curveDict['model']]*len(dirs),[commonDict['irfs']]*len(dirs),[basename]*len(dirs))
    
    pool = Pool(processes=int(commonDict['multicore']))
    pool.map(rundiffResps,params)
    pool.close()

if __name__ == '__main__':
    main()
