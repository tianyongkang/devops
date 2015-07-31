#!/usr/bin/python
from neutronclient.v2_0 import client
from credentials import get_credentials
import json
from sys import argv
import os

class Network:
    net_dict = 'net_dict'
    credentials = get_credentials()
    neutron = client.Client(**credentials)
    def create_network_out(self,netname,pynetname):
        body_sample = {'network': {'name': netname, 'router:external': True, 'provider:physical_network':pynetname, 'provider:network_type': 'flat', 'admin_state_up': True}}
        netw = self.neutron.create_network(body = body_sample)
        self.net_dict = netw['network']
        print '------------------------------------------' 
        for i in self.net_dict:
            print i, ':' ,self.net_dict[i]    

        print '-------------------------------------------'
        print 'Network %s created' % self.net_dict['id']
        
    def create_network_int(self,netname):
        body_sample = {'network': {'name': netname, 'shared': True ,'admin_state_up': True}}
        netw = self.neutron.create_network(body = body_sample)
        self.net_dict = netw['network']
        print '------------------------------------------' 
        for i in self.net_dict:
            print i, ':' ,self.net_dict[i]    

        print '-------------------------------------------'
        print 'Network %s created' % self.net_dict['id']

    def create_subnet_int(self,subname,cidr):   
        body_create_subnet = {'subnets': [{'cidr': cidr, 'enable_dhcp': True, 'name': subname , 'ip_version': 4, 'network_id': self.net_dict['id']}]}
        subnet = self.neutron.create_subnet(body=body_create_subnet)
        print '-------------------------------------------' 
        for i in subnet['subnets']:
            for i1 in i:
                print i1,i[i1]
        print '-------------------------------------------'

    def create_subnet_nopool(self,subname,cidr):
        body_create_subnet = {'subnets': [{'cidr': cidr, 'enable_dhcp': False, 'name': subname , 'ip_version': 4, 'network_id': self.net_dict['id']}]}
        subnet = self.neutron.create_subnet(body=body_create_subnet)
        print '-------------------------------------------' 
        for i in subnet['subnets']:
            for i1 in i:
                print i1,i[i1]
        print '-------------------------------------------'


    def create_subnet_pool(self,subname,cidr,ip_start,ip_end,gw):
        body_create_subnet = {'subnets': [{'cidr': cidr, 'allocation_pools': [{'start':ip_start,'end':ip_end}],'gateway_ip':gw,'enable_dhcp': False, 'name': subname , 'ip_version': 4, 'network_id': self.net_dict['id']}]}
        subnet = self.neutron.create_subnet(body=body_create_subnet)
        print '-------------------------------------------' 
        for i in subnet['subnets']:                         
            for i1 in i:                                    
                print i1,i[i1]                              
        print '-------------------------------------------' 

    def create_subnet_pool_only(self,subname,cidr,ip_start,ip_end,gw,network_id):
        body_create_subnet = {'subnets': [{'cidr': cidr, 'allocation_pools': [{'start':ip_start,'end':ip_end}],'gateway_ip':gw,'enable_dhcp': False, 'name': subname , 'ip_version': 4, 'network_id': network_id}]}
        subnet = self.neutron.create_subnet(body=body_create_subnet)
        print '-------------------------------------------' 
        for i in subnet['subnets']:                         
            for i1 in i:                                    
                print i1,i[i1]                              
        print '-------------------------------------------'

    def list_network(self):
        l = self.neutron.list_networks()['networks']
        for i in range(0,len(l)):                                                
            yield json.dumps(l[i], sort_keys=False,indent=7,separators=(',',':'))

    def list_subnets(self):
        l = self.neutron.list_subnets()['subnets']
        for i in range(0,len(l)):                                                
            yield json.dumps(l[i], sort_keys=False,indent=7,separators=(',',':'))

    def delete_network(self,net_id):
        return self.neutron.delete_network(net_id)
    
    def delete_subnet(self,sub_id):
        return self.neutron.delete_subnet(sub_id)

