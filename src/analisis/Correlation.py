#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import numpy
from collections import Counter
from JarvisMath import JarvisMath
from Usseful import index_in_range


class Correlation():
    def __init__(self):
        pass

    @staticmethod
    def nominal(data, attribute_1, attribute_2):
        if not index_in_range(attribute_1, data) or not index_in_range(attribute_2, data):
            return None

        frequency_table = Counter([(x[attribute_1], x[attribute_2]) for x in data])
        counter_attribute_1 = Counter(x[attribute_1] for x in data)
        counter_attribute_2 = Counter(x[attribute_2] for x in data)
        x2 = []
        for key, val in counter_attribute_1.iteritems():
            for key2, val2 in counter_attribute_2.iteritems():
                e = val * val2 / len(data)
                x = frequency_table[(key, key2)]
                calc = pow(x - e, 2) / e
                x2.append(calc)
        jm = JarvisMath()
        free_levels = (len(counter_attribute_1) - 1) * (len(counter_attribute_2) - 1)
        return jm.chi_square(sum(x2), free_levels)

    @staticmethod
    def numeric(data, attribute_1, attribute_2):
        if not index_in_range(attribute_1, data) or not index_in_range(attribute_2, data):
            return None

        list_attribute_1 = [x[attribute_1] for x in data]
        list_attribute_2 = [x[attribute_2] for x in data]
        mean_1 = numpy.mean(list_attribute_1)
        mean_2 = numpy.mean(list_attribute_2)
        desvest_1 = numpy.std(list_attribute_1)
        desvest_2 = numpy.std(list_attribute_2)
        n = len(data)
        partial = sum([(x[attribute_1] - mean_1)*(x[attribute_2]- mean_2) for x in data])
        return partial / (n * desvest_1 * desvest_2)