#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject

from src.vistas.tabs.BaseTab import BaseTab
from src.vistas.dialogs.ErrorDialog import ErrorDialog
from src.negocios.PreprocessManager import PreprocessManager
from src.vistas.dialogs.DomainDialog import DomainDialog
from src.vistas.dialogs.ModifyFileDialog import ModifyFileDialog

class PreprocessTab(BaseTab):

    def __init__(self, parent):
        BaseTab.__init__(self, parent)

        self.preprocess_manager = PreprocessManager(self)

        self.create_open_file_frame()
        self.create_class_attribute_frame()
        self.create_selected_attribute_frame()
        self.create_selected_attribute_numeric_frame()
        self.create_file_info_frame()
        self.create_file_attributes_frame()

        self.attach_all_to_layout()
        self.pack_start(self.page_layout, True, True, 0)

        self.set_signals()
        self.set_connections()

    def set_signals(self):
        GObject.signal_new('file-path-ready', self, GObject.SIGNAL_RUN_LAST, GObject.TYPE_PYOBJECT,
                           (GObject.TYPE_PYOBJECT,))
        GObject.signal_new('after-file-loaded', self, GObject.SIGNAL_RUN_LAST, GObject.TYPE_PYOBJECT,
                           ())
        GObject.signal_new('reg-exp-ready', self, GObject.SIGNAL_RUN_LAST, GObject.TYPE_PYOBJECT,
                           (GObject.TYPE_PYOBJECT, GObject.TYPE_PYOBJECT, Gtk.TreeIter))
        GObject.signal_new('refresh-all', self, GObject.SIGNAL_RUN_LAST, GObject.TYPE_PYOBJECT,
                           ())
        GObject.signal_new('registers-edited', self, GObject.SIGNAL_RUN_LAST, GObject.TYPE_PYOBJECT,
                           ())
        GObject.signal_new('update-transform-menu', self, GObject.SIGNAL_RUN_LAST, GObject.TYPE_PYOBJECT,
                           (GObject.TYPE_PYOBJECT, GObject.TYPE_PYOBJECT,))
        GObject.signal_new('class-changed', self, GObject.SIGNAL_RUN_LAST, GObject.TYPE_PYOBJECT,
                           ())

    def set_connections(self):
        self.buttons['file_select'].connect('clicked', self.on_open_file_menu)
        self.buttons['file_open'].connect('clicked', self.on_open_file_clicked)

        self.connect("after-file-loaded", self.preprocess_manager.clean_attributes_widgets,
                     self.tree_views, self.combo_boxes, self.labels)
        self.connect("after-file-loaded", self.parent.enable_save_edit_file)
        self.connect("after-file-loaded", self.parent.load_transformation_menu)
        self.connect("file-path-ready", self.preprocess_manager.set_file, self.parent.menu_options['edit_undo'])
        self.connect("after-file-loaded", self.preprocess_manager.load_combo_box_attributes,
                     self.combo_boxes['class_attribute'])
        self.connect("after-file-loaded", self.preprocess_manager.load_attributes_tree_view,
                     self.tree_views['attributes_list'])
        self.connect("after-file-loaded", self.preprocess_manager.set_file_info, self.labels)
        self.connect("after-file-loaded", self.toggle_attributes_buttons, False)

        self.tree_views['attributes_list'].connect("cursor-changed",
                                          self.preprocess_manager.set_data_in_table,
                                          self.tree_views['selected_attribute_list'])

        self.tree_views['attributes_list'].connect("cursor-changed",
                                          self.preprocess_manager.set_attribute_info,
                                          self.labels)

        self.tree_views['attributes_list'].connect("cursor-changed", self.toggle_attributes_buttons, True)

        self.buttons['attributes_remove'].connect("clicked", self.on_remove_attribute_clicked)
        self.buttons['attributes_regex'].connect("clicked", self.on_regexp_clicked)

        self.connect('reg-exp-ready', self.preprocess_manager.set_attribute_domain,
                     self.tree_views['attributes_list'])

        self.connect("refresh-all", self.preprocess_manager.clean_attributes_widgets,
                     self.tree_views, self.combo_boxes, self.labels)
        self.connect("refresh-all", self.preprocess_manager.load_combo_box_attributes,
                     self.combo_boxes['class_attribute'])
        self.connect("refresh-all", self.preprocess_manager.load_attributes_tree_view,
                     self.tree_views['attributes_list'])
        self.connect("refresh-all", self.preprocess_manager.set_file_info, self.labels)
        self.connect("refresh-all", self.refresh_parent)
        self.connect("refresh-all", self.parent.load_transformation_menu)

        # Registers edited sets undo active
        self.connect('registers-edited', self.parent.on_registers_edited)

        # Transform menu update
        self.connect('update-transform-menu', self.preprocess_manager.update_transform_menu)
        self.combo_boxes['class_attribute'].connect("changed", self.class_changed)
        self.combo_boxes['class_attribute'].connect("changed", self.preprocess_manager.csv.class_index_changed)

    def attach_all_to_layout(self):
        self.page_layout.attach(self.boxes['open_file'], 0, 0, 2, 1)
        self.page_layout.attach(self.frames['file_info'], 0, 1, 1, 1)
        self.page_layout.attach(self.frames['class_attribute'], 1, 1, 1, 1)
        self.page_layout.attach(self.frames['attributes_list'], 0, 2, 1, 4)
        self.page_layout.attach(self.frames['selected_attribute'], 1, 2, 1, 3)
        self.page_layout.attach(self.frames['selected_attribute_statistics'], 1, 5, 1, 1)

    def create_selected_attribute_frame(self):
        frame = self.create_frame('selected_attribute', 'Selected attribute')
        box = self.create_box(frame, 'selected_attribute')
        self.create_grid(box, 'selected_attribute')

        attribute_statistics_labels = ['Name', 'Missing', 'Distinct', 'Type', 'Unique']
        attribute_data_labels = ['attribute_name', 'attribute_missing', 'attribute_distinct',
                                 'attribute_type', 'attribute_unique']
        extras = ['attribute_name']

        self.insert_static_label_data_label('selected_attribute', attribute_statistics_labels,
                                            attribute_data_labels, extras, 3, 2)

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
        extras = ['file_info_name']

        self.insert_static_label_data_label('file_info', file_info_static_labels,
                                            file_info_data_labels, extras, 3, 2)

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

    def create_class_attribute_frame(self):
        frame = self.create_frame('class_attribute', 'Class attribute')

        self.combo_boxes['class_attribute'] = Gtk.ComboBoxText()
        self.combo_boxes['class_attribute'].set_border_width(5)

        frame.add(self.combo_boxes['class_attribute'])

    def on_open_file_clicked(self, widget):
        string = self.text_inputs['file_path'].get_text()

        if string and string.strip() and string.endswith('.csv'):
            if os.path.isfile(string):
                self.emit('file-path-ready', self.text_inputs['file_path'].get_text())
                self.emit('after-file-loaded')
            else:
                ErrorDialog("Error", "File not found", None)

    def on_open_file_menu(self, widget):
        dialog = Gtk.FileChooserDialog("Select a file: ", None, Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        filter = Gtk.FileFilter()
        filter.add_pattern("*.csv")
        dialog.set_filter(filter)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.text_inputs['file_path'].set_text(dialog.get_filename())
            if type(widget).__name__ == 'MenuItem':
                self.on_open_file_clicked(widget)
                pass
        dialog.destroy()

    def toggle_attributes_buttons(self, widget, sensitive):
        self.buttons['attributes_remove'].set_sensitive(sensitive)
        self.buttons['attributes_regex'].set_sensitive(sensitive)

    def on_remove_attribute_clicked(self, widget):
        model, row = self.tree_views['attributes_list'].get_selection().get_selected()
        if not row:
            return
        self.preprocess_manager.remove_attribute(model[row][1])
        self.emit('refresh-all')

    def on_regexp_clicked(self, widget):
        model, row = self.tree_views['attributes_list'].get_selection().get_selected()
        if not row:
            return
        attribute_name = model[row][1]

        dialog = DomainDialog(self, attribute_name)

        response = dialog.run()

        if response == Gtk.ResponseType.OK and attribute_name:
            self.emit('reg-exp-ready', dialog.get_regexp(), attribute_name, row)

        dialog.destroy()

    def on_edit_registers(self, widget):
        dialog = ModifyFileDialog(self)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            dialog.commit()
            self.preprocess_manager.set_file_info(None, self.labels)

        dialog.destroy()

    def on_save_file_menu(self, widget):
        dialog = Gtk.FileChooserDialog("Save file as: ", None,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.preprocess_manager.save_file(dialog.get_filename())

        dialog.destroy()

    def refresh_parent(self, widget):
        self.parent.emit('update-pages')

    def class_changed(self, widget):
        self.emit("class-changed")
