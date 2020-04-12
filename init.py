import gi, signal

gi.require_version('Gtk', '3.0')
gi.require_version("AppIndicator3", "0.1")

from gi.repository import Gtk, AppIndicator3
from os import path
from menu_items import MenuBuilder
from vpn_config import IMG_DIR

APP_NAME = 'FortiVPN-Quick-Tray'


if __name__ == "__main__":
    indicator = AppIndicator3.Indicator.new(APP_NAME, IMG_DIR + '/off.png', AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    
    builder = MenuBuilder(Gtk, indicator)
    indicator.set_menu(builder.build_menu())
    
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()