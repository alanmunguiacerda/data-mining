import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject
from vistas.BaseTab import BaseTab
from vistas.ErrorDialog import ErrorDialog
from controladores.CsvManager import CsvManager


class ClassificationTab(BaseTab):

    def __init__(self, parent):
        BaseTab.__init__(self, parent)

        self.csv_manager = CsvManager()

        self.create_classification_type_frame()
        self.create_trial_tuple_frame()
        self.create_model_tuple_frame()

        self.attach_all_to_layout()
        self.pack_start(self.page_layout, True, True, 0)

        self.set_signals()
        self.set_connections()

    def set_signals(self):
        pass

    def set_connections(self):
        pass

    def attach_all_to_layout(self):
        self.page_layout.attach(self.frames['classification_type'], 0, 0, 1, 1)
        self.page_layout.attach(self.frames['trial_tuple'], 0, 1, 1, 1)
        self.page_layout.attach(self.frames['model_tuple'], 0, 2, 1, 1)

    def create_classification_type_frame(self):
        frame = self.create_frame('classification_type', 'Classification type')
        box = self.create_box(frame, 'classification_type', False)

        box.set_spacing(10)
        box.set_homogeneous(True)

        self.buttons['zero_r_type'] = Gtk.RadioButton("Zero R")
        self.buttons['one_r_type'] = Gtk.RadioButton("One R")
        self.buttons['naive_bayes_type'] = Gtk.RadioButton("Naive Bayes")

        self.buttons['zero_r_type'].set_group(None)
        self.buttons['one_r_type'].join_group(self.buttons['zero_r_type'])
        self.buttons['naive_bayes_type'].join_group(self.buttons['one_r_type'])

        box.pack_start(self.buttons['zero_r_type'], False, False, 0)
        box.pack_start(self.buttons['one_r_type'], False, False, 0)
        box.pack_start(self.buttons['naive_bayes_type'], False, False, 0)

    def create_trial_tuple_frame(self):
        frame = self.create_frame('trial_tuple', 'Trial tuple')
        grid = self.create_grid(frame, 'trial_tuple')
        box = self.create_box(grid, 'trial_tuple', False)

        self.create_scrollable_window(box, 'trial_tuple')

        predict_button_box = self.create_box(None, 'predict_button', False)
        predict_button_box.set_spacing(10)
        predict_button_box.set_homogeneous(True)

        self.insert_buttons(predict_button_box,
                            ['predict'],
                            ['Predict'])

        box.set_spacing(10)
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)

        grid.attach(box, 0, 0, 1, 1)
        grid.attach(predict_button_box, 1, 0, 1, 1)

    def create_model_tuple_frame(self):

        frame = self.create_frame('model_tuple', 'Model tuple')
        box = self.create_box(frame, 'model_tuple', False)
        new_scrollable_window = self.create_scrollable_window(box, 'model_tuple')
        grid = self.create_grid(new_scrollable_window, 'model_tuple')

        attribute_statistics_labels = ['Accuracy']
        attribute_data_labels = ['accuracy']

        self.insert_static_label_data_label('model_tuple', attribute_statistics_labels, attribute_data_labels,
                                            columns=2, data_col_width=2, start_column=1, start_row=0)

        box.set_spacing(10)
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)

        new_scrollable_window.add(grid)





