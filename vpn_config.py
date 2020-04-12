from os import path

IMG_DIR = path.dirname(path.realpath(__file__)) + '/icons'


class VPNConfig:
    __vpn_config = '/etc/openfortivpn/Kosmosdal'
    __vpn_on = False

    @staticmethod
    def set_vpn_config(path):
        VPNConfig.__vpn_config = path
        print(VPNConfig.__vpn_config)  # TODO Remove me

    @staticmethod
    def get_vpn_config(self):
        return VPNConfig.__vpn_config

    @staticmethod
    def set_vpn_status(self, status):
        VPNConfig.__vpn_on = status
        print(VPNConfig.__vpn_on)  # TODO Remove me

    @staticmethod
    def get_vpn_status(self):
        return VPNConfig.__vpn_on
