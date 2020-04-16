from abc import ABC, abstractmethod
from vpn_config import VPNConfig
from subprocess import run, Popen, PIPE, TimeoutExpired, CalledProcessError
from shlex import split


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
        self.gtk.main_quit()


class ConnectMenuItem(AbstractMenuItem):
    def __init__(self, gtk, indicator, app_indicator):
        super().__init__(gtk, 'Connect')
        self.gtk = gtk
        self.indicator = indicator
        self.app_indicator = app_indicator

    def action(self, o):
        config_file = VPNConfig.get_vpn_config()
        VPNConfig.set_vpn_process(Popen(split('pkexec openfortivpn -c ' + config_file), stdin=PIPE, stdout=PIPE, stderr=PIPE))
        process = VPNConfig.get_vpn_process()

        try:
            out_data, _ = process.communicate(timeout=5)
            
            if len(out_data) and 'VPN account password' in out_data.decode():
                self.indicator.set_attention_icon_full('err', 'Error')
                self.indicator.set_status(self.app_indicator.IndicatorStatus.ATTENTION)
                self.indicator.set_label('FortiVPN ERR', 'FortiVPN OFF')
                VPNConfig.set_vpn_status = False
                
                return

        except TimeoutExpired:
            pass

        while True:
            output = process.stdout.readline()            
            if process.poll() is not None and output == '':
                break

            if 'Tunnel is up and running' in output.decode():
                VPNConfig.set_vpn_status = True
                self.indicator.set_attention_icon_full('on', 'Connected')
                self.indicator.set_status(self.app_indicator.IndicatorStatus.ATTENTION)
                self.indicator.set_label('FortiVPN ON', 'FortiVPN OFF')
                # self._item.set_sensitive(False)
                break


class DisconnectMenuItem(AbstractMenuItem):
    def __init__(self, gtk, indicator, app_indicator):
        super().__init__(gtk, 'Disconnect')
        self.gtk = gtk
        self.app_indicator = app_indicator
        self.indicator = indicator

    def action(self, o):
        if not VPNConfig.get_vpn_status():
            return

        try:
            run(split('pkexec kill ' + str(VPNConfig.get_vpn_process().pid)))

            VPNConfig.set_vpn_status = False
            self.indicator.set_attention_icon_full('off', 'Disconnected')
            self.indicator.set_status(self.app_indicator.IndicatorStatus.ATTENTION)
            self.indicator.set_label('FortiVPN OFF', 'FortiVPN OFF')

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
        pass


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
