from __future__ import division
import collections
import numpy
from JarvisMath import JarvisMath
from Usseful import list_search

class Classification:

    def __init__(self):
        pass

    @staticmethod
    def zero_r(data):
        if len(data) == 0:
            return {}

        frequency_table = collections.Counter(data).most_common()
        if len(frequency_table) != 0:
            rule = frequency_table[0][0]
        return rule

    @staticmethod
    def one_r(data, index_class):
        if len(data) == 0 or index_class not in range(0, len(data[0])):
            return {}

        frequency_table = JarvisMath.calculate_frequency_table(data, index_class)
        # encontrar mayor frecuencia, sumar el resto (error), ir guardando el menor
        for key, value in frequency_table.iteritems():
            for k2, v2 in value.iteritems():
                index_found = list_search(key, numeric_indexes)

        return frequency_table

    # Gets the naive bayes model from a data base, returns the class values counter used and the probability table
    @staticmethod
    def naive_bayes(data, index_class, numeric_indexes=[]):
        if len(data) == 0 or index_class not in range(0, len(data[0])):
            return []

        frequency_table = JarvisMath.calculate_frequency_table(data, index_class, numeric_indexes)

        class_counter = collections.Counter(elem[index_class] for elem in data)
        for key, value in frequency_table.iteritems():
            for k2, v2 in value.iteritems():
                index_found = list_search(key, numeric_indexes)

                if index_found != -1:
                    value[k2] = (numpy.mean(v2), numpy.std(v2))
                else:
                    value[k2] = v2 / class_counter[k2[1]]

        for key, value in class_counter.iteritems():
            class_counter[key] = value / len(data)

        '''for key, value in frequency_table.iteritems():
            print key
            for k2, v2 in value.iteritems():
                print k2, v2'''

        return [frequency_table, class_counter]

    @staticmethod
    def zero_r_prediction(instance, model, class_index):
        if len(model) == 0 or class_index not in range(0, len(instance)) or len(instance) == 0:
            return []

        instance.insert(class_index, model)
        return instance

    @staticmethod
    def one_r_prediction(instance, model, class_index):
        pass

    @staticmethod
    def naive_bayes_prediction(instance, model, class_index, numeric_indexes = []):
        if len(model) == 0 or class_index not in range(0, len(instance)) or len(instance) == 0:
            return []

        probabilities = []
        for key, value in model[1].iteritems():
            aux = 1
            for key2, value2 in model[0].iteritems():
                val = instance[key2 if key2 < class_index else key2 - 1]
                index_found = list_search(key2, numeric_indexes)
                if index_found == -1:
                    aux *= value2[(val, key)]
                else:
                    aux *= JarvisMath.gauss_density(val, value2[key][0], value2[key][1])

            aux *= value
            probabilities.append((aux, key))

        instance.insert(class_index, max(probabilities)[1])
        return instance

    @staticmethod
    def calculate_accuracy(objective, model, class_index):
        if len(objective) == 0 or len(objective) != len(model) or class_index not in range(0, len(objective[0])) \
                or len(objective[0]) != len(model[0]):
            return -1

        aux = sum([int(objective[ind] == model[ind]) for ind in range(0, len(objective))])

        return aux / len(objective)
