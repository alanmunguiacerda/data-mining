import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class DomainPopup(Gtk.Dialog):

    def __init__(self, parent, attribute_name):
        Gtk.Dialog.__init__(self, "Define regular expression", parent, Gtk.DialogFlags.MODAL,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(200, 100)
        self.set_border_width(10)
        self.set_resizable(False)

        # Content area (area above buttons)
        area = self.get_content_area()

        dialog_box = Gtk.Box()
        dialog_box.set_orientation(Gtk.Orientation.VERTICAL)
        dialog_box.set_border_width(10)
        dialog_box.set_spacing(5)

        dialog_box.add(Gtk.Label("Regular expression: "))
        self.text_box = Gtk.Entry()

        self.text_box.set_text(parent.preprocess_manager.csv.get_domain(attribute_name))
        
        dialog_box.add(self.text_box)

        area.add(dialog_box)
        self.show_all()

    def get_regexp(self):
        return self.text_box.get_text()

