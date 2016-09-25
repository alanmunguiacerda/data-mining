#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi


gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from src.controladores.CsvManager import CsvManager

class Csv:
    csv = CsvManager()

    def __init__(self):
        self.csv.load_file('../csv/FL_insurance_sample.csv')

    def set_data_in_table(self, widget, *data):
        print data

        return
        text = widget.get_active_text()
        counters = self.csv.get_index_counters()
        columns = ['Atributo', 'Dato', 'Repeticiones']
        print counters
        data_list_store = Gtk.ListStore(*[str]*len(columns))

        for key, value in counters.iteritems():
            data_list_store.append([key, '', ''])
            for k, v in value.iteritems():
                data_list_store.append(['', k, str(v)])

        data[0].set_model(data_list_store)

        for i, item in enumerate(columns):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(item, renderer, text=i)
            data[0].append_column(column)