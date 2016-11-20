#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
import os

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject

from src.vistas.BaseTab import BaseTab
from src.controladores.CsvManager import CsvManager
from src.vistas.ErrorDialog import ErrorDialog
from src.vistas.DomainPopup import DomainPopup
from src.vistas.ModifyFileDialog import ModifyFileDialog

class AnalysisTab(BaseTab):
    def __init__(self, parent):
        super(AnalysisTab, self).__init__(parent)

        self.csvManager = CsvManager()
        self.create_data_table()
        self.create_selectors()
        self.create_levenshtain_results()
        self.create_correlation_results()

        self.attach_all_to_layout()
        self.pack_start(self.page_layout, True, True, 0)

        self.set_signals()
        self.set_connections()

    def set_signals(self):
        pass

    def set_connections(self):
        pass

    def attach_all_to_layout(self):
        self.page_layout.attach(self.frames['data_table'], 0, 0, 4, 1)
        self.page_layout.attach(self.frames['selectors'], 0, 1, 2, 1)
        self.page_layout.attach(self.frames['lev_results'], 2, 1, 1, 1)
        self.page_layout.attach(self.frames['cor_results'], 3, 1, 1, 1)

    def create_data_table(self):
        frame = self.create_frame('data_table', 'Data')
        box = self.create_box(frame, 'data_table')
        self.insert_scrollable_tree_view(box, 'data_table')

    def create_selectors(self):
        frame = self.create_frame('selectors', 'Options')
        box = self.create_box(frame, 'selectors')
        self.create_grid(box, 'selectors')

        attribute_statistics_labels = ['Instance #1', 'Instance #2', 'Attribute #1', 'Attribute #2']
        combo_boxes = ['instance_1', 'instance_2', 'attribute_1', 'attribute_2']

        self.insert_static_label_combo_box('selectors', attribute_statistics_labels, combo_boxes)

    def create_levenshtain_results(self):
        frame = self.create_frame('lev_results', 'Levenshtain')
        box = self.create_box(frame, 'lev_results')
        self.create_grid(box, 'lev_results')

        static_labels = ['Value 1', 'Value 2', 'Result']
        data_labels = ['lev_1', 'lev_2', 'result']

        self.insert_static_label_data_label('lev_results', static_labels, data_labels, columns=1)

    def create_correlation_results(self):
        frame = self.create_frame('cor_results', 'Correlation')
        box = self.create_box(frame, 'cor_results')
        self.create_grid(box, 'cor_results')

        static_labels = ['Attribute 1', 'Attribute 2', 'Result']
        data_labels = ['cor_1', 'cor_2', 'result']

        self.insert_static_label_data_label('cor_results', static_labels, data_labels, columns=1)