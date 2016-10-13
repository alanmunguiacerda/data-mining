import gi

from vistas.mainwindow import MainWindow
from vistas.MainWindow2 import MainWindow2

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

window = MainWindow2()
window.show_all()
Gtk.main()
