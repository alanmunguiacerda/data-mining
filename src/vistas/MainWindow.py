#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from PreprocessTab import PreprocessTab
from AnalysisTab import AnalysisTab

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Litul' Yarvis")

        self.menus = {}
        self.menu_options = {}

        self.set_style()
        self.set_layout()
        self.create_menu_bar()
        self.create_notebook()

        self.create_pre_process_page()
        self.create_analysis_page()

        self.set_connections()

    def set_style(self):
        self.set_border_width(10)
        self.set_default_size(800, 600)

    def set_layout(self):
        self.layout = Gtk.Box()
        self.layout.set_orientation(Gtk.Orientation.VERTICAL)
        self.add(self.layout)

    def set_connections(self):
        self.connect("delete-event", Gtk.main_quit)
        self.menu_options['file_exit'].connect("activate", self.on_exit_file_menu)
        self.menu_options['file_open'].connect("activate", self.pre_process_page.on_open_file_menu)
        self.menu_options['file_save'].connect("activate", self.pre_process_page.on_save_file_menu)
        self.menu_options['edit_registers'].connect("activate", self.pre_process_page.on_edit_registers)
        self.menu_options['edit_undo'].connect("activate", self.pre_process_page.preprocess_manager.undo,
                                               self.pre_process_page, self.menu_options['edit_undo'])
        self.notebook.connect("switch-page", self.switch_page)

    def switch_page(self, notebook, page, page_num):
        try:
            page.emit('page-selected')
        except Exception:
            return

    def create_notebook(self):
        self.notebook = Gtk.Notebook()
        self.layout.pack_start(self.notebook, True, True, 0)

    def create_pre_process_page(self):
        self.pre_process_page = PreprocessTab(self)
        self.pre_process_page.set_border_width(10)
        self.notebook.append_page(self.pre_process_page, Gtk.Label("Pre-process"))

    def create_analysis_page(self):
        self.analysis_page = AnalysisTab(self)
        self.analysis_page.set_border_width(10)
        self.notebook.append_page(self.analysis_page, Gtk.Label("Analysis"))

    def create_menu_bar(self):
        file_items = [('file_open','Open File', True),
                      ('file_save', 'Save File', False),
                      None,
                      ('file_exit', 'Exit', True)]

        edit_items = [('edit_registers', 'Edit registers', False),
                      None,
                      ('edit_undo', 'Undo', False)]

        file_menu = self.create_menu_item('file_menu', 'File', file_items)
        edit_menu = self.create_menu_item('edit_menu', 'Edit', edit_items)

        self.menu_bar = Gtk.MenuBar()
        self.menu_bar.set_border_width(3)
        self.menu_bar.append(file_menu)
        self.menu_bar.append(edit_menu)

        self.layout.pack_start(self.menu_bar, False, False, 0)

    def create_menu_item(self, menu_name, display_name, items = []):
        if menu_name in self.menus:
            return False

        self.menus[menu_name] = Gtk.MenuItem(display_name)
        file_menu = Gtk.Menu()
        self.menus[menu_name].set_submenu(file_menu)

        for i in items:
            if not i:
                file_menu.append(Gtk.SeparatorMenuItem())
                continue

            if not i[0] in self.menu_options:
                self.menu_options[i[0]] = Gtk.MenuItem(i[1])
                self.menu_options[i[0]].set_sensitive(i[2])
                file_menu.append(self.menu_options[i[0]])

        return self.menus[menu_name]

    def on_exit_file_menu(self, widget):
        self.destroy()
        Gtk.main_quit()

    def enable_save_edit_file(self, *args):
        self.menu_options['file_save'].set_sensitive(True)
        self.menu_options['edit_registers'].set_sensitive(True)

    def on_registers_edited(self, *args):
        self.menu_options['edit_undo'].set_sensitive(True)