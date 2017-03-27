attributes = ('Points', '+/-', 'PP%', 'CORSI%', 'Top 20')
classes = ('Playoff Finish', ['0', '1', '2', '3', '4', 'SC'])

#TODO: Have not accounted for thresholds yet
class HockeyBayes:
    def __init__(self, data, instance):
        self._data = data
        self._instance = instance
        self._prob_list = []

    def find_prob_class_given_evidence(self, desired_class):
        for class_val in classes[1]:
            class_prob_list = []
            num_class_inst = self.find_num_inst_of_class(class_val)
            for attr_val in self._instance:
                index = self._instance.index(attr_val)
                val_inst = self.find_prob_attr_given_class(attr_val, index, class_val)
                class_prob_list.append(val_inst/num_class_inst)
            # Multiply all elements in list together
            all_probs = reduce(lambda x, y: x*y, class_prob_list)
            self._prob_list.append(all_probs * float(num_class_inst)/float(len(self._data[1:])))

        # Find the probability for the desired class
        class_index = classes[1].index(desired_class)
        probability = self._prob_list[class_index]/reduce(lambda x, y: x+y, self._prob_list)
        probability *= 100
        return probability

    def find_num_inst_of_class(self, class_value):
        num_inst_of_class = 0
        for inst in self._data[1:]:
            class_index = self._data[0].index(classes[0])
            if inst[class_index] == class_value:
                num_inst_of_class += 1
        return num_inst_of_class

    def find_prob_attr_given_class(self, value, index, class_value):
        num_value_in_class = 0
        for inst in self._data[1:]:
            class_index = self._data[0].index(classes[0])
            class_present = inst[class_index] == class_value
            value_present = inst[index] == value
            if class_present and value_present:
                num_value_in_class += 1
        return num_value_in_class
