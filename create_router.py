from neutronclient.v2_0 import client
from credentials import get_credentials
from create_network import Network
import os
from sys import argv
import json
from sys import argv

credentials = get_credentials()
neutron = client.Client(**credentials)

class Router(Network):
    router_id = 'router_id'
    def create_router(self, router_name):
        request = {'router': {'name': router_name,'admin_state_up': True}}
        router = neutron.create_router(request)
        self.router_id = router['router']['id']
    
    def create_gateway(self, network_id):
        g = neutron.add_gateway_router(self.router_id,body={'network_id': network_id})
        print json.dumps(g,sort_keys=False,indent=7,separators=(',',':'))

    def create_gateway_only(self,router_id,network_id):
        g = neutron.add_gateway_router(router_id, body={'network_id': network_id})
        print json.dumps(g,sort_keys=False,indent=7,separators=(',',':'))

    def create_interface(self, subnet_id):
        i = neutron.add_interface_router(self.router_id,body={'subnet_id': subnet_id})
        print json.dumps(i,sort_keys=False,indent=7,separators=(',',':'))

    def create_interface_only(self,router_id,subnet_id):
        i = neutron.add_interface_router(router_id, body={'subnet_id': subnet_id})
        print json.dumps(i,sort_keys=False,indent=7,separators=(',',':')) 

    def list_router(self):
        n = neutron.list_routers()['routers']
        print json.dumps(n,sort_keys=False,indent=7,separators=(',',':'))

def main():
    p = Router()
    o = os.popen('neutron net-list').read()
    try:
        if argv[1] == '-A':
            print o
            p.create_router(argv[2])
            network_id = raw_input("Please input outernal network_id:") 
            p.create_gateway(network_id)                                
            subnet_id = raw_input('Please input internal subnet_id:')  
            p.create_interface(subnet_id)
        elif argv[1] == '-Ar':
            p.create_router(argv[2])

        elif argv[1] == '-Aw':
            print o
            router_id = raw_input("Please input router id:")
            p.list_router()
            network_id = raw_input("Please input outernal network_id:") 
            p.create_gateway(router_id,network_id)

        elif argv[1] == '-Ai':
            p.list_router()
            router_id = raw_input("Please input router id:")
            print o
            subnet_id = raw_input('Please input internal subnet_id:') 
            p.create_interface_only(router_id,subnet_id)
        
        elif argv[1] == '-L':
            p.list_router()

        else:
            print 'python %s -A is create router,create outernal gateway,create internal gateway interface!'
            print 'python %s -Ar argv[1] is create router!'
            print 'python %s -Aw is create outernal gateway!'
            print 'python %s -Ai is create internal gateway interface!'
    except IndexError, e:
        print 'python %s -A is create router,create outernal gateway,create internal gateway interface!'
        print 'python %s -Ar argv[1] is create router!'                                                 
        print 'python %s -Aw is create outernal gateway!'                                               
        print 'python %s -Ai is create internal gateway interface!'                                     

if __name__ == '__main__':
    main()

#for i in dir(neutron):
#    print i

