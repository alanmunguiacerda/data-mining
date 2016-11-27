#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import numpy
from JarvisMath import JarvisMath


class NumericTransformations:

    def __init__(self):
        pass

    @staticmethod
    def min_max(data, data_min, data_max, new_min, new_max):
        max_min = data_max - data_min
        new_max_min = new_max - new_min
        normalized_data = [((x - data_min) / max_min * new_max_min + new_min) for x in data]

        return normalized_data

    @staticmethod
    def z_score(data, deviation):
        mean = numpy.mean(data)
        normalized_data = [(x - mean) / deviation for x in data]

        return normalized_data

    @staticmethod
    def z_score_standard(data):
        return NumericTransformations.z_score(data, numpy.std(data))

    @staticmethod
    def z_score_absolute(data):
        return NumericTransformations.z_score(data, JarvisMath.mad(data))

    @staticmethod
    def decimal_scaling(data):
        abs_max = abs(max(min(data), max(data), key=abs))
        factor = pow(10, len(str(abs_max)))

        normalized_data = []

        for ind in range(0, len(data)):
            normalized_data.append(data[ind] / factor)

        return normalized_data
