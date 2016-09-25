import gi
import re
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject


# MainWindow inherits from Gtk.Window
class MainWindow (Gtk.Window):

    # MainWindow class constructor
    def __init__(self):
        GObject.signal_new('file-path-ready', self, GObject.SIGNAL_RUN_LAST, GObject.TYPE_PYOBJECT,
                           (GObject.TYPE_PYOBJECT,))

        Gtk.Window.__init__(self, title="Lil Jarvis")

        self.set_border_width(10)
        self.set_default_size(800, 600)

        # Main layout
        self.layout = Gtk.Box()
        self.layout.set_orientation(Gtk.Orientation.VERTICAL)
        self.add(self.layout)

        # Note book
        self.notebook = Gtk.Notebook()
        # Notebook pages
        self.classify_page = Gtk.Box()
        self.pre_process_page = Gtk.Box()

        # Menu bar
        self.menu_bar = Gtk.MenuBar()
        self.menu_bar.set_border_width(3)

        # Variable instantiation
        #    File drop down items
        self.file_open = Gtk.MenuItem("Open")
        self.file_save = Gtk.MenuItem("Save")
        self.file_exit = Gtk.MenuItem("Exit")
        #    Open file widgets
        self.text_box = Gtk.Entry()
        self.select_button = Gtk.Button("Select")
        self.open_button = Gtk.Button("Open")
        #    File info group widgets
        self.file_info_name_label = Gtk.Label()
        self.file_info_name_instances = Gtk.Label()
        self.file_info_name_attributes = Gtk.Label()
        self.file_info_name_weights = Gtk.Label()
        #    Attributes group widgets
        self.mark_all_button = Gtk.Button("Mark all")
        self.none_button = Gtk.Button("None")
        self.invert_button = Gtk.Button("Invert")
        self.regexp_button = Gtk.Button("Domain")
        self.attributes_tree_view = Gtk.TreeView()
        self.attributes_remove_button = Gtk.Button("Remove")
        #    Selected attribute group widgets
        self.selected_attribute_statistics_name_label = Gtk.Label()
        self.selected_attribute_statistics_missing_label = Gtk.Label()
        self.selected_attribute_statistics_distinct_label = Gtk.Label()
        self.selected_attribute_statistics_type_label = Gtk.Label()
        self.selected_attribute_statistics_unique_label = Gtk.Label()
        self.selected_attribute_view = Gtk.TreeView()
        #    Class attribute group widget
        self.attributes_combo_box = Gtk.ComboBox()
        #    Status group widgets
        self.status_label = Gtk.Label()
        self.status_log_button = Gtk.Button("See log")

        # Control variables
        self.file_route = ""

        # Interface creation
        self.create_menu_bar()
        self.create_notebook()

        # Create connections (signal-slot)
        self.connections()

    def connections(self):
        self.connect("delete-event", Gtk.main_quit)
        # Open File connections
        self.select_button.connect("clicked", self.on_select_file_clicked)
        self.open_button.connect("clicked", self.on_open_file_clicked)
        self.file_open.connect("activate", self.on_open_file_menu)
        self.connect("file-path-ready", self.prueba)

    def create_menu_bar(self):
        # File menu
        file_menu = Gtk.Menu()
        file_menu_drop_down = Gtk.MenuItem("File")
        # File menu items

        file_menu_drop_down.set_submenu(file_menu)
        file_menu.append(self.file_open)
        file_menu.append(self.file_save)
        file_menu.append(Gtk.SeparatorMenuItem())
        file_menu.append(self.file_exit)

        self.menu_bar.append(file_menu_drop_down)

        self.layout.pack_start(self.menu_bar, False, False, 0)

    def create_notebook(self):
        # Notebook
        self.layout.pack_start(self.notebook, True, True, 0)

        # Page 1
        self.pre_process_page.set_border_width(10)

        self.notebook.append_page(self.pre_process_page, Gtk.Label("Pre-process"))
        self.create_pre_process_page()

        # Page 2
        self.classify_page.set_border_width(10)

        self.notebook.append_page(self.classify_page, Gtk.Label("Clasify"))

    def create_pre_process_page(self):
        page_layout = Gtk.Grid()
        page_layout.set_column_homogeneous(True)
        page_layout.set_row_spacing(10)
        page_layout.set_column_spacing(10)

        # Open File group
        open_file_box = Gtk.Box()
        open_file_box.set_spacing(5)

        open_file_box.pack_start(Gtk.Label("File: "), False, False, 0)

        self.text_box.set_hexpand(True)
        open_file_box.pack_start(self.text_box, True, True, 0)

        open_file_box.pack_start(self.select_button, False, False, 0)

        open_file_box.pack_start(self.open_button, False, False, 0)

        page_layout.attach(open_file_box, 0, 0, 2, 1)

        # File info group*************************************************************************************
        file_info_frame = Gtk.Frame()
        file_info_frame.set_label("Current Data base")
        
        file_info_grid = Gtk.Grid()
        file_info_grid.set_column_homogeneous(True)
        file_info_frame.add(file_info_grid)

        file_info_grid.attach(Gtk.Label("Name: "), 0, 0, 1, 1)
        file_info_grid.attach(Gtk.Label("Instances: "), 0, 1, 1, 1)

        file_info_grid.attach(Gtk.Label("Attributes: "), 2, 0, 1, 1)
        file_info_grid.attach(Gtk.Label("Weights: "), 2, 1, 1, 1)

        file_info_grid.attach(self.file_info_name_label, 1, 0, 1, 1)
        file_info_grid.attach(self.file_info_name_instances, 1, 1, 1, 1)

        file_info_grid.attach(self.file_info_name_attributes, 3, 0, 1, 1)
        file_info_grid.attach(self.file_info_name_weights, 3, 1, 1, 1)

        page_layout.attach(file_info_frame, 0, 1, 1, 1)

        # Attributes Group***********************************************************************************
        attributes_frame = Gtk.Frame()
        attributes_frame.set_label("Attributes")

        attributes_box = Gtk.Box()
        attributes_box.set_orientation(Gtk.Orientation.VERTICAL)

        attributes_frame.add(attributes_box)
        # Attributes buttons
        attributes_button_box = Gtk.Box()
        attributes_button_box.set_spacing(10)
        attributes_button_box.set_homogeneous(True)

        self.mark_all_button.set_border_width(5)
        attributes_button_box.pack_start(self.mark_all_button, False, False, 0)

        self.none_button.set_border_width(5)
        attributes_button_box.pack_start(self.none_button, False, False, 0)

        self.invert_button.set_border_width(5)
        attributes_button_box.pack_start(self.invert_button, False, False, 0)

        self.regexp_button.set_border_width(5)
        attributes_button_box.pack_start(self.regexp_button, False, False, 0)

        attributes_box.pack_start(attributes_button_box, False, False, 0)

        # Attributes tree view
        self.attributes_tree_view.set_border_width(5)
        self.attributes_tree_view.set_vexpand(True)
        attributes_box.pack_start(self.attributes_tree_view, True, True, 0)

        # Remove attribute button
        self.attributes_remove_button.set_border_width(5)
        attributes_box.pack_start(self.attributes_remove_button, False, False, 0)

        page_layout.attach(attributes_frame, 0, 2, 1, 2)

        # Selected attribute group***************************************************************************
        selected_attribute_frame = Gtk.Frame()
        selected_attribute_frame.set_label("Selected attribute")

        selected_attribute_box = Gtk.Box()
        selected_attribute_box.set_orientation(Gtk.Orientation.VERTICAL)
        selected_attribute_frame.add(selected_attribute_box)

        # Attribute statistics
        selected_attribute_statistics_labels_grid = Gtk.Grid()
        selected_attribute_statistics_labels_grid.set_column_homogeneous(True)

        selected_attribute_statistics_labels_grid.attach(Gtk.Label("Name: "), 0, 0, 1, 1)
        selected_attribute_statistics_labels_grid.attach(Gtk.Label("Missing: "), 0, 1, 1, 1)

        selected_attribute_statistics_labels_grid.attach(Gtk.Label("Distinct: "), 2, 1, 1, 1)

        selected_attribute_statistics_labels_grid.attach(Gtk.Label("Type: "), 4, 0, 1, 1)
        selected_attribute_statistics_labels_grid.attach(Gtk.Label("Unique: "), 4, 1, 1, 1)

        selected_attribute_statistics_labels_grid.attach(self.selected_attribute_statistics_name_label, 1, 0, 1, 1)
        selected_attribute_statistics_labels_grid.attach(self.selected_attribute_statistics_missing_label, 1, 1, 1, 1)

        selected_attribute_statistics_labels_grid.attach(self.selected_attribute_statistics_distinct_label, 3, 1, 1, 1)

        selected_attribute_statistics_labels_grid.attach(self.selected_attribute_statistics_type_label, 5, 0, 1, 1)
        selected_attribute_statistics_labels_grid.attach(self.selected_attribute_statistics_unique_label, 5, 1, 1, 1)

        selected_attribute_box.pack_start(selected_attribute_statistics_labels_grid, False, False, 0)

        # Statistics tree view
        self.selected_attribute_view.set_border_width(5)
        self.selected_attribute_view.set_vexpand(True)
        selected_attribute_box.pack_start(self.selected_attribute_view, True, True, 0)

        page_layout.attach(selected_attribute_frame, 1, 2, 1, 2)

        # Select Class attribute group***********************************************************************
        class_attribute_frame = Gtk.Frame()
        class_attribute_frame.set_label("Class attribute")

        self.attributes_combo_box.set_border_width(5)
        class_attribute_frame.add(self.attributes_combo_box)

        page_layout.attach(class_attribute_frame, 1, 1, 1, 1)

        # Status Group **************************************************************************************
        status_frame = Gtk.Frame()
        status_frame.set_label("Status")

        status_box = Gtk.Box()
        status_box.set_orientation(Gtk.Orientation.HORIZONTAL)
        status_frame.add(status_box)

        self.status_label.set_markup("<b><big>Lil Jarvis salutes you :D</big></b>")
        self.status_label.set_hexpand(True)
        self.status_label.set_justify(Gtk.Justification.LEFT)
        status_box.pack_start(self.status_label, True, True, 0)

        self.status_log_button.set_border_width(5)
        status_box.pack_start(self.status_log_button, False, False, 0)

        page_layout.attach(status_frame, 0, 4, 2, 1)

        self.pre_process_page.pack_start(page_layout, True, True, 0)

    def on_select_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Select a file: ", self, Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        filter = Gtk.FileFilter()
        filter.add_pattern("*.csv")
        dialog.set_filter(filter)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.text_box.set_text(dialog.get_filename())

        dialog.destroy()

    def on_open_file_clicked(self, widget):
        string = self.text_box.get_text()

        if string and string.strip() and string.endswith('.csv'):
            self.emit('file-path-ready', self.text_box.get_text())

    def on_open_file_menu(self, widget):
        dialog = Gtk.FileChooserDialog("Select a file: ", self, Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        filter = Gtk.FileFilter()
        filter.add_pattern("*.csv")
        dialog.set_filter(filter)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.text_box.set_text(dialog.get_filename())
            self.emit('file-path-ready', self.text_box.get_text())

        dialog.destroy()

    def prueba(self, *args):
        print(args[1])

