import pycatch22
import os

# Whether to compute the mean and standard deviation:
doCatch24 = True

# Whether to also include short names:
short_names = True

# The two data files
testData = [os.path.join("tests", "testData1.txt"),
            os.path.join("tests", "testSinusoid.txt")]

# Extract features from each data file in testData
for dataFile in testData:

    print ('\n'), dataFile

    data = [line.rstrip().split(' ') for line in open(dataFile)]
    flat_data = [float(item) for sublist in data for item in sublist]

    catchOut = pycatch22.catch22_all(flat_data,catch24 = doCatch24,short_names = short_names)

    featureNames = catchOut['names']
    featureNamesShort = catchOut['short_names']
    featureValues = catchOut['values']

    for featureName, featureNameShort, featureValue in zip(featureNames, featureNamesShort, featureValues):
        print('%s (%s) : %1.6f' % (featureName, featureNameShort, featureValue))
