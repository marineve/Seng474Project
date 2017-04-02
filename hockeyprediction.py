#!/usr/bin/python

import naivebayes as nb
import sys


def main(argv):
    # Assign user-input files for testing and classification
    training_data = argv[0]
    testing_data = argv[1]

    # Create a HockeyBayes instance and classify data
    predictor = nb.HockeyBayes(training_data)
    predictor.classify_data(testing_data)

if __name__ == "__main__":
    # Command line arguments:
    #   training_data: csv file containing training data
    #   test_data: the data file to be classified
    #   result: the result file containing team name and standing
    if len(sys.argv) == 3:
        main(sys.argv[1:])
    else:
        print 'Two files are required: one for testing, and one for classifying'
        exit(-1)
