#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class BaseTab(Gtk.Box):
    def __init__(self, parent, box=False, orientation=False):
        Gtk.Box.__init__(self)
        self.parent = parent

        if not box:
            self.page_layout = Gtk.Grid()
        else:
            self.box = Gtk.Box()

        self.frames = {}
        self.boxes = {}
        self.grids = {}
        self.labels = {}
        self.text_inputs = {}
        self.spin_inputs = {}
        self.buttons = {}
        self.scrollable_windows = {}
        self.tree_views = {}
        self.combo_boxes = {}

        if not box:
            self.create_page_layout()
        else:
            self.create_page_box(orientation)

    def create_page_layout(self):
        self.page_layout.set_column_homogeneous(True)
        self.page_layout.set_row_spacing(10)
        self.page_layout.set_column_spacing(10)

    def create_page_box(self, orientation):
        self.box.set_orientation(orientation)

    def create_frame(self, frame_name, display_name):
        if frame_name in self.frames:
            return False

        new_frame = Gtk.Frame()
        new_frame.set_label(display_name)

        self.frames[frame_name] = new_frame
        return new_frame

    def create_box(self, parent, box_name, orientation=True):
        if box_name in self.boxes:
            return False

        new_box = Gtk.Box()
        if orientation:
            new_box.set_orientation(Gtk.Orientation.VERTICAL)
        else:
            new_box.set_orientation(Gtk.Orientation.HORIZONTAL)

        self.boxes[box_name] = new_box

        if type(parent) is Gtk.Frame:
            parent.add(new_box)

        return new_box

    def create_grid(self, parent, grid_name, expand=False):
        if grid_name in self.grids:
            return False

        new_grid = Gtk.Grid()
        new_grid.set_column_homogeneous(True)
        new_grid.set_row_homogeneous(True)

        self.grids[grid_name] = new_grid

        if type(parent) is Gtk.Box:
            parent.pack_start(new_grid, expand, expand, 0)
        elif type(parent) is Gtk.Frame or type(parent) is Gtk.ScrolledWindow:
            parent.add(new_grid)

        return new_grid

    def create_scrollable_window(self, parent, scrollable_window_name):
        new_scrollable = Gtk.ScrolledWindow()
        self.scrollable_windows[scrollable_window_name] = new_scrollable
        self.scrollable_windows[scrollable_window_name].set_policy(Gtk.PolicyType.AUTOMATIC,
                                                                   Gtk.PolicyType.AUTOMATIC)
        if parent:
            parent.pack_start(self.scrollable_windows[scrollable_window_name], True, True, 0)

        return new_scrollable

    def insert_static_label_data_label(self, grid_name, static_labels, data_labels, extras=[],
                                       columns=2, data_col_width=3, start_column=0, start_row=0):
        if grid_name not in self.grids:
            return False

        (c, r) = (start_column, start_row)
        self.grids[grid_name].set_border_width(5)
        for st_lb, dt_lb in zip(static_labels, data_labels):
            static_label = Gtk.Label(st_lb+': ')
            self.labels[dt_lb] = Gtk.Label()

            static_label.set_halign(Gtk.Align.START)
            self.labels[dt_lb].set_halign(Gtk.Align.START)

            self.grids[grid_name].attach(static_label, c*data_col_width, r, 1, 1)
            # Only God and my past me knows what does this line do, beware with the line,
            # it likes to crash the program when is deleted
            cols = (data_col_width-1, (data_col_width-1)*columns)[dt_lb in extras]
            self.grids[grid_name].attach(self.labels[dt_lb], c*data_col_width+1, r, cols, 1)

            c += 1
            if c >= columns + start_column or dt_lb in extras:
                (c, r) = (start_column, r + 1)

    def insert_static_label_combo_box(self, grid_name, static_labels, combo_box,
                                       extras=[], start_col=0, start_row=0,
                                       columns=2, data_col_width=3):

        if not grid_name in self.grids:
            return False

        (c, r) = (start_col, start_row)
        self.grids[grid_name].set_border_width(5)
        for st_lb, cb_bx in zip(static_labels, combo_box):
            static_label = Gtk.Label(st_lb + ': ')
            self.combo_boxes[cb_bx] = Gtk.ComboBoxText()
            self.combo_boxes[cb_bx].set_border_width(5)

            static_label.set_halign(Gtk.Align.START)
            self.combo_boxes[cb_bx].set_halign(Gtk.Align.START)

            self.grids[grid_name].attach(static_label, c * data_col_width, r, 1, 1)
            cols = (data_col_width - 1, (data_col_width - 1) * columns)[cb_bx in extras]
            self.grids[grid_name].attach(self.combo_boxes[cb_bx], c * data_col_width + 1, r, cols, 1)

            c += 1
            if c >= columns or cb_bx in extras:
                (c, r) = (0, r + 1)

    def insert_static_label_input_text(self, grid_name, static_labels, text_inputs,
                                       extras=[], start_col = 0, start_row = 0,
                                       columns=2, data_col_width=3):

        if not grid_name in self.grids:
            return False

        (c, r) = (start_col, start_row)
        self.grids[grid_name].set_column_spacing(5)
        for st_lb, tx_in in zip(static_labels, text_inputs):
            static_label = Gtk.Label(st_lb + ': ')
            self.text_inputs[tx_in] = Gtk.Entry()

            static_label.set_halign(Gtk.Align.START)

            self.grids[grid_name].attach(static_label, c * data_col_width, r, 1, 1)
            cols = (data_col_width - 1, (data_col_width - 1) * columns)[tx_in in extras]
            self.grids[grid_name].attach(self.text_inputs[tx_in], c * data_col_width + 1, r, cols, 1)

            c += 1
            if c >= columns or tx_in in extras:
                (c, r) = (0, r + 1)

    def insert_static_label_spin_input(self, grid_name, static_labels, spin_inputs,
                                                   extras=[], start_col=0, start_row=0,
                                                   columns=2, data_col_width=3):
        if not grid_name in self.grids:
            return False

        (c, r) = (start_col, start_row)
        self.grids[grid_name].set_column_spacing(5)
        for st_lb, sp_in in zip(static_labels, spin_inputs):
            static_label = Gtk.Label(st_lb + ': ')
            self.spin_inputs[sp_in] = Gtk.SpinButton()

            static_label.set_halign(Gtk.Align.START)

            self.grids[grid_name].attach(static_label, c * data_col_width, r, 1, 1)
            cols = (data_col_width - 1, (data_col_width - 1) * columns)[sp_in in extras]
            self.grids[grid_name].attach(self.spin_inputs[sp_in], c * data_col_width + 1, r, cols, 1)

            c += 1
            if c >= columns or sp_in in extras:
                (c, r) = (0, r + 1)

    def insert_button(self, parent, button_name, button_label, col=0, row=0, col_span=0, row_span=0):
        if button_name in self.buttons:
            return None
        self.buttons[button_name] = Gtk.Button(button_label)
        self.buttons[button_name].set_border_width(5)

        if type(parent) is Gtk.Box:
            parent.pack_start(self.buttons[button_name], False, False, 0)
        elif type(parent) is Gtk.Grid:
            parent.attach(self.buttons[button_name], col, row, col_span, row_span)

        return self.buttons[button_name]

    def insert_buttons(self, parent, buttons_names, buttons_labels, cols=0, rows=0, col_span=0, row_span=0):
        createdElements = []
        if type(parent) is Gtk.Box:
            for name, label in zip(buttons_names, buttons_labels):
                self.insert_button(parent, name, label)
        elif type(parent) is Gtk.Grid:
            (c, r) = (0, 0)
            for name, label in zip(buttons_names, buttons_labels):
                self.insert_button(parent, name, label, c * col_span, r * row_span, col_span, row_span)
                c += 1

                if c >= cols:
                    (c, r) = (0, r + 1)

    def insert_buttons(self, parent, buttons_names, buttons_labels):
        created_elements = []
        for name, label in zip(buttons_names, buttons_labels):
            if name in self.buttons:
                continue
            self.buttons[name] = Gtk.Button(label)
            self.buttons[name].set_border_width(5)
            created_elements.append(self.buttons[name])

            if parent:
                parent.pack_start(self.buttons[name], False, False, 0)

        return created_elements

    def insert_scrollable_tree_view(self, parent, tree_name):
        # possible use of a previous method
        if tree_name in self.tree_views:
            return False

        # self.scrollable_windows[tree_name] = Gtk.ScrolledWindow()
        new_scrollable_window = self.create_scrollable_window(parent, tree_name)
        self.tree_views[tree_name] = Gtk.TreeView()
        self.tree_views[tree_name].set_border_width(5)
        self.tree_views[tree_name].set_vexpand(True)

        # self.scrollable_windows[tree_name].set_policy(Gtk.PolicyType.AUTOMATIC,
        #                                               Gtk.PolicyType.AUTOMATIC)
        # self.scrollable_windows[tree_name].add(self.tree_views[tree_name])

        new_scrollable_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        new_scrollable_window.add(self.tree_views[tree_name])

        # if parent:
        #    parent.pack_start(self.scrollable_windows[tree_name], True, True, 0)

        return self.tree_views[tree_name]