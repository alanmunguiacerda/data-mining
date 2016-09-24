import gi

from vistas.mainwindow import MainWindow

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

window = MainWindow()
window.show_all()
Gtk.main()
