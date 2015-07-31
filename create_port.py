#!/usr/bin/python
from neutronclient.v2_0 import client
from credentials import get_credentials
import uuid
import json
from sys import argv

credential = get_credentials()
neutron = client.Client(**credential)

class Port():
    def update_port(self):
        body_value = {"port": {"binding:host_id": "network-compute","admin_state_up": True,"device_owner": "network:router_gateway", "fixed_ips": [{"subnet_id":"0ecbf1e0-62d1-45a5-93ac-00192fcfa4bd","ip_address":"192.168.227.210"},{"subnet_id":"ce51c839-d42c-4ef5-a8fa-d12c1c13e15a","ip_address":"192.168.228.210"}]}}
        u = neutron.update_port('5344c61f-da90-4dfe-9242-d25376266d94',body=body_value) 
        print json.dumps(u, sort_keys=False,indent=7,separators=(',',':'))

    def list_port(self):
        l = neutron.list_ports()['ports']
        return l



def main():
    p = Port()
    if argv[1] == '-U':
        p.update_port()
    elif argv[1] == '-L':
        for i in p.list_port():
            print json.dumps(i, sort_keys=False,indent=7,separators=(',',':'))
    else:
        print 'is not aram!'


if __name__ == '__main__':
    main()
