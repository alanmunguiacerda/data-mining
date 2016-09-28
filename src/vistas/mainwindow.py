import gi
import os

from negocios.PreprocessManager import PreprocessManager
from vistas.DomainPopup import DomainPopup
from vistas.modifyfiledialog import ModifyFileDialog

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject


# MainWindow inherits from Gtk.Window
class MainWindow (Gtk.Window):

    # MainWindow class constructor
    def __init__(self):
        GObject.signal_new('file-path-ready', self, GObject.SIGNAL_RUN_LAST, GObject.TYPE_PYOBJECT,
                           (GObject.TYPE_PYOBJECT,))

        GObject.signal_new('reg-exp-ready', self, GObject.SIGNAL_RUN_LAST, GObject.TYPE_PYOBJECT,
                           (GObject.TYPE_PYOBJECT,  GObject.TYPE_PYOBJECT,))

        GObject.signal_new('attribute-to-remove', self, GObject.SIGNAL_RUN_LAST, GObject.TYPE_PYOBJECT,
                           (GObject.TYPE_PYOBJECT, ))
        GObject.signal_new('refresh-all', self, GObject.SIGNAL_RUN_LAST, GObject.TYPE_PYOBJECT,
                           (GObject.TYPE_PYOBJECT, ))
        Gtk.Window.__init__(self, title="Lil Jarvis")

        # Csv
        self.preprocess_manager = PreprocessManager()

        # Main window style properties
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
        #    Edit drop down items
        self.edit_registers = Gtk.MenuItem("Edit Registers")
        self.edit_undo = Gtk.MenuItem("Undo")
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
        self.attributes_remove_button = Gtk.Button("Remove")
        self.regexp_button = Gtk.Button("Domain")
        self.attributes_tree_view = Gtk.TreeView()
        self.disable_remove_domain_button()
        #    Selected attribute group widgets
        self.selected_attribute_statistics_name_label = Gtk.Label()
        self.selected_attribute_statistics_missing_label = Gtk.Label()
        self.selected_attribute_statistics_distinct_label = Gtk.Label()
        self.selected_attribute_statistics_type_label = Gtk.Label()
        self.selected_attribute_statistics_unique_label = Gtk.Label()
        self.selected_attribute_view = Gtk.TreeView()
        #    Class attribute group widget
        self.attributes_combo_box = Gtk.ComboBoxText()
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
        self.select_button.connect("clicked", self.on_open_file_menu)
        self.open_button.connect("clicked", self.on_open_file_clicked)
        self.file_open.connect("activate", self.on_open_file_menu)

        # Save file connections
        self.file_save.connect("activate", self.on_save_file_menu)

        # Send the filename to the csv manager
        self.connect("file-path-ready", self.preprocess_manager.clean_attributes_widgets, self.attributes_tree_view,
                     self.attributes_combo_box, self.selected_attribute_view,
                     self.selected_attribute_statistics_name_label, self.selected_attribute_statistics_missing_label,
                     self.selected_attribute_statistics_distinct_label, self.selected_attribute_statistics_type_label,
                     self.selected_attribute_statistics_unique_label)
        self.connect("file-path-ready", self.enable_save_edit_file)
        self.connect("file-path-ready", self.preprocess_manager.set_file)
        self.connect("file-path-ready", self.preprocess_manager.load_combo_box_attributes, self.attributes_combo_box)
        self.connect("file-path-ready", self.preprocess_manager.load_attributes_tree_view, self.attributes_tree_view)
        self.connect("file-path-ready", self.preprocess_manager.set_file_info,
                     self.file_info_name_label, self.file_info_name_attributes,
                     self.file_info_name_instances, self.file_info_name_weights)

        # Draw shit in the screen
        self.attributes_tree_view.connect("cursor-changed", self.preprocess_manager.set_data_in_table,
                                          self.selected_attribute_view)
        self.attributes_tree_view.connect("cursor-changed", self.preprocess_manager.set_attribute_info,
                                          self.selected_attribute_statistics_name_label,
                                          self.selected_attribute_statistics_missing_label,
                                          self.selected_attribute_statistics_distinct_label,
                                          self.selected_attribute_statistics_type_label,
                                          self.selected_attribute_statistics_unique_label)

        # Enable/Disable buttons
        self.attributes_tree_view.connect("cursor-changed", self.enable_remove_domain_button)
        self.connect("file-path-ready", self.disable_remove_domain_button)

        # Remove attribute connection
        self.attributes_remove_button.connect("clicked", self.on_remove_attribute_clicked, )

        # Connection to open the domain popup
        self.regexp_button.connect("clicked", self.on_regexp_clicked)

        # Connection to define attribute's domain
        self.connect('reg-exp-ready', self.preprocess_manager.set_attribute_domain)

        # Remove attribute
        self.connect("attribute-to-remove", self.preprocess_manager.remove_attribute)
        self.connect("refresh-all", self.preprocess_manager.clean_attributes_widgets, self.attributes_tree_view,
                     self.attributes_combo_box, self.selected_attribute_view,
                     self.selected_attribute_statistics_name_label, self.selected_attribute_statistics_missing_label,
                     self.selected_attribute_statistics_distinct_label, self.selected_attribute_statistics_type_label,
                     self.selected_attribute_statistics_unique_label)
        self.connect("refresh-all", self.preprocess_manager.load_combo_box_attributes,
                     self.attributes_combo_box)
        self.connect("refresh-all", self.preprocess_manager.load_attributes_tree_view,
                     self.attributes_tree_view)
        self.connect("refresh-all", self.preprocess_manager.set_file_info,
                     self.file_info_name_label, self.file_info_name_attributes,
                     self.file_info_name_instances, self.file_info_name_weights)
        # Connection to close program
        self.file_exit.connect("activate", self.on_exit_file_menu)

        # Connection to edit registers
        self.edit_registers.connect("activate", self.on_edit_registers_menu)

        # Connection to undo
        self.edit_undo.connect("activate", self.preprocess_manager.undo, self)

    def create_menu_bar(self):
        # File menu
        file_menu = Gtk.Menu()
        file_menu_drop_down = Gtk.MenuItem("File")
        # File menu items
        self.file_save.set_sensitive(False)
        file_menu_drop_down.set_submenu(file_menu)
        file_menu.append(self.file_open)
        file_menu.append(self.file_save)
        file_menu.append(Gtk.SeparatorMenuItem())
        file_menu.append(self.file_exit)

        self.menu_bar.append(file_menu_drop_down)

        # Edit menu
        edit_menu = Gtk.Menu()
        edit_menu_drop_down = Gtk.MenuItem("Edit")
        # File menu items
        self.edit_registers.set_sensitive(False)
        edit_menu_drop_down.set_submenu(edit_menu)
        edit_menu.append(self.edit_registers)
        edit_menu.append(self.edit_undo)

        self.menu_bar.append(edit_menu_drop_down)

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

        self.notebook.append_page(self.classify_page, Gtk.Label("Classify"))

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
        file_info_grid.attach(Gtk.Label("Weights: "), 0, 1, 1, 1)
        file_info_grid.attach(Gtk.Label("Instances: "), 2, 1, 1, 1)
        file_info_grid.attach(Gtk.Label("Attributes: "), 4, 1, 1, 1)

        self.file_info_name_label.set_halign(Gtk.Align.START)
        self.file_info_name_instances.set_halign(Gtk.Align.START)
        self.file_info_name_attributes.set_halign(Gtk.Align.START)
        self.file_info_name_weights.set_halign(Gtk.Align.START)

        file_info_grid.attach(self.file_info_name_label, 1, 0, 2, 1)
        file_info_grid.attach(self.file_info_name_weights, 1, 1, 1, 1)
        file_info_grid.attach(self.file_info_name_instances, 3, 1, 1, 1)
        file_info_grid.attach(self.file_info_name_attributes, 5, 1, 1, 1)

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

        self.attributes_remove_button.set_border_width(5)
        attributes_button_box.pack_start(self.attributes_remove_button, False, False, 0)

        self.regexp_button.set_border_width(5)
        attributes_button_box.pack_start(self.regexp_button, False, False, 0)

        attributes_box.pack_start(attributes_button_box, False, False, 0)

        # Attributes tree view
        self.attributes_tree_view.set_border_width(5)
        self.attributes_tree_view.set_vexpand(True)

        attributes_scroll_tree = Gtk.ScrolledWindow()
        attributes_scroll_tree.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        attributes_scroll_tree.add(self.attributes_tree_view)

        attributes_box.pack_start(attributes_scroll_tree, True, True, 0)

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

        selected_attribute_statistics_labels_grid.attach(self.selected_attribute_statistics_name_label, 1, 0, 2, 1)
        selected_attribute_statistics_labels_grid.attach(self.selected_attribute_statistics_missing_label, 1, 1, 1, 1)

        selected_attribute_statistics_labels_grid.attach(self.selected_attribute_statistics_distinct_label, 3, 1, 1, 1)

        selected_attribute_statistics_labels_grid.attach(self.selected_attribute_statistics_type_label, 5, 0, 1, 1)
        selected_attribute_statistics_labels_grid.attach(self.selected_attribute_statistics_unique_label, 5, 1, 1, 1)

        self.selected_attribute_statistics_name_label.set_halign(Gtk.Align.START)
        self.selected_attribute_statistics_missing_label.set_halign(Gtk.Align.START)
        self.selected_attribute_statistics_distinct_label.set_halign(Gtk.Align.START)
        self.selected_attribute_statistics_type_label.set_halign(Gtk.Align.START)
        self.selected_attribute_statistics_unique_label.set_halign(Gtk.Align.START)

        selected_attribute_box.pack_start(selected_attribute_statistics_labels_grid, False, False, 0)

        # Statistics tree view
        self.selected_attribute_view.set_border_width(5)
        self.selected_attribute_view.set_vexpand(True)

        scrollTree = Gtk.ScrolledWindow()
        scrollTree.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrollTree.add(self.selected_attribute_view)

        selected_attribute_box.pack_start(scrollTree, True, True, 0)

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
        status_box.set_border_width(10)
        status_frame.add(status_box)

        self.status_label.set_markup("<b><big>Lil Jarvis salutes you :D</big></b>")
        self.status_label.set_hexpand(True)
        self.status_label.set_halign(Gtk.Align.START)
        status_box.pack_start(self.status_label, True, True, 0)

        self.status_log_button.set_border_width(5)
        status_box.pack_start(self.status_log_button, False, False, 0)

        page_layout.attach(status_frame, 0, 4, 2, 1)

        self.pre_process_page.pack_start(page_layout, True, True, 0)

    def send_error_dialog(self, title, message):
        dialog = Gtk.Dialog(title, self, 0,
                            (Gtk.STOCK_OK, Gtk.ResponseType.OK))

        dialog.set_default_size(200, 75)
        box = dialog.get_content_area()
        box.add(Gtk.Label(message))
        box.show_all()
        dialog.run()
        dialog.destroy()

    def on_open_file_clicked(self, widget):
        string = self.text_box.get_text()

        if string and string.strip() and string.endswith('.csv'):
            if os.path.isfile(string):
                self.emit('file-path-ready', self.text_box.get_text())
            else:
                self.send_error_dialog("Error", "File not found")

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
            if type(widget).__name__ == 'MenuItem':
                self.on_open_file_clicked(widget)

        dialog.destroy()

    def on_save_file_menu(self, widget):
        dialog = Gtk.FileChooserDialog("Save file as: ", self,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.preprocess_manager.save_file(dialog.get_filename())

        dialog.destroy()

    def on_exit_file_menu(self, widget):
        self.destroy()
        Gtk.main_quit()

    def on_edit_registers_menu(self, widget):
        dialog = ModifyFileDialog(self)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            dialog.commit()
            self.preprocess_manager.set_file_info(None, self.file_info_name_label, self.file_info_name_attributes,
                     self.file_info_name_instances, self.file_info_name_weights)

        dialog.destroy()

    def on_remove_attribute_clicked(self, widget):
        model, row = self.attributes_tree_view.get_selection().get_selected()
        if not row:
            return
        attribute_name = model[row][1]
        self.emit('attribute-to-remove', attribute_name)
        self.emit('refresh-all', "DummyText")

    def on_regexp_clicked(self, widget):
        model, row = self.attributes_tree_view.get_selection().get_selected()
        if not row:
            return
        attribute_name = model[row][1]

        dialog = DomainPopup(self, attribute_name)

        response = dialog.run()

        if response == Gtk.ResponseType.OK and attribute_name:
            self.emit('reg-exp-ready', dialog.get_regexp(), attribute_name)

        dialog.destroy()

    def enable_remove_domain_button(self, *args):
        self.attributes_remove_button.set_sensitive(True)
        self.regexp_button.set_sensitive(True)

    def disable_remove_domain_button(self, *args):
        self.attributes_remove_button.set_sensitive(False)
        self.regexp_button.set_sensitive(False)

    def enable_save_edit_file(self, *args):
        self.file_save.set_sensitive(True)
        self.edit_registers.set_sensitive(True)

