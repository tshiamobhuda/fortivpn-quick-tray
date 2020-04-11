import gi, signal

gi.require_version('Gtk', '3.0')
gi.require_version("AppIndicator3", "0.1")

from gi.repository import Gtk, AppIndicator3
from os import path

APP_NAME = 'FortiVPN-Quick-Tray'

def main():

    img_dir = path.dirname(path.realpath(__file__)) + '/icons'
    indicator = AppIndicator3.Indicator.new(APP_NAME, img_dir + '/off.png', AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

    menu = Gtk.Menu()

    stop = Gtk.MenuItem('exit')
    stop.connect('activate', Gtk.main_quit)

    menu.append(stop)
    menu.show_all()

    indicator.set_menu(menu)

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()


if __name__ == "__main__":
    main()