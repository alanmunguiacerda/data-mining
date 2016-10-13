#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from PreprocessTab import PreprocessTab

class MainWindow2(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Test window")
        self.set_connections()

        self.set_style()
        self.set_layout()
        self.create_notebook()

        self.create_pre_process_page()

    def set_style(self):
        self.set_border_width(10)
        self.set_default_size(800, 600)

    def set_layout(self):
        self.layout = Gtk.Box()
        self.layout.set_orientation(Gtk.Orientation.VERTICAL)
        self.add(self.layout)

    def set_connections(self):
        self.connect("delete-event", Gtk.main_quit)

    def create_notebook(self):
        self.notebook = Gtk.Notebook()
        self.layout.pack_start(self.notebook, True, True, 0)

    def create_pre_process_page(self):
        self.pre_process_page = PreprocessTab(self)
        self.pre_process_page.set_border_width(10)
        self.notebook.append_page(self.pre_process_page, Gtk.Label("Pre-process"))

