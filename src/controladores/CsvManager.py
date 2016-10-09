#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import csv
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

    def __init__(self):
        pass

    def reset_shared(self):
        del self.headers[:]
        del self.data[:]
        del self.dataVersions[:]
        self.domains.clear()
        self.wrong_registers.clear()
        self.filename = None

    def load_file(self, filename):
        if not filename:
            return

        try:
            loaded_file = open(filename, 'rU')
        except exceptions.IOError:
            return False

        self.reset_shared()
        self.filename = filename
        reader = csv.reader(loaded_file)
        for item in reader.next():
            self.headers.append(item)
        for line in reader:
            for i, element in enumerate(line):
                if not element or element.isspace():
                    line[i] = constants.MISSING_DATA_SYMBOL
            self.data.append(line)

        return True

    def new_version(self, data=False, headers=False, domains=False):
        print "Versioning {!s}, {!s}, {!s}".format(data, headers, domains)
        new_version = {}
        if data:
            new_version['data'] = copy.deepcopy(self.data)
        if headers:
            new_version['headers'] = copy.deepcopy(self.headers)
        if domains:
            new_version['domains'] = copy.deepcopy(self.domains)
        if len(new_version) > 0:
            self.dataVersions.append(new_version)

    def rollback(self):
        past_version = self.dataVersions.pop()
        if 'data' in past_version:
            del self.data[:]
            self.data = past_version['data']
        if 'headers' in past_version:
            del self.headers[:]
            self.headers = past_version['headers']
        if 'domains' in past_version:
            self.domains.clear()
            self.domains = past_version['domains']
        return True

    def delete_attribute(self, attribute_name):
        try:
            index_found = self.headers.index(attribute_name)
        except exceptions.Exception:
            return False

        self.new_version(data = True, headers=True, domains=True)

        if attribute_name in self.domains:
            del self.domains[attribute_name]

        del self.headers[index_found]

        for row in self.data:
            del row[index_found]

        return True

    def delete_tuples(self, rows_index):
        if not rows_index or len(rows_index) < 1:
            return False

        self.new_version(data = True)

        rows_index = sorted(rows_index, reverse=True)
        for index in rows_index:
            try:
                del self.data[index]
            except IndexError:
                pass

        return True

    def fill_tuples(self, new_tuples):
        if not new_tuples or len(new_tuples) < 1:
            return False

        self.new_version(data = True)

        for key, value in new_tuples.iteritems():
            self.data[key] = value

        return True

    def get_index_counters(self):
        count = {}
        for i, header in enumerate(self.headers):
            count[header] = collections.Counter(elem[i] for elem in self.data)

        return count

    def get_index_counters(self, attribute_name):
        try:
            index = self.headers.index(attribute_name)
        except exceptions.Exception:
            return False

        return collections.Counter(elem[index] for elem in self.data)

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

        writer.writerow(self.headers)
        for item in self.data:
            writer.writerow(item)

    def missing_values(self, attribute_name):
        try:
            index = self.headers.index(attribute_name)
        except exceptions.Exception:
            return False

        return sum(1 for i in self.data if i[index] == constants.MISSING_DATA_SYMBOL)

    def add_tuples(self, tuples):
        if not tuples or len(tuples) < 1:
            return False

        self.new_version(data=True)

        for tuple in tuples:
            self.data.append(tuple)

        return True

    def print_headers(self):
        for item in self.headers:
            print item

    def print_data(self):
        for row in self.data:
            print row

    def set_domain(self, regexp, attribute):
        try:
            re.compile(regexp)
        except re.error:
            return False

        self.new_version(domains=True)
        self.domains[attribute] = regexp
        self.check_domain(attribute)

        return True

    def get_domain(self, attribute):
        if attribute in self.domains:
            return self.domains[attribute]
        else:
            return ""

    def check_domain(self, attribute_name):
        if attribute_name in self.wrong_registers:
            del self.wrong_registers[attribute_name]

        try:
            index = self.headers.index(attribute_name)
        except exceptions.Exception:
            return False

        if attribute_name in self.domains:
            domain = self.domains[attribute_name]
            i = 0
            for elem in self.data:
                if re.match(domain, elem[index]) is None:
                    if attribute_name in self.wrong_registers:
                        registers_list = self.wrong_registers[attribute_name]
                    else:
                        registers_list = []
                        self.wrong_registers[attribute_name] = registers_list

                    registers_list.append(i)
                i += 1

    def check_all_domains(self):
        for elem in self.domains:
            self.check_domain(elem)
