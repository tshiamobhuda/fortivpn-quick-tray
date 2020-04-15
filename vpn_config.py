class VPNConfig:
    __vpn_config = '/etc/openfortivpn/Kosmosdal'
    __vpn_on = False
    __vpn_process = None

    @staticmethod
    def set_vpn_config(path):
        VPNConfig.__vpn_config = path
        print(VPNConfig.__vpn_config)  # TODO Remove me

    @staticmethod
    def get_vpn_config():
        return VPNConfig.__vpn_config

    @staticmethod
    def set_vpn_status(status):
        VPNConfig.__vpn_on = status
        print(VPNConfig.__vpn_on)  # TODO Remove me

    @staticmethod
    def get_vpn_status():
        return VPNConfig.__vpn_on

    @staticmethod
    def set_vpn_process(process):
        VPNConfig.__vpn_process = process

    @staticmethod
    def get_vpn_process():
        return VPNConfig.__vpn_process