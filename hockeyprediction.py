#!/usr/bin/python

import naivebayes as nb
import sys

data_file = 'season_data2.xlsx'

def get_data():
    return [
        ['Points', '+/-', 'PP%', 'CORSI%', 'Top 20', 'Playoff Finish'],
        ['8', '8', '8', '8', '8', '0'],
        ['2', '2', '2', '2', '2', '4'],
        ['1', '1', '1', '1', '1', 'SC'],
        ['4', '4', '4', '4', '4', '1'],
        ['5', '5', '5', '5', '5', '2'],
        ['6', '6', '6', '6', '6', '3']
    ]

def main(argv):
    # Assign user-input values
    instance = argv[0]
    class_value = argv[1]
    if class_value in nb.classes[1]:
        # Create a HockeyBayes instance
        data = get_data()
        predictor = nb.HockeyBayes(data, instance)

        # Find probabilities
        probability = predictor.find_prob_class_given_evidence(class_value)

        # Output the probability to the user
        print probability

if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1:])
    else:
        exit(-1)
