#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi


gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from src.controladores.CsvManager import CsvManager

class Csv:
    csv = CsvManager()

    def __init__(self):
        pass

    def set_file(self, widget, *data):
        self.csv.load_file(data[0])

    def set_data_in_table(self, selection, *data):
        model, row = selection.get_selection().get_selected()

        if not row:
            return

        attributeIndex = -1
        for i, col in enumerate(selection.get_columns()):
            if col.get_title() == 'Attribute':
                attributeIndex = i

        if attributeIndex < 0:
            return

        attributeName = model[row][attributeIndex]
        counters = self.csv.get_index_counters(attributeName)
        columns = ['Dato', 'Repeticiones']
        data_list_store = Gtk.ListStore(*[str]*len(columns))

        for k, v in counters.iteritems():
            data_list_store.append([k, str(v)])

        data[0].set_model(data_list_store)

        for i, item in enumerate(columns):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(item, renderer, text=i)
            data[0].append_column(column)