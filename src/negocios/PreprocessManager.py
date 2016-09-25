#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi


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
            return

        attribute_index = -1
        for i, col in enumerate(selection.get_columns()):
            if col.get_title() == 'Attribute':
                attribute_index = i

        if attribute_index < 0:
            return

        # attribute_name = model[row][1]
        attribute_name = model[row][attribute_index]
        counters = self.csv.get_index_counters(attribute_name)
        columns = ['No', 'Label', 'Count', 'Weight']
        data_list_store = Gtk.ListStore(*[str]*len(columns))

        i = 0
        for k, v in counters.iteritems():
            data_list_store.append([str(i), k, str(v), str(v)])
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

        for var in headers_list:
            args[2].append_text(var)

        args[2].set_active(0)

    def load_attributes_tree_view(self, *args):
        headers_list = self.csv.headers

        list_store = Gtk.ListStore(GObject.TYPE_INT, GObject.TYPE_STRING)

        i = 0
        for var in headers_list:
            list_store.append([i, var])
            i += 1

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

