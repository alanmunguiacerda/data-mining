#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import csv
import numpy
import pickle
import ntpath

import exceptions
import collections

import re

import constants


class CsvManager:
    data = []
    headers = []
    dataVersions = []
    filename = None
    domains = {}
    wrong_registers = {}
    class_index = 0

    def __init__(self):
        pass

    def reset_shared(self):
        del CsvManager.headers[:]
        del CsvManager.data[:]
        del CsvManager.dataVersions[:]
        CsvManager.domains.clear()
        CsvManager.wrong_registers.clear()
        CsvManager.filename = None
        CsvManager.class_index = 0

    def load_file(self, filename):
        if not filename:
            return False

        try:
            loaded_file = open(filename, 'rU')
        except exceptions.IOError:
            return False

        self.reset_shared()
        CsvManager.filename = filename
        reader = csv.reader(loaded_file)
        for item in reader.next():
            CsvManager.headers.append(item)

        for line in reader:
            for i, element in enumerate(line):
                if not element or element.isspace():
                    line[i] = constants.MISSING_DATA_SYMBOL
            CsvManager.data.append(line)

        path_name = str.split(filename, '.')[0]
        try:
            CsvManager.domains = self.load_obj(path_name)
            self.check_all_domains()
        except exceptions.Exception:
            CsvManager.domains = {}

        return True

    def new_version(self, data=False, headers=False, domains=False):
        new_version = {}
        if data:
            new_version['data'] = copy.deepcopy(CsvManager.data)
        if headers:
            new_version['headers'] = copy.deepcopy(CsvManager.headers)
        if domains:
            new_version['domains'] = copy.deepcopy(CsvManager.domains)
        if CsvManager.wrong_registers:
            new_version['wrong_registers'] = copy.deepcopy(CsvManager.wrong_registers)
        if len(new_version) > 0:
            CsvManager.dataVersions.append(new_version)

    def rollback(self):
        past_version = CsvManager.dataVersions.pop()
        if 'data' in past_version:
            del CsvManager.data[:]
            CsvManager.data = past_version['data']
        if 'headers' in past_version:
            del CsvManager.headers[:]
            CsvManager.headers = past_version['headers']
        if 'domains' in past_version:
            CsvManager.domains.clear()
            CsvManager.domains = past_version['domains']
        if 'wrong_registers' in past_version:
            CsvManager.wrong_registers = past_version['wrong_registers']
        return True

    def delete_attribute(self, attribute_name):
        try:
            index_found = CsvManager.headers.index(attribute_name)
        except exceptions.Exception:
            return False

        self.new_version(data=True, headers=True, domains=True)

        if attribute_name in CsvManager.domains:
            del CsvManager.domains[attribute_name]

        del CsvManager.headers[index_found]

        for row in CsvManager.data:
            del row[index_found]

        if index_found == CsvManager.class_index:
            CsvManager.class_index = 0

        return True

    def delete_tuples(self, rows_index):
        if not rows_index or len(rows_index) < 1:
            return False

        self.new_version(data = True)

        rows_index = sorted(rows_index, reverse=True)
        for index in rows_index:
            try:
                del CsvManager.data[index]
            except IndexError:
                pass

        return True

    def fill_tuples(self, new_tuples):
        if not new_tuples or len(new_tuples) < 1:
            return False

        self.new_version(data = True)

        for key, value in new_tuples.iteritems():
            CsvManager.data[key] = value

        return True

    def get_index_counters(self):
        count = {}
        for i, header in enumerate(CsvManager.headers):
            count[header] = collections.Counter(elem[i] for elem in CsvManager.data)

        return count

    def get_index_counters(self, attribute_name):
        try:
            index = CsvManager.headers.index(attribute_name)
        except exceptions.Exception:
            return False

        return collections.Counter(elem[index] for elem in CsvManager.data)

    def get_unique_attributes(self):
        count = self.get_index_counters()
        uniques = []
        for key, value in count.iteritems():
            if len(value) < 2:
                uniques.append(key)

        return uniques

    def save_version(self, file_path):
        new_file = open(file_path, 'wb')
        writer = csv.writer(new_file)

        writer.writerow(CsvManager.headers)
        for item in CsvManager.data:
            clean_item = [x.replace(constants.MISSING_DATA_SYMBOL, "") for x in item]
            writer.writerow(clean_item)

        path_name = str.split(file_path, '.')[0]

        self.save_obj(CsvManager.domains, path_name)

    def missing_values(self, attribute_name):
        try:
            index = CsvManager.headers.index(attribute_name)
        except exceptions.Exception:
            return False

        return sum(1 for i in CsvManager.data if i[index] == constants.MISSING_DATA_SYMBOL)

    def add_tuples(self, tuples):
        if not tuples or len(tuples) < 1:
            return False

        self.new_version(data=True)

        for tuple in tuples:
            CsvManager.data.append(tuple)

        return True

    def set_domain(self, regexp, attribute):
        try:
            re.compile(regexp)
        except re.error:
            return False

        self.new_version(domains=True)
        CsvManager.domains[attribute] = regexp
        self.check_domain(attribute)

        return True

    def get_domain(self, attribute):
        if attribute in CsvManager.domains:
            return CsvManager.domains[attribute]
        else:
            return ""

    def check_domain(self, attribute_name):
        if attribute_name in CsvManager.wrong_registers:
            del CsvManager.wrong_registers[attribute_name]

        try:
            index = CsvManager.headers.index(attribute_name)
        except exceptions.Exception:
            return False

        if attribute_name in CsvManager.domains:
            domain = CsvManager.domains[attribute_name]
            for i, elem in enumerate(CsvManager.data):
                if re.match(domain, elem[index]) is None:
                    if not attribute_name in CsvManager.wrong_registers:
                        CsvManager.wrong_registers[attribute_name] = []

                    CsvManager.wrong_registers[attribute_name].append(i)

    def check_all_domains(self):
        for elem in CsvManager.domains:
            self.check_domain(elem)

    def check_type(self, object):
        try:
            float(object)
            return float
        except ValueError:
            return str

    def get_numeric_items(self, attribute_name):
        try:
            index_found = CsvManager.headers.index(attribute_name)
        except exceptions.Exception:
            return False

        try:
            nums = [float(x[index_found]) for x in CsvManager.data]
        except ValueError:
            return False

        return nums

    def get_numeric_attributes(self):
        return [x for x in self.headers if self.get_numeric_items(x)]


    def get_string_items(self, attribute_name):
        try:
            index_found = CsvManager.headers.index(attribute_name)
        except exceptions.Exception:
            return False

        try:
            strings = [x[index_found] for x in CsvManager.data if x[index_found] != constants.MISSING_DATA_SYMBOL]
        except ValueError:
            return False

        return strings

    def get_mean(self, attribute_name):
        nums = self.get_numeric_items(attribute_name)
        if not nums:
            return False
        return numpy.mean(nums)

    def get_median(self, attribute_name):
        nums = self.get_numeric_items(attribute_name)
        if not nums:
            return False
        return numpy.median(nums)

    def get_mode(self, attribute_name):
        data = self.get_numeric_items(attribute_name)
        if not data:
            data = self.get_string_items(attribute_name)
        if not data:
            return []

        hist = collections.Counter(data)
        maxRepeat = hist.most_common(1)[0][1]

        return [x[0] for x in hist.most_common() if x[1] == maxRepeat and x[1] > 1]

    def get_max(self, attribute_name):
        nums = self.get_numeric_items(attribute_name)
        if not nums:
            return False

        return max(nums)

    def get_min(self, attribute_name):
        nums = self.get_numeric_items(attribute_name)
        if not nums:
            return False

        return min(nums)

    def get_standard_deviation(self, attribute_name):
        nums = self.get_numeric_items(attribute_name)
        if not nums:
            return False

        return numpy.std(nums)

    def save_obj(self, obj, path_filename):
        with open(path_filename + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    def load_obj(self, path_filename):
        with open(path_filename + '.pkl', 'rb') as f:
            return pickle.load(f)

    def replace_column(self, attribute, new_data):
        try:
            index_found = CsvManager.headers.index(attribute)
        except exceptions.Exception:
            return False

        if len(new_data) != len(CsvManager.data):
            return False

        self.new_version(data=True)
        for i, value in enumerate(new_data):
            CsvManager.data[i][index_found] = str(value)
        return True

    def class_index_changed(self, widget):
        CsvManager.class_index = widget.get_active()
