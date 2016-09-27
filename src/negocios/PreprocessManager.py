#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
import copy
import ntpath

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from gi.repository import GObject

from controladores.CsvManager import CsvManager


class PreprocessManager:
    csv = CsvManager()

    def __init__(self):
        pass

    def set_file(self, widget, *data):
        self.csv.load_file(data[0])

    def set_data_in_table(self, selection, *data):
        model, row = selection.get_selection().get_selected()

        if not row:
            return False

        attribute_name = model[row][1]
        counters = self.csv.get_index_counters(attribute_name)

        if not counters:
            return False

        columns = ['Number', 'Label', 'Count', 'Weight']
        data_list_store = Gtk.ListStore(*[str]*len(columns))

        i = 0
        for k, v in counters.iteritems():
            data_list_store.append([str(i), k, str(v), "{0:.1f}".format(v)])
            i += 1

        data[0].set_model(data_list_store)

        for col in data[0].get_columns():
            data[0].remove_column(col)

        for i, item in enumerate(columns):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(item, renderer, text=i)
            data[0].append_column(column)

    def save_file(self, path):
        self.csv.save_version(path)

    def load_combo_box_attributes(self, *args):
        headers_list = self.csv.headers

        args[2].remove_all()

        for var in headers_list:
            args[2].append_text(var)

        args[2].set_active(0)

    def load_attributes_tree_view(self, *args):
        headers_list = self.csv.headers

        list_store = Gtk.ListStore(GObject.TYPE_INT, GObject.TYPE_STRING)

        for i, var in enumerate(headers_list):
            list_store.append([i, var])

        args[2].set_model(list_store)

        for i, col_title in enumerate(["Number", "Attribute"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(col_title, renderer, text=i)

            # Add columns to TreeView
            args[2].append_column(column)

    def clean_attributes_widgets(self, *args):
        # Tree view cleaning
        columns = args[2].get_columns()
        for column in columns:
            args[2].remove_column(column)

        # Combo box cleaning
        args[3].remove_all()

        # Tree view cleaning
        columns = args[4].get_columns()
        for column in columns:
            args[4].remove_column(column)

        for i in range(5, 10):
            args[i].set_label("")

    def set_file_info(self, widget, *args):
        labels = [x for x in args if type(x).__name__ == 'Label']

        _, filename = ntpath.split(self.csv.filename)
        filename = filename.split('.')[0]

        labels[0].set_text(filename)
        labels[1].set_text(str(len(self.csv.headers)))
        instances = len(self.csv.data)
        labels[2].set_text(str(instances))
        labels[3].set_text("{0:.1f}".format(instances))

    def remove_attribute(self, widget, *args):
        self.csv.delete_attribute(args[0])

    def set_attribute_info(self, *args):
        model, row = args[0].get_selection().get_selected()

        if not row:
            return

        attribute_name = model[row][1]
        counters = self.csv.get_index_counters(attribute_name)
        # Attribute name label
        args[1].set_label(attribute_name)

        # Missing
        missing = self.csv.missing_values(attribute_name)
        args[2].set_label(str(missing) + "( " + str((missing * 100) / len(self.csv.data)) + "% )")

        # Distinct label
        args[3].set_label(str(len(counters)))

        unique_count = 0
        numeric = True
        for k, v in counters.iteritems():
            if v is 1:
                unique_count += 1
            if not k.replace('.', '', 1).isdigit():
                numeric = False

        # Type label
        if len(counters) is 2:
            args[4].set_label("Binary")
        else:
            args[4].set_label("Numeric" if numeric else "Nominal")
        # Unique label
        args[5].set_label(str(unique_count) + "( " + str((unique_count * 100) / len(self.csv.data)) + "% )")

    def set_file_in_table(self, tree_view):
        headers = copy.deepcopy(self.csv.headers)

        headers.insert(0, "Action")
        list_store = Gtk.ListStore(*[str] * len(headers))

        for row in self.csv.data:
            row_aux = copy.deepcopy(row)
            row_aux.insert(0, "")
            list_store.append(row_aux)

        tree_view.set_model(list_store)

        for col in tree_view.get_columns():
            tree_view.remove_column(col)

        for i, item in enumerate(headers):
            renderer = Gtk.CellRendererText()
            if i is not 0:
                renderer.set_property("editable", True)
                renderer.connect("edited", tree_view.get_parent().get_parent().get_parent().keep_changes, i)
            column = Gtk.TreeViewColumn(item, renderer, text=i)
            tree_view.append_column(column)
