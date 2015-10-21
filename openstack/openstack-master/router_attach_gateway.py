import os
from sys import argv
import random
import logging
from neutronclient.v2_0 import client

def createrouter():
    """ thus function will first check the arguments and check their id, finally create the router
        finally, create the router, add interface absed on the interfeace
    """
 
    # authenticate the nuetron client 

    neutron = client.Client(username='admin', password='supersecret', tenant_name='admin', auth_url=os.environ['OS_AUTH_URL'])
    neutron.format= 'json'


    
    # check if the router name exists or not

    routername = str(argv[1])

    if neutron.list_routers(name=routername)['routers']:
        routerid =  neutron.list_routers(name=routername)["routers"][0]["id"]
    else:
        print "router does not exist. " 


    
    publicnetid = neutron.list_networks(name='public')['networks'][0]['id']
    print "public net id is", publicnetid


#    cidr = str(argv[2])

#    subnetid = neutron.list_subnets(cidr=cidr)['subnets'][0]['id']

#    subnet_id = {'subnet_id': subnetid}

#    neutron.add_interface_router(routerid, body=subnet_id)


   # externalgw = {'external_gateway_info': {'network_id': publicnetid }}
    externalgw = {'network_id': publicnetid }
    neutron.add_gateway_router(routerid, body=externalgw)


if False:
   
    # create router with info above
    
    routers = {'name': routername, 'admin_state_up': True}
    router = neutron.create_router({'router':routers})

    print 'router:'+ routername  + ' is created' 

    routerid = router['router']['id']
    print 'router id is:', routerid


    # add subnets interfaces to the routers
    
    for subnetid in subnetids:
        subnet_id = {"subnet_id": subnetid }
        neutron.add_interface_router(subnet_id)


    # add public interface to the router

    subnetinfo = {'subnet_id': subnetid}
    neutron.add_interface_router(ubnetinfo)


if False:
    print "deleting the router"
    neutron.delete_router(router['routers'][0]['id'])


if __name__ == "__main__":

    if len(argv)!=2:
         print "This function takes at 1  arguments, usage: ./router_add_gateway.py routername"
         exit(0) 
    else:
        print 'valid input ! '
        createrouter()
