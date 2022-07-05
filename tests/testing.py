import pycatch22
import os

# Whether to compute the mean and standard deviation:
doCatch24 = True

# The two data files
testData = [os.path.join("tests", "testData1.txt"),
            os.path.join("tests", "testSinusoid.txt")]

# Extract features from each data file in testData
for dataFile in testData:

    print ('\n'), dataFile

    data = [line.rstrip().split(' ') for line in open(dataFile)]
    flat_data = [float(item) for sublist in data for item in sublist]

    catchOut = pycatch22.catch22_all(flat_data,catch24 = doCatch24)

    featureNames = catchOut['names']
    featureValues = catchOut['values']

    for featureName, featureValue in zip(featureNames, featureValues):
        print('%s : %1.6f' % (featureName, featureValue))
