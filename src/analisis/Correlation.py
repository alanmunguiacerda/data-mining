#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import numpy
from collections import Counter
from JarvisMath import JarvisMath

class Correlation():
    def __init__(self):
        pass

    @staticmethod
    def nominal(data_1, data_2):
        if len(data_1) != len(data_2):
            return False

        frequency_table = Counter([(x, y) for x, y in zip(data_1, data_2)])
        counter_attribute_1 = Counter(x for x in data_1)
        counter_attribute_2 = Counter(x for x in data_2)
        x2 = []
        for key, val in counter_attribute_1.iteritems():
            for key2, val2 in counter_attribute_2.iteritems():
                e = val * val2 / len(data_1)
                x = frequency_table[(key, key2)]
                calc = pow(x - e, 2) / e
                x2.append(calc)
        jm = JarvisMath()
        free_levels = (len(counter_attribute_1) - 1) * (len(counter_attribute_2) - 1)
        print free_levels
        return jm.chi_square(sum(x2), free_levels)

    @staticmethod
    def numeric(data_1, data_2):
        if len(data_1) != len(data_2):
            return False

        mean_1 = numpy.mean(data_1)
        mean_2 = numpy.mean(data_2)
        desvest_1 = numpy.std(data_1)
        desvest_2 = numpy.std(data_2)
        partial = sum([(x - mean_1)*(y- mean_2) for x, y in zip(data_1, data_2)])
        return partial / (len(data_1) * desvest_1 * desvest_2)