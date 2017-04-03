import csv

attributes = ['points', '+/-', 'pp%', 'corsi%', 't20', 'ploffs']
classes = ['0', '1', '2', '3', '4', 'SC']
num_attribute_values = {
    'points': 6,
    '+/-': 7,
    'pp%': 2,
    'corsi%': 5,
    't20': 4,
    'ploffs': len(classes),
}

class HockeyBayes:
    """This class uses Naive Bayes algorithm to classify hockey statistics."""
    def __init__(self, training_data):
        """Initilizes a HockeyBayes instance.

        Args:
            training_data (file): A csv file containing training data.
        """
        self._training_data = []
        for training_file in training_data:
            data = self.get_csv_data(training_file)
            modified_data = self.transform_data(data)
            self._training_data.extend(modified_data)

    def classify_data(self, test_data, result_file_name=None):
        """Classify test data with the training data.

        Args:
            test_data (file): A csv file containing the test data to be classified.
            result_file_name (str): An optional result file name.
        """
        testing_data = self.transform_data(self.get_csv_data(test_data))

        # Set up the results list
        results = [['team']]
        results[0].extend(classes)

        # Classify test data
        for instance in testing_data:
            # Send all test data except the last column, which contains what
            # we're attempting to classify
            probabilities = self.find_prob_class_given_evidence(instance[:-1])

            # Add the team name
            all_probs = [instance[0]]

            # Append the probabilities and add it to the results list
            for val in classes:
                all_probs.append(probabilities[val])
            results.append(all_probs)

        # Write the results to a csv file
        result_csv = self.write_csv_data(results, result_file_name)

    def get_csv_data(self, data_file):
        """Extract data from a csv file.

        Args:
            data_file: File containing data in csv format.

        Returns:
            list: A list of lists containing hockey data
        """
        with open(data_file, 'rb') as f:
            reader = csv.reader(f)
            return list(reader)

    def write_csv_data(self, data, file_name):
        """Write data to a csv file.

        Args:
            data (list): A list of lists to write to a file.
        """
        if file_name is None:
            file_name = 'result.csv'
        with open(file_name, 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(data)

    def transform_data(self, data):
        """Transform data into usable form using thresholds.

        Args:
            data (list): A list of lists containing raw data.

        Returns:
            list: A list of lists containing the processed data.
        """
        team_index = data[0].index('team')
        points_index = data[0].index('points')
        gf_index = data[0].index('gf')
        ga_index = data[0].index('ga')
        pp_percent_index = data[0].index('pp%')
        corsi_percent_index = data[0].index('corsi%')
        t20_index = data[0].index('t20')
        ploffs_index = data[0].index('ploffs')

        processed_data = []
        for instance in data[1:]:
            # Replace values with threshold values
            # Transform Points
            points_val = float(instance[points_index])
            if points_val < 70:
                points = '<70'
            elif 70 <= points_val < 80:
                points = '>=70'
            elif 80 <= points_val < 90:
                points = '>=80'
            elif 90 <= points_val < 100:
                points = '>=90'
            elif 100 <= points_val:
                points = '>=100'

            # Find +/-
            goals_diff_val = float(instance[gf_index]) - float(instance[ga_index])
            if goals_diff_val < -40:
                goals_diff = '<-40'
            elif -40 <= goals_diff_val < -20:
                goals_diff = '>=-40'
            elif -20 <= goals_diff_val < 0:
                goals_diff = '>=-20'
            elif 0 <= goals_diff_val < 20:
                goals_diff = '>=0'
            elif 20 <= goals_diff_val < 40:
                goals_diff = '>=20'
            elif 40 <= goals_diff_val < 60:
                goals_diff = '>=40'
            elif 60 <= goals_diff_val:
                goals_diff = '>=60'

            # Power play percentage
            pp_percent_val = float(instance[pp_percent_index])
            if pp_percent_val < 20:
                pp_percent = '<20'
            else:
                pp_percent = '>=20'

            # corsi%
            corsi_percent_val = float(instance[corsi_percent_index])
            if corsi_percent_val < 46:
                corsi_percent = '<46'
            elif 46 <= corsi_percent_val < 49:
                corsi_percent = '>=46'
            elif 49 <= corsi_percent_val < 52:
                corsi_percent = '>=49'
            elif 52 <= corsi_percent_val < 55:
                corsi_percent = '>=52'
            elif 55 <= corsi_percent_val:
                corsi_percent = '>=55'

            # Top 20
            t20_val = float(instance[t20_index])
            if t20_val >= 3:
                t20 = '>=3'
            else:
                t20 = t20_val

            processed_data.append(
                [
                    instance[team_index],
                    points,
                    goals_diff,
                    pp_percent,
                    corsi_percent,
                    t20,
                    instance[ploffs_index]
                ])
        return processed_data

    def find_prob_class_given_evidence(self, instance):
        """Determine an instance's class from training data.

        Args:
            instance (list): A list containing data for one team.

        Returns:
            dict: A dictionary containing probabilities for all class values.
        """
        prob_dict = {}
        for class_val in classes:
            class_prob_list = []
            num_class_inst = self.find_num_inst_of_class(class_val)

            for attr_val in instance:
                index = instance.index(attr_val)
                attr = attributes[index]
                num_val_inst = self.find_num_attr_given_class(attr_val, index, class_val)

                # Correct for the zero-frequency problem
                numerator = float(num_val_inst) + 1.0
                denominator = float(num_class_inst) + float(num_attribute_values[attr])
                class_prob_list.append(numerator/denominator)


            # Multiply all elements in list together
            all_probs = reduce(lambda x, y: x*y, class_prob_list)
            class_prob = (float(num_class_inst) + 1)/(len(self._training_data) + num_attribute_values['ploffs'])
            temp_prob = all_probs * class_prob
            prob_dict.update({class_val: temp_prob})

        # Find probabilities for all classes
        prob_sum = sum(prob_dict.values())
        for key, value in prob_dict.iteritems():
            final_prob = value/prob_sum
            final_prob *= 100
            prob_dict[key] = final_prob
        return prob_dict

    def find_num_inst_of_class(self, class_value):
        """Determine the number of instances of a class in the training data.

        Args:
            class_value (str): A string representing the class value to find.

        Returns:
            float: The number of instances containing a particular class value.
        """
        num_inst_of_class = 0
        for inst in self._training_data[1:]:
            if inst[-1] == class_value:
                num_inst_of_class += 1
        return num_inst_of_class

    def find_num_attr_given_class(self, value, index, class_value):
        """Determine the number of instances a specified value in the training data.

        Args:
            value (str): A string representing the value to match.
            index (int): The index of the value.
            class_value (str): A string representing the class value.

        Returns:
            float: The number of instances that contain the value and the class_value.
        """
        num_value_in_class = 0
        for inst in self._training_data:
            class_present = inst[-1] == class_value
            value_present = inst[index] == value
            if class_present and value_present:
                num_value_in_class += 1
        return num_value_in_class
