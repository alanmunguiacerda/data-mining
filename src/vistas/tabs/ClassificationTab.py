import gi
import constants
from negocios.ClassificationManager import ClassificationManager

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject
from vistas.tabs.BaseTab import BaseTab

class ClassificationTab(BaseTab):

    def __init__(self, parent):
        BaseTab.__init__(self, parent, True, True)

        self.classification_manager = ClassificationManager(self)
        self.type = 0

        self.create_classification_type_frame()
        self.create_trial_tuple_frame()
        self.create_model_tuple_frame()

        self.attach_all_to_layout()
        self.pack_start(self.box, True, True, 0)

        self.set_signals()
        self.set_connections()

    def set_signals(self):
        GObject.signal_new('page-selected', self, GObject.SIGNAL_RUN_LAST, GObject.TYPE_PYOBJECT,
                           ())

    def set_connections(self):
        self.buttons['zero_r_type'].connect("toggled", self.get_radio_button_active)
        self.buttons['one_r_type'].connect("toggled", self.get_radio_button_active)
        self.buttons['naive_bayes_type'].connect("toggled", self.get_radio_button_active)

        self.buttons['predict'].connect('clicked', self.classification_manager.create_model)
        self.connect('page-selected', self.classification_manager.create_classification_interface)

    def attach_all_to_layout(self):
        self.box.pack_start(self.frames['classification_type'], False, False, 0)
        self.box.pack_start(self.frames['trial_tuple'], True, True, 0)
        self.box.pack_start(self.frames['model_tuple'], True, True, 0)

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
        box = self.create_box(frame, 'trial_tuple', False)

        new_scrollable_window = self.create_scrollable_window(box, 'trial_tuple')
        grid = self.create_grid(new_scrollable_window, 'trial_tuple', True)

        predict_button_box = self.create_box(box, 'predict_button', False)

        self.insert_buttons(predict_button_box,
                            ['predict'],
                            ['Predict'])

        box.set_spacing(5)

        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        grid.set_column_homogeneous(False)

        predict_button_box.set_spacing(10)
        predict_button_box.set_homogeneous(True)

        box.add(predict_button_box)

    def create_model_tuple_frame(self):
        frame = self.create_frame('model_tuple', 'Model tuple')
        box = self.create_box(frame, 'model_tuple', False)

        new_scrollable_window = self.create_scrollable_window(box, 'model_tuple')
        grid = self.create_grid(new_scrollable_window, 'model_tuple')

        attribute_statistics_labels = ['Accuracy']
        attribute_data_labels = ['accuracy']

        self.insert_static_label_data_label('model_tuple', attribute_statistics_labels, attribute_data_labels,
                                            columns=2, data_col_width=2, start_column=2, start_row=0)

        box.set_spacing(10)
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        grid.set_column_homogeneous(False)

    def get_radio_button_active(self, widget):
        if self.buttons['zero_r_type'].get_active():
            self.type = constants.ZERO_R_TYPE
        elif self.buttons['one_r_type'].get_active():
            self.type = constants.ONE_R_TYPE
        else:
            self.type = constants.NAIVE_BAYES






