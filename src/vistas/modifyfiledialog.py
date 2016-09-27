import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from src import constants

class ModifyFileDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Modify registers", parent, Gtk.DialogFlags.MODAL,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.parent = parent
        self.set_default_size(500, 400)
        self.set_border_width(10)

        # Content area (area above buttons)
        area = self.get_content_area()

        button_box = Gtk.Box()
        button_box.set_border_width(5)
        button_box.set_spacing(10)
        button_box.set_homogeneous(True)

        self.add_button = Gtk.Button(" + Add")
        self.remove_button = Gtk.Button(" - Remove")
        self.remove_button.set_sensitive(False)

        button_box.pack_start(self.add_button, False, False, 0)
        button_box.pack_start(self.remove_button, False, False, 0)

        area.add(button_box)

        self.file_tree_view = Gtk.TreeView()
        self.file_tree_view.set_vexpand(True)

        scroll_tree = Gtk.ScrolledWindow()
        scroll_tree.set_border_width(5)
        scroll_tree.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll_tree.add(self.file_tree_view)

        area.add(scroll_tree)

        self.set_treeview_data()

        self.create_connections()

        self.show_all()

    def set_treeview_data(self):
        self.parent.preprocess_manager.set_file_in_table(self.file_tree_view, self.modify_cell)

    def create_connections(self):
        self.file_tree_view.connect("cursor-changed", self.enable_remove_button)
        self.remove_button.connect("clicked", self.delete_row)
        self.add_button.connect("clicked", self.add_row)

    def enable_remove_button(self, *args):
        model, row = self.file_tree_view.get_selection().get_selected()
        if row:
            self.remove_button.set_sensitive(True)

    def delete_row(self, *args):
        model, row = self.file_tree_view.get_selection().get_selected()
        if row:
            model.set_value(row, 0, "Del")
            self.remove_button.set_sensitive(True)

    def add_row(self, widget):
        model = self.file_tree_view.get_model()
        aux_list = []
        for i,_ in enumerate(self.file_tree_view.get_columns()):
            aux_list.append("Add" if i is 0 else constants.MISSING_DATA_SYMBOL)

        model.append(aux_list)

    def modify_cell(self, widget, row_un, change, column):
        model, row = self.file_tree_view.get_selection().get_selected()
        if row:
            model.set_value(row, column, change)

            if model.get_value(row, 0) == "Add":
                return

            model.set_value(row, 0, "Mod")

    def commit(self):
        add_rows = []
        modify_rows = {}
        delete_rows = []
        for i, row in enumerate(self.file_tree_view.get_model()):
            if row[0] == 'Add':
                add_rows.append([cell for cell in row[1:]])
            elif row[0] == 'Mod':
                modify_rows[i] = [cell for cell in row[1:]]
            elif row[0] == 'Del':
                delete_rows.append(i)

        self.parent.preprocess_manager.add_rows(add_rows)
        self.parent.preprocess_manager.modify_rows(modify_rows)
        self.parent.preprocess_manager.delete_rows(delete_rows)