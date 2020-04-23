import gi
import signal

gi.require_version('Gtk', '3.0')
gi.require_version("AppIndicator3", "0.1")

from gi.repository import Gtk, AppIndicator3
from menu_items import MenuBuilder
from os import path

if __name__ == "__main__":
    indicator = AppIndicator3.Indicator.new_with_path(
        'FortiVPN-Quick-Tray',

if __name__ == "__main__":
    indicator = AppIndicator3.Indicator.new_with_path(
        APP_NAME,
        'off',
        AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
        path.dirname(path.realpath(__file__)) + '/icons'
    )

    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    indicator.set_label('FortiVPN OFF', 'FortiVPN OFF')

    builder = MenuBuilder(Gtk, indicator, AppIndicator3)
    indicator.set_menu(builder.build_menu())

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()
