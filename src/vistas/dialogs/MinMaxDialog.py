import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class MinMaxDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Define parameters", None, Gtk.DialogFlags.MODAL,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(200, 400)
        self.set_border_width(10)
        self.set_resizable(False)

        # Content area (area above buttons)
        area = self.get_content_area()

        dialog_box = Gtk.Box()
        dialog_box.set_orientation(Gtk.Orientation.VERTICAL)
        dialog_box.set_border_width(10)
        dialog_box.set_spacing(5)

        dialog_box.add(Gtk.Label("Old min: "))
        self.old_min = Gtk.Entry()
        dialog_box.add(self.old_min)

        dialog_box.add(Gtk.Label("Old max: "))
        self.old_max = Gtk.Entry()
        dialog_box.add(self.old_max)

        dialog_box.add(Gtk.Label("New min: "))
        self.new_min = Gtk.Entry()
        dialog_box.add(self.new_min)

        dialog_box.add(Gtk.Label("New max: "))
        self.new_max = Gtk.Entry()
        dialog_box.add(self.new_max)

        area.add(dialog_box)
        self.show_all()

    def get_data(self):
        return {
            'old_min': self.old_min.get_text(),
            'old_max': self.old_max.get_text(),
            'new_min': self.new_min.get_text(),
            'new_max': self.new_max.get_text()
        }

