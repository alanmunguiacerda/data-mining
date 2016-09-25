#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
import copy
import csv
import exceptions
import collections


class CsvManager:
    data = []
    headers = []
    dataVersions = []

    def __init__(self):
        pass

    def reset_shared(self):
        del self.headers[:]
        del self.data[:]
        del self.dataVersions[:]

    def load_file(self, filename=None):
        if filename:
            try:
                loaded_file = open(filename, 'rU')
            except exceptions.IOError:
                return False

            self.reset_shared()
            reader = csv.reader(loaded_file)
            for item in reader.next():
                self.headers.append(item)
            for line in reader:
                self.data.append(line)

            return True

    def new_version(self):
        new_version = {
            'data': copy.deepcopy(self.data),
            'headers': copy.deepcopy(self.headers)
        }
        self.dataVersions.append(new_version)

    def rollback(self):
        del self.data[:]
        del self.headers[:]
        past_version = self.dataVersions.pop()
        self.data = past_version['data']
        self.headers = past_version['headers']
        return True

    def delete_attribute(self, attribute_name=None):
        if not attribute_name:
            return False

        try:
            index_found = self.headers.index(attribute_name)
        except exceptions.Exception:
            return False

        self.new_version()

        del self.headers[index_found]

        for row in self.data:
            del row[index_found]

        return True

    def delete_tuples(self, rows_index=None):
        if not rows_index:
            return False

        self.new_version()

        for index in rows_index:
            del self.data[index]

        return True

    def fill_tuples(self, new_tuples=None):
        if not new_tuples:
            return False

        self.new_version()

        for key, value in new_tuples.iteritems():
            self.data[key] = value

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

    def print_headers(self):
        for item in self.headers:
            print item

    def print_data(self):
        for row in self.data:
            print row