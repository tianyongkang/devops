from credentials import get_nova_credentials_v2
from novaclient.client import Client
import os
import json
import re
import sys

credentials = get_nova_credentials_v2()
nova_client = Client(**credentials)


class Server():
    net = nova_client.networks.find(label="demo-net")          
    net_pt = nova_client.networks.find(label="putao-net")      
    net_un = nova_client.networks.find(label="demo-net-unicom")
    nics = [{'net-id':net.id},{'net-id':net_un.id},{'net-id':net_pt.id}]
    image = nova_client.images.find(name="debianjessie") 
    flavor = nova_client.flavors.find(name="m1.small")   
    def create_server(self):
        dm = {}
        df = {}
        dk = {}
        hname = raw_input('Please input instance name:')

        imgs = nova_client.images.list()
        for i in range(len(imgs)):
            dm[i] = imgs[i]
        print dm
        img = raw_input('Please input image number:')
        for i in range(len(imgs)):
            if int(img) == i:
                image = imgs[i]
        
        flvs = nova_client.flavors.list()
        for i in range(len(flvs)):
            df[i] = flvs[i]
        print df
        flv = raw_input('Please input flavor number:')
        for i in range(len(flvs)):
            if int(flv) == i:
                flavor = flvs[i]

 
        keys = nova_client.keypairs.list()
        for i in range(len(keys)):
            dk[i] = keys[i]
        print dk
        key = raw_input('Please input keypair number:')
        for i in range(len(keys)):
            if int(key) == i:
                keypair = re.sub(' ','',re.sub('>','',str(keys[i]).split(':')[1]))
        instance = nova_client.servers.create(name=hname, image=image, flavor=flavor, key_name=keypair, nics=self.nics)
        print nova_client.servers.find(name = hname).id,'instance created'

    def list_server(self):
        os.system('nova list')
    
    def list_floating_ip_unused(self):
        f = nova_client.floating_ips.list()
        floatip_will = []
        for i in f:
            if str(i).split(', ')[2] == 'instance_id=None':
                floatip_will += [re.sub('ip=','',str(i).split(', ')[3])]
        print 'unused floating ip:'
        for i in sorted(floatip_will):
            print i

    def list_floating_ip_used(self):
        f = nova_client.floating_ips.list()
        floatip_will = []
        for i in f:
            if str(i).split(', ')[2] != 'instance_id=None':
                floatip_will += [re.sub('ip=','',str(i).split(', ')[3])]
        print 'used float ip:'
        for i in sorted(floatip_will):
            print i

    def add_floating_ip(self):
        server_id = raw_input('Please input instance id:')
        floatip = raw_input('Please input float ip:')
        fixedip = raw_input('Please input fixed ip address:')
        nova_client.servers.add_floating_ip(server_id,floatip,fixed_address=fixedip)
    def remove_floating_ip(self):
        server_id = raw_input('Please input instance id:')
        floatip = raw_input('Please input float ip:')
        nova_client.servers.remove_floating_ip(server_id,floatip)

    def drop_server(self):
        os.system('nova list')
        id = raw_input('Please input instance id:')
        nova_client.servers.find(id=id).stop()

    def start_server(self):
        os.system('nova list')
        id = raw_input('Please input instance id:')
        nova_client.servers.find(id=id).start()

    def delete_server(self):
        os.system('nova list')
        id = raw_input('Please input instance id:')
        nova_client.servers.find(id=id).delete()

def main():
    p = Server()
    if sys.argv[1] == '-C':
        p.create_server()
    elif sys.argv[1] == '-AF':
        p.list_server()
        p.list_floating_ip_unused()
        p.add_floating_ip()
    elif sys.argv[1] == '-LF':
        p.list_floating_ip_unused()
        p.list_floating_ip_used()
    elif sys.argv[1] == '-RF':
        p.list_server()
        p.list_floating_ip_used()
        p.remove_floating_ip()
    elif sys.argv[1] == '-OFF':
        p.drop_server()
    elif sys.argv[1] == '-ON':
        p.start_server()
    elif sys.argv[1] == '-LS':
        p.list_server()
    elif sys.argv[1] == '-D':
        p.delete_server()

if __name__ == '__main__':
    main()
