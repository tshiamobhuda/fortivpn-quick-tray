class VPNConfig():
    __vpn_config = '/etc/openfortivpn/Kosmosdal'

    def set_vpn_config(self, path):
        VPNConfig.__vpn_config = path
        print(VPNConfig.__vpn_config)

    def get_vpn_config(self):
        return VPNConfig.__vpn_config

