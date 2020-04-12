import gi, signal

gi.require_version('Gtk', '3.0')
gi.require_version("AppIndicator3", "0.1")

from gi.repository import Gtk, AppIndicator3
from os import path

APP_NAME = 'FortiVPN-Quick-Tray'
IMG_DIR = path.dirname(path.realpath(__file__)) + '/icons'

VPN_ON = False
VPN_CONFIG = '/etc/openfortivpn/Kosmosdal'

def build_menu():
    menu = Gtk.Menu()

    menu.append(build_menu_item('connect', action_connect_vpn))
    menu.append(build_menu_item('disconnect', action_disconnect_vpn))
    menu.append(Gtk.SeparatorMenuItem.new())
    menu.append(build_menu_item('config', action_configure_vpn))
    menu.append(build_menu_item('logs', action_show_vpn_logs))
    menu.append(Gtk.SeparatorMenuItem.new())
    menu.append(build_menu_item('close', action_close_app))

    menu.show_all()
    
    return menu

def build_menu_item(name, handler):
    item = Gtk.MenuItem(name)
    item.connect('activate', handler)
    
    return item

def action_connect_vpn(object):
    indicator.set_icon(IMG_DIR + '/on.png')

def action_disconnect_vpn(object):
    indicator.set_icon(IMG_DIR + '/off.png')

def action_configure_vpn(object):
    dialog = Gtk.FileChooserDialog(
        title="Select openfortivpn configuration file",
        action=Gtk.FileChooserAction.OPEN,
        parent=Gtk.Window(),
        buttons=(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK,
            Gtk.ResponseType.OK
        )
    )

    filter = Gtk.FileFilter()
    filter.set_name('Text File')
    filter.add_mime_type('text/plain')
    dialog.add_filter(filter)

    if dialog.run() == Gtk.ResponseType.OK:
        global VPN_CONFIG
        VPN_CONFIG = dialog.get_filename()
        dialog.destroy()
    else:
        dialog.destroy()

def action_show_vpn_logs(object):
    pass

def action_close_app(object):
    Gtk.main_quit()

if __name__ == "__main__":
    indicator = AppIndicator3.Indicator.new(APP_NAME, IMG_DIR + '/off.png', AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()