import gi, signal

gi.require_version('Gtk', '3.0')
gi.require_version("AppIndicator3", "0.1")

from gi.repository import Gtk, AppIndicator3
from os import path

APP_NAME = 'FortiVPN-Quick-Tray'
IMG_DIR = path.dirname(path.realpath(__file__)) + '/icons'

def build_menu():
    menu = Gtk.Menu()

    connect_vpn = Gtk.MenuItem('connect')
    connect_vpn.connect('activate', action_connect_vpn)

    disconnect_vpn = Gtk.MenuItem('disconnect')
    disconnect_vpn.connect('activate', action_disconnect_vpn)

    configure_vpn = Gtk.MenuItem('config')
    configure_vpn.connect('activate', action_configure_vpn)

    show_vpn_logs = Gtk.MenuItem('logs')
    show_vpn_logs.connect('activate', action_show_vpn_logs)

    close = Gtk.MenuItem('exit')
    close.connect('activate', Gtk.main_quit)

    menu.append(connect_vpn)
    menu.append(disconnect_vpn)
    menu.append(Gtk.SeparatorMenuItem.new())
    menu.append(configure_vpn)
    menu.append(show_vpn_logs)
    menu.append(Gtk.SeparatorMenuItem.new())
    menu.append(close)

    menu.show_all()
    
    return menu

def action_connect_vpn(object):
    indicator.set_icon(IMG_DIR + '/on.png')

def action_disconnect_vpn(object):
    indicator.set_icon(IMG_DIR + '/off.png')

def action_configure_vpn(object):
    pass

def action_show_vpn_logs(object):
    pass

if __name__ == "__main__":
    indicator = AppIndicator3.Indicator.new(APP_NAME, IMG_DIR + '/off.png', AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()