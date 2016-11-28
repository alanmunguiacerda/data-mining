import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ErrorDialog(Gtk.Dialog):

    def __init__(self, title, message, parent):
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL,
                            (Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(200, 75)
        self.set_border_width(10)
        self.set_resizable(False)

        box = self.get_content_area()
        box.add(Gtk.Label(message))
        box.show_all()
        self.run()
        self.destroy()
