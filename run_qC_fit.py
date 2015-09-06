"""

Calls qC_fit.py to calculate fit in parallel using n subprocesses, where
n is the number of cores specified in the configuration file.

"""

import subprocess
import ConfigParser
import sys
import os
import gt_apps as apps
import math
import fileinput
from qC_utils import readConfig

def splitList(l,n):
    """
    Returns list split up in n chunks.
    """
    n = max(1,n)
    return [l[i:i + n] for i in range(0,len(l),n)]

def writeResults():
    """
    Concatenate all lc_results_*.txt text files into one lc_results.txt file.
    """
    filenames = [fname for fname in os.listdir(os.getcwd()) if "lc_results" in fname]
    results = []
    for line in fileinput.input(filenames):
        results.append(line)
    with open('lc_results.txt','w') as f:
        f.write("# Col[1] = time bin\n" + \
                "# Col[2] = flux\n" + \
    	    "# Col[3] = flux error\n" + \
    	    "# Col[4] = index\n" + \
    	    "# Col[5] = index error\n" + \
    	    "# Col[6] = TS value\n")
        for line in sorted(results):
            f.write(line)
    for fname in filenames:
        subprocess.call(['rm',fname])	

def main():
    basename = sys.argv[1]

    commonDict,analysisDict,likeDict,plotDict,curveDict = readConfig(basename)
    cwd = os.getcwd()
    dirs = [dirname for dirname in os.listdir(cwd) if (os.path.isdir(os.path.join(cwd,dirname)) \
        	and "quickCurve" in dirname)]
    bin_nums = range(len(dirs))
    chunk_size = int(math.ceil(len(dirs)/float(commonDict['multicore'])))
    processes = []
    for chunk in splitList(bin_nums,chunk_size):
    	processes.append(subprocess.Popen(['python','qC_fit.py',basename,str(chunk[0]),str(chunk[-1]+1)]))
    for p in processes:
    	p.wait()
    writeResults()

if __name__ == '__main__':
	main()
