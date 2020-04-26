import gi
import signal

gi.require_version('Gtk', '3.0')
gi.require_version("AppIndicator3", "0.1")

from gi.repository import Gtk, AppIndicator3
from menu_items import MenuBuilder
from os import path

class Indicator():
    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new_with_path(
            'FortiVPN-Quick-Tray',
            'off',
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
            path.dirname(path.realpath(__file__)) + '/icons'
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_label('FortiVPN OFF', 'FortiVPN OFF')
        self.indicator.set_menu(self._build_menu())

        self.vpn_config = None

    def _build_menu(self):
        menu = Gtk.Menu()

        self.connect_menu_item = Gtk.MenuItem('Connect')
        self.disconnect_menu_item = Gtk.MenuItem('Disonnect')
        self.config_menu_item = Gtk.MenuItem('Config')
        self.logs_menu_item = Gtk.MenuItem('Logs')
        self.exit_menu_item = Gtk.MenuItem('Exit')

        self.connect_menu_item.connect('activate', self._click_exit)
        self.disconnect_menu_item.connect('activate', self._click_disconnect)
        self.config_menu_item.connect('activate', self._click_config)
        self.logs_menu_item.connect('activate', self._click_logs)
        self.exit_menu_item.connect('activate', self._click_exit)
        
        menu.append(self.connect_menu_item)
        menu.append(self.disconnect_menu_item)
        menu.append(Gtk.SeparatorMenuItem.new())
        menu.append(self.config_menu_item)
        menu.append(self.logs_menu_item)
        menu.append(Gtk.SeparatorMenuItem.new())
        menu.append(self.exit_menu_item)

        menu.show_all()

        return menu

    def _click_connect(self, object):
        pass

    def _click_disconnect(self, object):
        pass

    def _click_config(self, object):
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
            self.vpn_config = dialog.get_filename()
            print(self.vpn_config)
            dialog.destroy()
        else:
            dialog.destroy()

    def _click_logs(self, object):
        pass

    def _click_exit(self, object):
        Gtk.main_quit()

if __name__ == "__main__":

    Indicator()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()
