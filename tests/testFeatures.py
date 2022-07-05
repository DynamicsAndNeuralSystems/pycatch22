import os
import pandas as pd
import pycatch22

#-------------------------------------------------------------------------------
def giveMeFeatureVector(tsData):
    '''
    Returns a catch-22 feature vector from input time-series data
    '''
    features = dir(pycatch22)
    features = [item for item in features if not '__' in item]

    featureVector = []
    for testFun in features:
        featureFun = getattr(pycatch22,testFun)
        featureVector.append(featureFun(tsData))

    return featureVector

#-------------------------------------------------------------------------------

x = pd.read_csv('test.txt',header=None);
tsData = x[0].values.tolist()
fV = giveMeFeatureVector(tsData)
