import gi
import sys

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

        float_info = sys.float_info
        adjustment_1 = Gtk.Adjustment(0, -float_info.max, float_info.max, 1, 0, 0)
        adjustment_2 = Gtk.Adjustment(0, -float_info.max, float_info.max, 1, 0, 0)
        adjustment_3 = Gtk.Adjustment(0, -float_info.max, float_info.max, 1, 0, 0)
        adjustment_4 = Gtk.Adjustment(0, -float_info.max, float_info.max, 1, 0, 0)

        dialog_box.add(Gtk.Label("Old min: "))
        self.old_min = Gtk.SpinButton()
        self.old_min.configure(adjustment_1, 0, float_info.dig)
        dialog_box.add(self.old_min)

        dialog_box.add(Gtk.Label("Old max: "))
        self.old_max = Gtk.SpinButton()
        self.old_max.configure(adjustment_2, 0, float_info.dig)
        dialog_box.add(self.old_max)

        dialog_box.add(Gtk.Label("New min: "))
        self.new_min = Gtk.SpinButton()
        self.new_min.configure(adjustment_3, 0, float_info.dig)
        dialog_box.add(self.new_min)

        dialog_box.add(Gtk.Label("New max: "))
        self.new_max = Gtk.SpinButton()
        self.new_max.configure(adjustment_4, 0, float_info.dig)
        dialog_box.add(self.new_max)

        area.add(dialog_box)
        self.show_all()

    def get_data(self):
        return {
            'old_min': self.old_min.get_value(),
            'old_max': self.old_max.get_value(),
            'new_min': self.new_min.get_value(),
            'new_max': self.new_max.get_value()
        }

