import gi

from vistas.MainWindow import MainWindow

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

window = MainWindow()
window.show_all()
Gtk.main()
