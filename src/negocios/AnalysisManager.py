#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
import copy
import exceptions

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from src.controladores.CsvManager import CsvManager
from src.analisis.NominalTransformation import NominalTransformation
from src.analisis.Correlation import Correlation
from src.Usseful import list_search
from src.vistas.dialogs.ErrorDialog import ErrorDialog

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

    def load_spin_input(self, spin_input):
        adjustment = Gtk.Adjustment(0, 0, len(self.csv.data)-1, 1, 0, 0)
        spin_input.configure(adjustment, 1, 0)

    def update_all(self, tree_view, combo_boxes, spin_inputs):
        self.set_file_in_table(tree_view)
        self.load_combo_box_attributes(combo_boxes['attribute_1'])
        self.load_combo_box_attributes(combo_boxes['attribute_2'])
        self.load_spin_input(spin_inputs['instance_1'])
        self.load_spin_input(spin_inputs['instance_2'])

    def calculate_transform(self, data_labels, value_1, value_2):
        data_labels['lev_1'].set_markup(str(value_1))
        data_labels['lev_2'].set_markup(str(value_2))

        if self.csv.check_type(value_1) is str and self.csv.check_type(value_2) is str:
            levenshtain = NominalTransformation.levenshtain_distance(value_1, value_2)
            data_labels['lev_result'].set_markup(str(levenshtain[-1][-1]))
        else:
            data_labels['lev_result'].set_markup('MUST BE STRINGS')

    def calculate_correlation(self, data_labels, attribute_1, attribute_2):
        data_labels['cor_1'].set_markup(str(attribute_1))
        data_labels['cor_2'].set_markup(str(attribute_2))

        numeric = True
        data_1 = self.csv.get_numeric_items(attribute_1)
        data_2 = self.csv.get_numeric_items(attribute_2)

        if not data_1 and not data_2:
            data_1 = self.csv.get_string_items(attribute_1)
            data_2 = self.csv.get_string_items(attribute_2)
            numeric = False

        if not data_1 or not data_2:
            data_labels['cor_result'].set_markup('MUST BE SAME TYPE')
            ErrorDialog('Error', 'Attributes must be of the same type', None)
            return False

        if numeric:
            correlation = Correlation.numeric(data_1, data_2)
        else:
            correlation= Correlation.nominal(data_1, data_2)

        if correlation != False:
            data_labels['cor_result'].set_markup(str(correlation))
        else:
            data_labels['cor_result'].set_markup('CORRELATION ERROR')

    def calculate(self, widget, spin_inputs, combo_boxes, data_labels):
        attribute_1 = combo_boxes['attribute_1'].get_active_text()
        attribute_2 = combo_boxes['attribute_2'].get_active_text()
        index_1 = list_search(attribute_1, self.csv.headers)
        index_2 = list_search(attribute_2, self.csv.headers)

        if index_1 < 0 or index_2 < 0:
            data_labels['lev_result'].set_markup('ATTRIBUTE ERROR')
            return False

        self.calculate_correlation(data_labels, attribute_1, attribute_2)

        try:
            instance_1 = int(spin_inputs['instance_1'].get_value())
            instance_2 = int(spin_inputs['instance_2'].get_value())
        except ValueError:
            ErrorDialog('Error', 'Instance number must be an integer', None)
            return False

        value_1 = self.csv.data[instance_1][index_1]
        value_2 = self.csv.data[instance_2][index_2]

        self.calculate_transform(data_labels, value_1, value_2)

