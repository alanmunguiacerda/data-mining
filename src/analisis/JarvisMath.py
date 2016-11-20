import numpy
import math
from collections import Counter
from itertools import groupby
from operator import itemgetter
from Usseful import list_search


class JarvisMath:

    def __init__(self):
        pass

    @staticmethod
    def mad(data):
        mean = numpy.mean(data)
        aux = sum([abs(x - mean) for x in data])

        return aux / len(data)

    @staticmethod
    def calculate_frequency_table(data, class_index, numeric_indexes = []):
        if len(data) is 0:
            return {}

        attr = {}
        for i, val in enumerate(data[0]):
            if i == class_index:
                continue
            found_index = list_search(i, numeric_indexes)

            if found_index is -1:
                # Not numeric
                attr[i] = Counter([(x[i], x[class_index]) for x in data])
            else:
                # Numeric
                attr[i] = JarvisMath.group_by([[x[i], x[class_index]] for x in data])
        return attr

    @staticmethod
    def group_by(lst):
        lst.sort(key=itemgetter(1))
        groups = groupby(lst, itemgetter(1))
        dic = {}
        for key, data in groups:
            dic[key] = [elem[0] for elem in data]
        return dic

    @staticmethod
    def gauss_density(x, mean, std_deviation):
        div = 1 / (math.sqrt(2 * math.pi) * std_deviation)
        euler = pow(math.e, (-(pow(x - mean, 2)) / (2*pow(std_deviation, 2))))
        return div * euler