def main():
    p = Network()
    try:
        if argv[1].upper() == '-LN':
            for i in p.list_network():
                print i

        elif argv[1].upper() == '-LS':
            for i in p.list_subnets():
                print i

        elif argv[1].upper() == '-AN':
            p.create_network_out(argv[2],argv[3])      
            p.create_subnet_nopool(argv[4],argv[5])

        elif argv[1].upper() == '-AP':
            p.create_network_out(argv[2],argv[3])
            p.create_subnet_pool(argv[4],argv[5],argv[6],argv[7],argv[8])

        elif argv[1].upper() == '-AI':
            p.create_network_int(argv[2])
            p.create_subnet_int(argv[3],argv[4])

        elif argv[1].upper() == '-AS':
            for i in range(0,len(p.list_network())):                                                 
                print json.dumps(p.list_network()[i], sort_keys=False,indent=7,separators=(',',':')) 
            network_id = raw_input("Please input network_id:")
            p.create_subnet_pool_only(argv[2],argv[3],argv[4],argv[5],argv[6],network_id)

        elif argv[1].upper() == '-DN':
            for i in p.list_network():
                print i
            net_id = raw_input('Please input will delete network id:')
            print 'deleted %s network!' % net_id,p.delete_network(net_id)

        elif argv[1].upper() == '-DS':
            for i in p.list_subnets():
                print i
            sub_id = raw_input('Please input will delete network id:')
            print 'deleted %s subnet!' % sub_id,p.delete_subnet(sub_id)

        elif argv[1].upper() == '-H':
            print 'must assign param!'
            print 'if fisrt param is -LN,is examine network list!'
            print 'if fisrt param is -DN ,and raw_input input network id ,is delete network!'
            print 'if fisrt param is -LS,is examine subnets list!'
            print 'if fisrt param is -DS ,and raw_input input subnet id ,is delete subnet!'
            print 'if fisrt param is -AI,Add new internal network and subnets,command example: python %s -AI demo-net demo-subnet 192.168.1.0/24' % argv[0]
            print 'if fisrt param is -AS,Only add new outernal subnets,command example: python %s -AS  ext-subnet-unicom 10.1.14.0/24 10.1.14.200 10.1.14.220 10.1.14.1 network-id' % argv[0]
            print 'if fisrt param is -AN,Add new outernal network and subnets,not assign network segment and gateway command example: python %s -AN ext-net external ext-subnet 10.1.12.0/24' % argv[0]
            print 'if fisrt param is -AP,Add new outernal network and subnets, assign network segment and gateway command example: python %s -AP ext-net external ext-subnet 10.1.12.0/24 10.1.12.200 10.1.12.220 10.1.12.1' % argv[0]
        
        else:
            print 'Please python %s -h' % argv[0]

    except IndexError, e:
        print 'must assign param!'
        print 'if fisrt param is -LN,is examine network list!'
        print 'if fisrt param is -DN ,and raw_input input network id ,is delete network!'
        print 'if fisrt param is -LS,is examine subnets list!'
        print 'if fisrt param is -DS ,and raw_input input subnet id ,is delete subnet!'
        print 'if fisrt param is -AI,Add new internal network and subnets,command example: python %s -AI demo-net demo-subnet 192.168.1.0/24' % argv[0]
        print 'if fisrt param is -AS,Only add new outernal subnets,command example: python %s -AS  ext-subnet-unicom 10.1.14.0/24 10.1.14.200 10.1.14.220 10.1.14.1 network-id' % argv[0]
        print 'if fisrt param is -AN,Add new outernal network and subnets,not assign network segment and gateway command example: python %s -AN ext-net external ext-subnet 10.1.12.0/24' % argv[0]
        print 'if fisrt param is -AP,Add new outernal network and subnets, assign network segment and gateway command example: python %s -AP ext-net external ext-subnet 10.1.12.0/24 10.1.12.200 10.1.12.220 10.1.12.1' % argv[0]
        
if __name__ == '__main__':
    main()
