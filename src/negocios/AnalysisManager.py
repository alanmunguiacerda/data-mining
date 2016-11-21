#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
import copy
import exceptions

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from controladores.CsvManager import CsvManager
from analisis.NominalTransformation import NominalTransformation
from analisis.Usseful import list_search

class AnalysisManager():
    def __init__(self, parent):
        self.parent = parent
        self.csv = CsvManager()

    def set_file_in_table(self, tree_view):
        headers = ["#"]
        headers.extend(copy.deepcopy(self.csv.headers))

        list_store = Gtk.ListStore(*[str] * len(headers))

        data = copy.deepcopy(self.csv.data)

        for i, item in enumerate(data):
            for j, elem in enumerate(self.csv.headers):
                if elem in self.csv.wrong_registers:
                    wrong_registers = self.csv.wrong_registers[elem]
                    try:
                        index = wrong_registers.index(i)
                    except exceptions.Exception:
                        index = -1

                    if index != -1:
                        item[j] = '<span background="red" foreground="white">' + item[j] + '</span>'
            item.insert(0, str(i))

            list_store.append(item)

        tree_view.set_model(list_store)

        for col in tree_view.get_columns():
            tree_view.remove_column(col)

        for i, item in enumerate(headers):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(item, renderer, markup=i)

            tree_view.append_column(column)

    def load_combo_box_attributes(self, combo_box):
        combo_box.remove_all()
        for var in self.csv.headers:
            combo_box.append_text(var)

        combo_box.set_active(0)

    def update_all(self, tree_view, combo_boxes):
        self.set_file_in_table(tree_view)
        self.load_combo_box_attributes(combo_boxes['attribute_1'])
        self.load_combo_box_attributes(combo_boxes['attribute_2'])

    def calculate_transform(self, text_inputs, combo_boxes, data_labels):
        instance_1 = text_inputs['instance_1'].get_text()
        instance_2 = text_inputs['instance_2'].get_text()
        try:
            instance_1 = int(instance_1)
            instance_2 = int(instance_2)
        except ValueError:
            return None
        # TODO: send error message

        attribute_1 = combo_boxes['attribute_1'].get_active_text()
        attribute_2 = combo_boxes['attribute_2'].get_active_text()
        index_1 = list_search(attribute_1, self.csv.headers)
        index_2 = list_search(attribute_2, self.csv.headers)

        if index_1 < 0 or index_2 < 0:
            return None

        value_1 = self.csv.data[instance_1][index_1]
        value_2 = self.csv.data[instance_2][index_2]

        data_labels['lev_1'].set_text(str(value_1))
        data_labels['lev_2'].set_text(str(value_2))

        if self.csv.check_type(value_1) is str and self.csv.check_type(value_2) is str:
            levenshtain = NominalTransformation.levenshtain_distance(value_1, value_2)
            data_labels['lev_result'].set_text(str(levenshtain[-1][-1]))
        else:
            data_labels['lev_result'].set_text('ERROR')


    def calculate(self, widget, text_inputs, combo_boxes, data_labels):
        attribute_1 = combo_boxes['attribute_1'].get_active_text()
        attribute_2 = combo_boxes['attribute_2'].get_active_text()
        index_1 = list_search(attribute_1, self.csv.headers)
        index_2 = list_search(attribute_2, self.csv.headers)

        self.calculate_transform(text_inputs, combo_boxes, data_labels)
