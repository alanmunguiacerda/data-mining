#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import exceptions
import ntpath

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject
from controladores.CsvManager import CsvManager
from analisis.NumericTransformations import NumericTransformations
from src.vistas.dialogs.MinMaxDialog import MinMaxDialog
from vistas.dialogs.ErrorDialog import ErrorDialog

class PreprocessManager:
    def __init__(self, parent):
        self.parent = parent
        self.csv = CsvManager()

    def set_file(self, widget, file_name, edit_undo):
        if self.csv.load_file(file_name):
            edit_undo.set_sensitive(False)

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
            column = Gtk.TreeViewColumn(item, renderer, markup=i)
            data[0].append_column(column)

    def save_file(self, path):
        self.csv.save_version(path)

    def load_combo_box_attributes(self, widget, combo_box):
        headers_list = self.csv.headers

        for var in headers_list:
            combo_box.append_text(var)

        combo_box.set_active(0)

    def load_attributes_tree_view(self, widget, tree):
        headers_list = self.csv.headers

        list_store = Gtk.ListStore(GObject.TYPE_INT, GObject.TYPE_STRING,
                                   GObject.TYPE_STRING, GObject.TYPE_STRING)

        for i, var in enumerate(headers_list):
            valid = (("green", "Correct"), ("red", "Not valid"))[var in self.csv.wrong_registers]
            list_store.append([i, var,
                               '<span foreground="'+valid[0]+'">' + valid[1] + '</span>',
                               self.csv.get_domain(var)])

        tree.set_model(list_store)

        for i, col_title in enumerate(["Number", "Attribute", "Status", "Domain"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(col_title, renderer, markup=i)

            # Add columns to TreeView
            tree.append_column(column)

    def clean_attributes_widgets(self, widget, trees, combo_boxes, labels):
        # Tree view cleaning
        columns = trees['attributes_list'].get_columns()
        for column in columns:
            trees['attributes_list'].remove_column(column)

        columns = trees['selected_attribute_list'].get_columns()
        for column in columns:
            trees['selected_attribute_list'].remove_column(column)

        # Combo box cleaning
        combo_boxes['class_attribute'].remove_all()

        for k, v in labels.iteritems():
            if 'file' in k:
                continue
            v.set_text('')


    def set_file_info(self, widget, labels):
        _, filename = ntpath.split(self.csv.filename)
        filename = filename.split('.')[0]

        labels['file_info_name'].set_text(filename)
        labels['file_info_attributes'].set_text(str(len(self.csv.headers)))
        instances = len(self.csv.data)
        labels['file_info_instances'].set_text(str(instances))
        labels['file_info_weights'].set_text("{0:.1f}".format(instances))

    def remove_attribute(self, attribute_name):
        if self.csv.delete_attribute(attribute_name):
            self.parent.emit('registers-edited')

    def set_attribute_info(self, widget, labels):
        model, row = widget.get_selection().get_selected()

        if not row:
            return

        attribute_name = model[row][1]
        counters = self.csv.get_index_counters(attribute_name)
        # Attribute name label
        labels['attribute_name'].set_label(attribute_name)

        # Missing
        missing = self.csv.missing_values(attribute_name)
        labels['attribute_missing'].set_label(str(missing) + "( " + str((missing * 100) / len(self.csv.data)) + "% )")

        # Distinct label
        labels['attribute_distinct'].set_label(str(len(counters)))

        unique_count = 0
        numeric = True
        for k, v in counters.iteritems():
            if v == 1:
                unique_count += 1
            if self.csv.check_type(k) is str:
                numeric = False

        # Type label
        if len(counters) is 2:
            labels['attribute_type'].set_label("Binary")
        else:
            labels['attribute_type'].set_label("Numeric" if numeric else "Nominal")
        # Unique label
            labels['attribute_unique'].set_label(str(unique_count) + "( " + str((unique_count * 100) / len(self.csv.data)) + "% )")

        # Mean
        labels['attribute_mean'].set_label('{!s}'.format(self.csv.get_mean(attribute_name)))
        # Median
        labels['attribute_median'].set_label('{!s}'.format(self.csv.get_median(attribute_name)))
        # Mode
        mode = ' '.join(str(x)+', ' for x in self.csv.get_mode(attribute_name))
        if len(mode) > 15:
            labels['attribute_mode'].set_label(mode[0:15]+'...')
        else:
            labels['attribute_mode'].set_label(mode)
        # Min
        labels['attribute_min'].set_label('{!s}'.format(self.csv.get_min(attribute_name)))
        # Max
        labels['attribute_max'].set_label('{!s}'.format(self.csv.get_max(attribute_name)))
        # Std
        labels['attribute_stand_dev'].set_label('{!s}'.format(self.csv.get_standard_deviation(attribute_name)))

    def set_file_in_table(self, tree_view, modify_cell):
        headers = ["Action"]
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
            item.insert(0, "")

            list_store.append(item)

        tree_view.set_model(list_store)

        for col in tree_view.get_columns():
            tree_view.remove_column(col)

        for i, item in enumerate(headers):
            renderer = Gtk.CellRendererText()

            if i is not 0:
                renderer.set_property("editable", True)
                renderer.connect("edited", modify_cell, i)

            column = Gtk.TreeViewColumn(item, renderer, markup=i)

            tree_view.append_column(column)

    def delete_rows(self, rows):
        if self.csv.delete_tuples(rows):
            self.parent.emit('registers-edited')

    def add_rows(self, rows):
        if self.csv.add_tuples(rows):
            self.parent.emit('registers-edited')

    def modify_rows(self, rows):
        if self.csv.fill_tuples(rows):
            self.parent.emit('registers-edited')

    def set_attribute_domain(self, widget, regexp, attribute, row, view):
        if self.csv.set_domain(regexp, attribute):
            self.parent.emit('registers-edited')
        else:
            ErrorDialog("Error", "Invalid regular expression", None)
            return False

        model = view.get_model()
        model.set_value(row, 3, regexp)
        if attribute in self.csv.wrong_registers:
            model.set_value(row, 2, '<span foreground="red">Not valid</span>')
        else:
            model.set_value(row, 2, '<span foreground="green">Correct</span>')

    def undo(self, widget, window, edit_undo):
        if len(self.csv.dataVersions) > 0:
            self.csv.rollback()
            window.emit('refresh-all')
        if len(self.csv.dataVersions) < 1:
            edit_undo.set_sensitive(False)

    def update_transform_menu(self, widget, menu, menuBar):
        num_attributes = self.csv.get_numeric_attributes()
        for key, value in menu.iteritems():
            if key.startswith('transform'):
                for x in value['sub']['menu'].get_children():
                    value['sub']['menu'].remove(x)
                for attribute in num_attributes:
                    new_menu = Gtk.MenuItem(attribute)
                    value['sub']['sub'][attribute] = new_menu
                    value['sub']['menu'].append(new_menu)
                    new_menu.connect("activate", self.numeric_transform, key)
                value['menu'].set_sensitive(True)
        menuBar.show_all()

    def numeric_transform(self, widget, algorithm):
        attribute = widget.get_label()
        values = self.csv.get_numeric_items(attribute)

        if not values:
            ErrorDialog("Error", "That attribute contains non numeric values", None)
            return False

        normalized = None
        if 'min_max' in algorithm:
            normalized = self.numeric_min_max(values)
        elif 'z_score_std' in algorithm:
            normalized = NumericTransformations.z_score_standard(values)
        elif 'z_score_abs' in algorithm:
            normalized = NumericTransformations.z_score_absolute(values)
        elif 'decimal' in algorithm:
            normalized = NumericTransformations.decimal_scaling(values)

        if not  normalized:
            ErrorDialog("Error", "Couldn't calculate the normalized values", None)
            return False

        if not self.csv.replace_column(attribute, normalized):
            ErrorDialog("Error", "The data provided couldn't be transformed", None)
            return False

        self.parent.emit('refresh-all')
        self.parent.emit('registers-edited')
        return True

    def numeric_min_max(self, values):
        dialog = MinMaxDialog(self)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            data = dialog.get_data()
            for key, value in data.iteritems():
                try:
                    data[key] = float(value)
                except ValueError:
                    ErrorDialog("Error", "All the values must be numeric", None)
                    dialog.destroy()
                    return False

            normalized = NumericTransformations.min_max(values, data['old_min'], data['old_max'],
                                                        data['new_min'], data['new_max'])
        dialog.destroy()

        return normalized