import ConfigParser

def readConfig(basename):
    """
    Reads in the configuration file.
    """
    commonDictionary = {}
    analysisDictionary = {}
    likelihoodDictionary = {}
    plotDictionary = {}
    curveDictionary = {}
    
    config = ConfigParser.RawConfigParser()
    config.read(basename+'.cfg')
    
    if(config.has_section('common')):
    	commonDictionary = dict(config.items('common'))
    	if(commonDictionary['binned'] in ['True', 'true', '1', 'yes']):
    	    commonDictionary['binned'] = True
    	else:
    	    commonDictionary['binned'] = False
        
    if(config.has_section('quickAnalysis')):
    	analysisDictionary = dict(config.items('quickAnalysis'))
    
    if(config.has_section('quickLike')):
    	likelihoodDictionary = dict(config.items('quickLike'))
    
    if(config.has_section('quickPlot')):
    	plotDictionary = dict(config.items('quickPlot'))
    
    if(config.has_section('quickCurve')):
    	curveDictionary = dict(config.items('quickCurve'))
    	if( curveDictionary['sliding'] in ['True', 'true', '1', 'yes']):
  	    curveDictionary['sliding'] = True
    	else:
       	    curveDictionary['sliding'] = False
    
    return commonDictionary,analysisDictionary,likelihoodDictionary,plotDictionary,curveDictionary

