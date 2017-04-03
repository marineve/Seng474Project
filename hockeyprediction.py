#!/usr/bin/python

import argparse
import naivebayes as nb

parser = argparse.ArgumentParser()
parser.add_argument(
                '--train',
                nargs='*',
                required=True,
                help='A list of csv files containing training data')
parser.add_argument(
                '--test',
                required=True,
                help='A csv file containing testing data')
parser.add_argument('--result', help='The name of the result file with .csv ext')
args = parser.parse_args()

# Assign training data
training_data = args.train

# Assign testing data
testing_data = args.test

# Add the result file name
result_file_name = args.result

# Create a HockeyBayes instance and classify test data
predictor = nb.HockeyBayes(training_data)
predictor.classify_data(testing_data, result_file_name)
