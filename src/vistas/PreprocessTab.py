#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from src.vistas.BaseTab import BaseTab
from src.negocios.PreprocessManager import PreprocessManager

class PreprocessTab(BaseTab):
    def __init__(self, parent):
        super(PreprocessTab, self).__init__(parent)

        self.preprocess_manager = PreprocessManager(self)

        self.create_open_file_frame()
        self.create_domain_drop_box()
        self.create_selected_attribute_frame()
        self.create_selected_attribute_numeric_frame()
        self.create_file_info_frame()
        self.create_file_attributes_frame()

        self.attach_all_to_layout()
        self.pack_start(self.page_layout, True, True, 0)

        self.set_signals()
        self.set_connections()

    def set_signals(self):
        pass

    def set_connections(self):
        pass

    def attach_all_to_layout(self):
        self.page_layout.attach(self.boxes['open_file'], 0, 0, 2, 1)
        self.page_layout.attach(self.frames['file_info'], 0, 1, 1, 1)
        self.page_layout.attach(self.frames['class_attribute'], 1, 1, 1, 1)
        self.page_layout.attach(self.frames['attributes_list'], 0, 2, 1, 4)
        self.page_layout.attach(self.frames['selected_attribute'], 1, 2, 1, 3)
        self.page_layout.attach(self.frames['selected_attribute_statistics'], 1, 5, 1, 1)

    def create_selected_attribute_frame(self):
        frame = self.create_frame('selected_attribute' ,'Selected attribute')
        box = self.create_box(frame, 'selected_attribute')
        self.create_grid(box, 'selected_attribute')

        attribute_statistics_labels = ['Name', 'Missing', 'Distinct', 'Type', 'Unique']
        attribute_data_labels = ['attribute_name', 'attribute_missing', 'attribute_distinct',
                                 'attribute_type', 'attribute_unique']

        self.insert_static_label_data_label('selected_attribute', attribute_statistics_labels,
                                            attribute_data_labels)

        self.insert_scrollable_tree_view(box, 'selected_attribute_list')

    def create_selected_attribute_numeric_frame(self):
        frame = self.create_frame('selected_attribute_statistics', 'Numeric statistics')
        self.create_grid(frame, 'selected_attribute_statistics')

        attribute_statistics_labels = ['Mean', 'Median', 'Mode', 'Min', 'Max', 'Stand. Dev']
        attribute_data_labels = ['attribute_mean', 'attribute_median',
                                 'attribute_mode', 'attribute_min', 'attribute_max',
                                 'attribute_stand_dev']

        self.insert_static_label_data_label('selected_attribute_statistics',
                                            attribute_statistics_labels,
                                            attribute_data_labels)

    def create_open_file_frame(self):
        open_file_box = self.create_box(None, 'open_file', False)
        open_file_box.set_spacing(5)

        open_file_box.pack_start(Gtk.Label("File: "), False, False, 0)

        self.text_inputs['file_path'] = Gtk.Entry()
        self.buttons['file_select'] = Gtk.Button("Select")
        self.buttons['file_open'] = Gtk.Button("Open")

        self.text_inputs['file_path'].set_hexpand(True)

        open_file_box.pack_start(self.text_inputs['file_path'], True, True, 0)
        open_file_box.pack_start(self.buttons['file_select'], False, False, 0)
        open_file_box.pack_start(self.buttons['file_open'], False, False, 0)

    def create_file_info_frame(self):
        frame = self.create_frame('file_info', 'Current database')
        box = self.create_box(frame, 'file_info')
        self.create_grid(box, 'file_info')

        file_info_static_labels = ['Name', 'Weights', 'Instances', 'Attributes']
        file_info_data_labels = ['file_info_name', 'file_info_weights',
                                 'file_info_instances', 'file_info_attributes']

        self.insert_static_label_data_label('file_info', file_info_static_labels, file_info_data_labels)

    def create_file_attributes_frame(self):
        attributes_list_frame = self.create_frame('attributes_list', 'Attributes')
        attributes_list_box = self.create_box(attributes_list_frame, 'attributes_list')

        attributes_buttons_box = self.create_box(None, 'attributes_buttons', False)
        attributes_buttons_box.set_spacing(10)
        attributes_buttons_box.set_homogeneous(True)

        self.insert_buttons(attributes_buttons_box,
                            ['attributes_remove', 'attributes_regex'],
                            ['Remove', 'Domain'])


        attributes_list_box.pack_start(self.boxes['attributes_buttons'], False, False, 0)

        self.insert_scrollable_tree_view(attributes_list_box, 'attributes_list')

    def create_domain_drop_box(self):
        frame = self.create_frame('class_attribute', 'Class attribute')

        self.combo_boxes['class_attribute'] = Gtk.ComboBoxText()
        self.combo_boxes['class_attribute'].set_border_width(5)

        frame.add(self.combo_boxes['class_attribute'])