import gi
import signal

gi.require_version('Gtk', '3.0')
gi.require_version("AppIndicator3", "0.1")

from gi.repository import Gtk, AppIndicator3
from os import path
from subprocess import run, Popen, PIPE, TimeoutExpired
from shlex import split
from threading import Thread
from time import sleep


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

        self.vpn_config = '/etc/openfortivpn/config'
        self.vpn_process = None

    def _build_menu(self):
        menu = Gtk.Menu()

        self.connect_menu_item = Gtk.MenuItem('Connect')
        self.disconnect_menu_item = Gtk.MenuItem('Disonnect')
        self.disconnect_menu_item.set_sensitive(False)
        self.config_menu_item = Gtk.MenuItem('Config')
        self.logs_menu_item = Gtk.MenuItem('Logs')
        self.exit_menu_item = Gtk.MenuItem('Exit')

        self.connect_menu_item.connect('activate', self._click_connect)
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
        self._change_icon('TRY')
        self._set_fields_sensitivity(False, ['connect', 'config', 'close'])

        with open('output.log', 'w+b') as f:
            try:
                self.vpn_process = Popen(split('pkexec openfortivpn -c ' + self.vpn_config), stdin=PIPE, stdout=f, stderr=f)
                self.vpn_process.communicate(timeout=1)
            except TimeoutExpired:
                pass
        
        vpn_process_thread = Thread(target=self._monitor_logs, daemon=True)
        vpn_process_thread.start()

    def _click_disconnect(self, object):
        try:
            run(split('pkexec kill ' + str(self.vpn_process.pid)))
        except ChildProcessError:
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
        dialog = Gtk.Dialog(
            title="Logs",
            parent=Gtk.Window(),
            buttons=(
                Gtk.STOCK_CLOSE,
                Gtk.ResponseType.CLOSE,
            )
        )

        dialog.set_default_size(440, 440)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)

        text_view = Gtk.TextView()
        text_view.set_editable(False)
        text_buffer = text_view.get_buffer()

        if self.vpn_process != None:
            with open('output.log') as logs:
                text_buffer.set_text(logs.read())
        else:
            with open('output.log', 'w'): 
                pass

        scrolledwindow.add(text_view)

        container = dialog.get_content_area()
        container.add(scrolledwindow)

        dialog.show_all()

        if dialog.run() == Gtk.ResponseType.CLOSE:
            dialog.destroy()

    def _click_exit(self, object):
        if self.indicator.get_attention_icon_desc() == 'ON':
            dialog = Gtk.MessageDialog(
                Gtk.Window(),
                0,
                Gtk.MessageType.WARNING,
                Gtk.ButtonsType.CLOSE,
                'VPN ON'
            )
            dialog.format_secondary_text("VPN is still ON. Please Disconnect first before exiting")

            if dialog.run() == Gtk.ResponseType.CLOSE:
                dialog.destroy()

                return

        Gtk.main_quit()

    def _monitor_logs(self):
        with open('output.log') as f:
            while True:
                line = f.readline()
                if line.find('Error') != -1 or line.find('ERROR') != -1:
                    self._set_fields_sensitivity(True, ['connect' , 'config', 'close'])
                    self._change_icon('ERR')
                    break

                if line.find('Tunnel is up and running') != -1:
                    self.disconnect_menu_item.set_sensitive(True)
                    self._change_icon('ON')

                if line.find('Logged out') != -1:
                    self.disconnect_menu_item.set_sensitive(False)
                    self._set_fields_sensitivity(True, ['connect', 'config', 'close'])
                    self._change_icon('OFF')
                    break

                sleep(0.1)

    def _change_icon(self, state):
        self.indicator.set_attention_icon_full(state.lower(), state)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ATTENTION)
        self.indicator.set_label(f'FortiVPN {state}', 'FortiVPN OFF')

    def _set_fields_sensitivity(self, sensitivity, fields):
        def _set_sensitivity(object, data): 
            menu_item_label = object.get_label()

            if menu_item_label.lower() in data.get('fields'):
                object.set_sensitive(data.get('sensitivity'))
                
        container = self.indicator.get_menu()
        container.foreach(_set_sensitivity, {'sensitivity': sensitivity, 'fields': fields})


if __name__ == "__main__":
    Indicator()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()
