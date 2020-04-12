from abc import ABC, abstractmethod
from vpn_config import VPNConfig, IMG_DIR


class AbstractMenuItem(ABC):
    def __init__(self, gtk, name):
        self.__gtk = gtk
        self.__item = self.__gtk.MenuItem(name)
        self.__item.connect('activate', self.action)

    def get_menu_item(self):
        return self.__item

    @abstractmethod
    def action(self, o): pass


class CloseMenuItem(AbstractMenuItem):
    def __init__(self, gtk):
        super().__init__(gtk, 'close')
        self.gtk = gtk

    def action(self, o):
        self.gtk.main_quit()


class ConnectMenuItem(AbstractMenuItem):
    def __init__(self, gtk, indicator):
        super().__init__(gtk, 'connect')
        self.gtk = gtk
        self.indicator = indicator

    def action(self, o):
        self.indicator.set_icon(IMG_DIR + '/on.png')


class DisconnectMenuItem(AbstractMenuItem):
    def __init__(self, gtk, indicator):
        super().__init__(gtk, 'disconnect')
        self.gtk = gtk
        self.indicator = indicator

    def action(self, o):
        self.indicator.set_icon(IMG_DIR + '/off.png')


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
            VPNConfig().set_vpn_config(dialog.get_filename())
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
    def __init__(self, gtk, indicator):
        self.__gtk = gtk
        self.__indicator = indicator

    def build_menu(self):
        menu = self.__gtk.Menu()
        
        menu.append(ConnectMenuItem(self.__gtk, self.__indicator).get_menu_item())
        menu.append(DisconnectMenuItem(self.__gtk, self.__indicator).get_menu_item())
        menu.append(self.__gtk.SeparatorMenuItem.new())
        menu.append(ConfigMenuItem(self.__gtk).get_menu_item())
        menu.append(LogsMenuItem(self.__gtk).get_menu_item())
        menu.append(self.__gtk.SeparatorMenuItem.new())
        menu.append(CloseMenuItem(self.__gtk).get_menu_item())
        
        menu.show_all()

        return menu
