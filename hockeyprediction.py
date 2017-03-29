#!/usr/bin/python

import naivebayes as nb
import sys


def main(argv):
    # Assign user-input files for testing and classification
    test_data = argv[0]
    class_data = argv[1]

    # Create a HockeyBayes instance and classify data
    predictor = nb.HockeyBayes(test_data)
    predictor.classify_data(class_data)

if __name__ == "__main__":
    # Command line arguments:
    #   testing_data: csv file containing test data
    #   class_data: the data file to be classified
    #   result: the result file containing team name and standing
    if len(sys.argv) == 3:
        main(sys.argv[1:])
    else:
        print 'Two files are required: one for testing, and one for classifying'
        exit(-1)
