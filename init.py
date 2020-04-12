import gi, signal

gi.require_version('Gtk', '3.0')
gi.require_version("AppIndicator3", "0.1")

from gi.repository import Gtk, AppIndicator3
from os import path
from menu_items import CloseMenuItem, ConnectMenuItem, DisconnectMenuItem, ConfigMenuItem, LogsMenuItem

APP_NAME = 'FortiVPN-Quick-Tray'
IMG_DIR = path.dirname(path.realpath(__file__)) + '/icons'
indicator = AppIndicator3.Indicator.new(APP_NAME, IMG_DIR + '/off.png', AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)

def build_menu():
    menu = Gtk.Menu()

    menu.append(ConnectMenuItem(Gtk, indicator, IMG_DIR).get_menu_item())
    menu.append(DisconnectMenuItem(Gtk, indicator, IMG_DIR).get_menu_item())
    menu.append(Gtk.SeparatorMenuItem.new())
    menu.append(ConfigMenuItem(Gtk).get_menu_item())
    menu.append(LogsMenuItem(Gtk).get_menu_item())
    menu.append(Gtk.SeparatorMenuItem.new())
    menu.append(CloseMenuItem(Gtk).get_menu_item())

    menu.show_all()
    
    return menu

if __name__ == "__main__":
    indicator = AppIndicator3.Indicator.new(APP_NAME, IMG_DIR + '/off.png', AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()