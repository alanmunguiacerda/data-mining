#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject

from src.vistas.BaseTab import BaseTab
from src.negocios.AnalysisManager import AnalysisManager

class AnalysisTab(BaseTab):
    def __init__(self, parent):
        BaseTab.__init__(self, parent)

        self.analysisManager = AnalysisManager(self)

        self.create_data_table()
        self.create_selectors()
        self.create_levenshtain_results()
        self.create_correlation_results()

        self.attach_all_to_layout()
        self.pack_start(self.page_layout, True, True, 0)

        self.set_signals()
        self.set_connections()

    def set_signals(self):
        GObject.signal_new('page-selected', self, GObject.SIGNAL_RUN_LAST, GObject.TYPE_PYOBJECT,
                           ())

    def set_connections(self):
        self.connect('page-selected', self.selected)
        self.buttons['calculate'].connect('clicked', self.analysisManager.calculate, self.text_inputs, self.combo_boxes, self.labels)

    def attach_all_to_layout(self):
        self.page_layout.attach(self.frames['data_table'], 0, 0, 3, 1)
        self.page_layout.attach(self.frames['selectors'], 0, 1, 2, 2)
        self.page_layout.attach(self.frames['lev_results'], 2, 1, 1, 1)
        self.page_layout.attach(self.frames['cor_results'], 2, 2, 1, 1)

    def create_data_table(self):
        frame = self.create_frame('data_table', 'Data')
        box = self.create_box(frame, 'data_table')
        self.insert_scrollable_tree_view(box, 'data_table')

    def create_selectors(self):
        frame = self.create_frame('selectors', 'Options')
        box = self.create_box(frame, 'selectors')
        grid = self.create_grid(box, 'selectors')

        instance_static_labels = ['Instance #1', 'Instance #2']
        input_fields = ['instance_1', 'instance_2']

        self.insert_static_label_input_text('selectors', instance_static_labels, input_fields)

        attribute_statistics_labels = ['Attribute #1', 'Attribute #2', 'Calculate']
        combo_boxes = ['attribute_1', 'attribute_2', 'calc_type']

        self.insert_static_label_combo_box('selectors', attribute_statistics_labels, combo_boxes,
                                           start_row=2)

        self.insert_button(grid, 'calculate', 'Calculate', 3, 3, 3, 1)

    def create_levenshtain_results(self):
        frame = self.create_frame('lev_results', 'Levenshtain')
        box = self.create_box(frame, 'lev_results')
        self.create_grid(box, 'lev_results')

        static_labels = ['Value 1', 'Value 2', 'Result']
        data_labels = ['lev_1', 'lev_2', 'lev_result']

        self.insert_static_label_data_label('lev_results', static_labels, data_labels, columns=1)

    def create_correlation_results(self):
        frame = self.create_frame('cor_results', 'Correlation')
        box = self.create_box(frame, 'cor_results')
        self.create_grid(box, 'cor_results')

        static_labels = ['Attribute 1', 'Attribute 2', 'Result']
        data_labels = ['cor_1', 'cor_2', 'cor_result']

        self.insert_static_label_data_label('cor_results', static_labels, data_labels, columns=1)

    def selected(self, *args):
        self.analysisManager.update_all(self.tree_views['data_table'], self.combo_boxes)