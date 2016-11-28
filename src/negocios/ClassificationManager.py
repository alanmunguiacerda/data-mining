import src.constants
import gi
import sys

from copy import deepcopy
from src.vistas.dialogs.ErrorDialog import ErrorDialog
from src.Usseful import take_out_class
from src.controladores.CsvManager import CsvManager
from src.analisis.Classification import Classification

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ClassificationManager:
    csv_manager = CsvManager()

    def __init__(self, parent):
        self.parent = parent

        self.data_changed = False
        self.type = 0

        self.labels_trial = {}
        self.input_trial = {}
        self.labels_static_model = {}
        self.labels_data_model = {}
        self.numeric_indexes = []
        self.data = []

    def delete_widgets(self):
        keys = self.labels_trial.keys()
        for key in keys:
            self.parent.grids['trial_tuple'].remove(self.labels_trial[key])
            self.parent.grids['trial_tuple'].remove(self.input_trial[key])

        keys = self.labels_static_model.keys()
        for key in keys:
            self.parent.grids['model_tuple'].remove(self.labels_static_model[key])
            self.parent.grids['model_tuple'].remove(self.labels_data_model[key])

    def clear_all(self):
        self.delete_widgets()

        self.labels_trial.clear()
        self.input_trial.clear()

        self.labels_static_model.clear()
        self.labels_data_model.clear()

        del self.numeric_indexes[:]

        self.parent.labels['accuracy'].set_text("")

    def trial_widgets(self, attribute, row):
        label = Gtk.Label(attribute + ': ')

        label.set_halign(Gtk.Align.START)

        if self.csv_manager.get_numeric_items(attribute):
            widget = Gtk.SpinButton()
            self.numeric_indexes.append(row if row < self.csv_manager.class_index else row + 1)
            widget.set_numeric(True)
            widget.configure(Gtk.Adjustment(lower=sys.float_info.min, upper=sys.float_info.max, step_increment=1.0),
                             10.0, sys.float_info.dig)
        else:
            values = self.csv_manager.get_index_counters(attribute)
            widget = Gtk.ComboBoxText()
            for elem in values.items():
                if elem[0] != src.constants.MISSING_DATA_SYMBOL:
                    widget.append_text(elem[0])
            widget.set_active(0)

        self.labels_trial[attribute + '_trial'] = label
        self.input_trial[attribute + '_trial'] = widget

        self.parent.grids['trial_tuple'].attach(label, 0, row, 1, 1)
        self.parent.grids['trial_tuple'].attach(widget, 1, row, 1, 1)

    def model_widgets(self, attribute, row):
        label = Gtk.Label(attribute + ': ')
        label_d = Gtk.Label()

        label.set_halign(Gtk.Align.START)
        label_d.set_halign(Gtk.Align.START)

        self.labels_static_model[attribute + '_model'] = label
        self.labels_data_model[attribute + '_model'] = label_d

        self.parent.grids['model_tuple'].attach(label, 0, row, 1, 1)
        self.parent.grids['model_tuple'].attach(label_d, 1, row, 2, 1)

    def create_classification_interface(self, widget):
        # if len(self.labels_trial.items()) > 0:
        if not self.data_changed:
            return

        self.clear_all()
        self.data_changed = False

        for ind, elem in enumerate(self.csv_manager.headers):
            if ind == self.csv_manager.class_index:
                self.model_widgets(elem, ind)
                continue

            ind_aux = ind if ind < self.csv_manager.class_index else ind - 1
            self.trial_widgets(elem, ind_aux)

            self.model_widgets(elem, ind)

        self.parent.grids['trial_tuple'].show_all()
        self.parent.grids['model_tuple'].show_all()

        self.data_changed = False

    def create_model(self, widget):
        if self.data_changed:
            ErrorDialog("Classification error", "Reload the tab to predict", None)
            return

        self.parent.labels['accuracy'].set_text("")

        self.clean_database()

        trial_tuple = self.get_trial_tuple()

        if self.type == src.constants.ZERO_R_TYPE:
            model = Classification.zero_r([elem[self.csv_manager.class_index] for elem in self.data])
            model_tuple = Classification.zero_r_prediction(trial_tuple, model, self.csv_manager.class_index)
        elif self.type == src.constants.ONE_R_TYPE:
            model = Classification.one_r(self.data,  self.csv_manager.class_index, self.numeric_indexes)
            model_tuple = Classification.one_r_prediction(trial_tuple, model, self.csv_manager.class_index)
        else:
            model = Classification.naive_bayes(self.data, self.csv_manager.class_index, self.numeric_indexes)
            model_tuple = Classification.naive_bayes_prediction(trial_tuple, model,
                                                                self.csv_manager.class_index, self.numeric_indexes)

        self.set_model_tuple(model_tuple)
        self.calculate_accuracy(model)

        self.parent.grids['model_tuple'].show_all()

    def clean_database(self):
        self.data = deepcopy(self.csv_manager.data)

        for ind, instance in enumerate(self.data):
            for elem in instance:
                if elem == src.constants.MISSING_DATA_SYMBOL:
                    del self.data[ind]
                    break

        pass

    def get_trial_tuple(self):
        trial_tuple = []
        for key in self.csv_manager.headers:
            if key + '_trial' not in self.input_trial:
                continue

            widget = self.input_trial[key + '_trial']
            if type(widget) == Gtk.ComboBoxText:
                val = widget.get_active_text()
            else:
                val = widget.get_value()

            trial_tuple.append(val)

        return trial_tuple

    def set_model_tuple(self, model_tuple):
        if len(model_tuple) == 0:
            return

        for ind, key in enumerate(self.csv_manager.headers):
            label = self.labels_data_model[key+'_model']
            label.set_text(str(model_tuple[ind]))

    def calculate_accuracy(self, model):
        data_without_class = take_out_class(self.data, self.csv_manager.class_index)

        if self.type == src.constants.ZERO_R_TYPE:
            model_data = [Classification.zero_r_prediction(elem, model,
                                                           self.csv_manager.class_index) for elem in data_without_class]
        elif self.type == src.constants.ONE_R_TYPE:
            model_data = [Classification.one_r_prediction(elem, model,
                                                          self.csv_manager.class_index) for elem in data_without_class]
        else:
            model_data = [Classification.naive_bayes_prediction(elem, model,
                                                                self.csv_manager.class_index, self.numeric_indexes)
                          for elem in data_without_class]

        accuracy = Classification.calculate_accuracy(self.data, model_data, self.csv_manager.class_index)

        self.parent.labels['accuracy'].set_text(str(accuracy))

    def set_data_changed(self):
        self.data_changed = True

