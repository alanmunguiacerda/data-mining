#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi


gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

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

        attribute_name = model[row][attribute_index]
        counters = self.csv.get_index_counters(attribute_name)
        columns = ['No', 'Label', 'Count', 'Weight']
        data_list_store = Gtk.ListStore(*[str]*len(columns))

        i = 0
        for k, v in counters.iteritems():
            data_list_store.append([str(i), k, str(v), str(v)])
            i+=1

        data[0].set_model(data_list_store)

        if len(data[0].get_columns()) != len(columns):
            for i, item in enumerate(columns):
                renderer = Gtk.CellRendererText()
                column = Gtk.TreeViewColumn(item, renderer, text=i)
                data[0].append_column(column)