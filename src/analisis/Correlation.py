#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from collections import Counter
from JarvisMath import JarvisMath

class Correlation():
    jm = JarvisMath()

    def __init__(self):
        pass

    def nominal(self, data, attribute_1, attribute_2):
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

        free_levels = (len(counter_attribute_1) - 1) * (len(counter_attribute_2) - 1)
        return self.jm.chi_square(sum(x2), free_levels)