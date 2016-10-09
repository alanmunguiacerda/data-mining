#!/usr/bin/env python
# -*- coding: utf-8 -*-
import exceptions
import gi
import copy
import ntpath

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject
from controladores.CsvManager import CsvManager
from vistas.errordialog import ErrorDialog


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

        for var in headers_list:
            args[2].append_text(var)

        args[2].set_active(0)

    def load_attributes_tree_view(self, *args):
        headers_list = self.csv.headers

        list_store = Gtk.ListStore(GObject.TYPE_INT, GObject.TYPE_STRING, GObject.TYPE_STRING)

        for i, var in enumerate(headers_list):
            list_store.append([i, var, '<span foreground="green">Correct</span>'])

        args[2].set_model(list_store)

        for i, col_title in enumerate(["Number", "Attribute", "Status"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(col_title, renderer, markup=i)

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

    def set_file_in_table(self, tree_view, modify_cell):
        headers = ["Action"]
        headers.extend(copy.deepcopy(self.csv.headers))

        list_store = Gtk.ListStore(*[str] * len(headers))

        data = copy.deepcopy(self.csv.data)

        i = 0
        for item in data:
            j = 0
            for elem in self.csv.headers:
                if elem in self.csv.wrong_registers:
                    wrong_registers = self.csv.wrong_registers[elem]
                    try:
                        index = wrong_registers.index(i)
                    except exceptions.Exception:
                        index = -1

                    if index is not -1:
                        item[j] = '<span background="red" foreground="white">' + item[j] + '</span>'
                j += 1

            item.insert(0, "")

            list_store.append(item)
            i += 1

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
            print "Delete"
            print self.csv.data

    def add_rows(self, rows):
        if self.csv.add_tuples(rows):
            print "ADD SOMETHING"
            print self.csv.data

    def modify_rows(self, rows):
        if self.csv.fill_tuples(rows):
            print "MODIFY SOMETHING"
            print self.csv.data

    def set_attribute_domain(self, widget, regexp, attribute, row, view):
        if self.csv.set_domain(regexp, attribute):
            pass
        else:
            ErrorDialog("Error", "Invalid regular expression", None)

        model = view.get_model()
        if attribute in self.csv.wrong_registers:
            model.set_value(row, 2, '<span foreground="red">Not valid</span>')
        else:
            model.set_value(row, 2, '<span foreground="green">Correct</span>')

    def undo(self, widget, window):
        if len(self.csv.dataVersions) > 0:
            self.csv.rollback()
            window.emit('refresh-all', "DummyData")
        if len(self.csv.dataVersions) < 1:
            window.edit_undo.set_sensitive(False)