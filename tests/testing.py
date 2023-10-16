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

    print("Extracting features from: " + dataFile)

    data = [line.rstrip().split(' ') for line in open(dataFile)]
    flat_data = [float(item) for sublist in data for item in sublist]

    # Run catch22
    catch22_res = pycatch22.catch22_all(flat_data,catch24 = doCatch24,short_names = short_names)

    # Print the results
    print(catch22_res)
