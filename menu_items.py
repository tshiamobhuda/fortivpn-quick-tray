from abc import ABC, abstractmethod
from vpn_config import VPNConfig
from subprocess import run, Popen, PIPE, TimeoutExpired
from shlex import split
from time import sleep
from threading import Thread, enumerate, active_count


class AbstractMenuItem(ABC):
    def __init__(self, gtk, name):
        self.__gtk = gtk
        self._item = self.__gtk.MenuItem(name)
        self._item.connect('activate', self.action)

    def get_menu_item(self):
        return self._item

    @abstractmethod
    def action(self, o): pass


class CloseMenuItem(AbstractMenuItem):
    def __init__(self, gtk):
        super().__init__(gtk, 'Close')
        self.gtk = gtk

    def action(self, o):
        # TODO probably check if VPN is running & close it first 
        self.gtk.main_quit()


class ConnectMenuItem(AbstractMenuItem):
    def __init__(self, gtk, indicator, app_indicator):
        super().__init__(gtk, 'Connect')
        self.gtk = gtk
        self.indicator = indicator
        self.app_indicator = app_indicator

    def action(self, o):
        self.set_fields_sensitivity(False, ['connect', 'disconnect', 'config', 'close'])

        config_file = VPNConfig.get_vpn_config()

        with open('output.log', 'w+b') as logs_file:
            try:
                VPNConfig.set_vpn_process(Popen(split('pkexec openfortivpn -c ' + config_file), stdin=PIPE, stdout=logs_file, stderr=logs_file))
                VPNConfig.get_vpn_process().communicate(timeout=1)
            except TimeoutExpired:
                print('time exipred')
                pass
        
        my_thread = Thread(target=self.monitor_logs, daemon=True)
        my_thread.start()

    def set_fields_sensitivity(self, sensitivity, fields):
        def _set_sensitivity(object, data): 
            menu_item_label = object.get_label()

            if menu_item_label.lower() in data.get('fields'):
                object.set_sensitive(data.get('sensitivity'))
                
        container = self.indicator.get_menu()
        container.foreach(_set_sensitivity, {'sensitivity': sensitivity, 'fields': fields})

    def monitor_logs(self):
        print('thread started')
        with open('output.log') as f:
            while True:
                line = f.readline()
                if line.find('Error') != -1 or line.find('ERROR') != -1:
                    print('error', line)
                    self.set_fields_sensitivity(True, ['connect' , 'config', 'close'])
                    self.indicator.set_attention_icon_full('err', 'Error')
                    self.indicator.set_status(self.app_indicator.IndicatorStatus.ATTENTION)
                    self.indicator.set_label('FortiVPN ERR', 'FortiVPN OFF')
                    break

                if line.find('Tunnel is up and running') != -1:
                    print('connected', line)
                    self.set_fields_sensitivity(True, ['disconnect'])
                    self.indicator.set_attention_icon_full('on', 'Connected')
                    self.indicator.set_status(self.app_indicator.IndicatorStatus.ATTENTION)
                    self.indicator.set_label('FortiVPN ON', 'FortiVPN OFF')
                    
                
                if line.find('Logged out') != -1:
                    print('disconnected', line)
                    self.set_fields_sensitivity(True, ['connect', 'config', 'close'])
                    self.indicator.set_attention_icon_full('off', 'Disconnected')
                    self.indicator.set_status(self.app_indicator.IndicatorStatus.ATTENTION)
                    self.indicator.set_label('FortiVPN OFF', 'FortiVPN OFF')
                    break

                sleep(0.1)

class DisconnectMenuItem(AbstractMenuItem):
    def __init__(self, gtk, indicator, app_indicator):
        super().__init__(gtk, 'Disconnect')
        self.gtk = gtk
        self.app_indicator = app_indicator
        self.indicator = indicator
        self._item.set_sensitive(False)

    def action(self, o):
        try:
            run(split('pkexec kill ' + str(VPNConfig.get_vpn_process().pid)))
        except ChildProcessError as error:
            print(error.errno, error.strerror)


class ConfigMenuItem(AbstractMenuItem):
    def __init__(self, gtk):
        super().__init__(gtk, 'Config')
        self.gtk = gtk

    def action(self, o):
        dialog = self.gtk.FileChooserDialog(
            title="Select openfortivpn configuration file",
            action=self.gtk.FileChooserAction.OPEN,
            parent=self.gtk.Window(),
            buttons=(
                self.gtk.STOCK_CANCEL,
                self.gtk.ResponseType.CANCEL,
                self.gtk.STOCK_OK,
                self.gtk.ResponseType.OK
            )
        )

        filter = self.gtk.FileFilter()
        filter.set_name('Text File')
        filter.add_mime_type('text/plain')
        dialog.add_filter(filter)

        if dialog.run() == self.gtk.ResponseType.OK:
            VPNConfig.set_vpn_config(dialog.get_filename())
            dialog.destroy()
        else:
            dialog.destroy()


class LogsMenuItem(AbstractMenuItem):
    def __init__(self, gtk):
        super().__init__(gtk, 'Logs')
        self.gtk = gtk

    def action(self, o):
        dialog = self.gtk.Dialog(
            title="Logs",
            parent=self.gtk.Window(),
            buttons=(
                self.gtk.STOCK_CLOSE,
                self.gtk.ResponseType.CLOSE,
            )
        )

        dialog.set_default_size(440, 440)

        scrolledwindow = self.gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)

        text_view = self.gtk.TextView()
        text_buffer = text_view.get_buffer()

        with open('output.log') as logs:
            text_buffer.set_text(logs.read())

        scrolledwindow.add(text_view)

        container = dialog.get_content_area()
        container.add(scrolledwindow)

        dialog.show_all()

        if dialog.run() == self.gtk.ResponseType.CLOSE:
            dialog.destroy()


class MenuBuilder:
    def __init__(self, gtk, indicator, app_indicator):
        self.__gtk = gtk
        self.__indicator = indicator
        self.__app_indicator = app_indicator

    def build_menu(self):
        menu = self.__gtk.Menu()
        
        menu.append(ConnectMenuItem(self.__gtk, self.__indicator, self.__app_indicator).get_menu_item())
        menu.append(DisconnectMenuItem(self.__gtk, self.__indicator, self.__app_indicator).get_menu_item())
        menu.append(self.__gtk.SeparatorMenuItem.new())
        menu.append(ConfigMenuItem(self.__gtk).get_menu_item())
        menu.append(LogsMenuItem(self.__gtk).get_menu_item())
        menu.append(self.__gtk.SeparatorMenuItem.new())
        menu.append(CloseMenuItem(self.__gtk).get_menu_item())
        
        menu.show_all()

        return menu
