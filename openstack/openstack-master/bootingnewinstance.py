import os
from sys import argv
import time
import novaclient.v1_1.client as nvclient
from credentials import get_nova_creds
from neutronclient.v2_0 import client
def createinstance():
    creds = get_nova_creds()
    nova = nvclient.Client(**creds)

#if not nova.keypairs.findall(name="mykey"):
#    with open(os.path.expanduser(''))

# a key pair named "mykey" is already created. 


    neutron = client.Client(username='admin', password='supersecret', 
                            tenant_name='demo', 
                            auth_url=os.environ['OS_AUTH_URL'])
    neutron.format= 'json'
    netname = str(argv[2])

    print netname


    if not neutron.list_networks(name=netname)['networks']:
        print "network does not exist"
        exit(0)
    else:
        netid =  neutron.list_networks(name=netname)["networks"][0]["id"]

# prepare all paremeters image, flavor, instancename, networkinfo


    image = nova.images.find(name="cirros-0.3.1-x86_64-uec")
    flavor = nova.flavors.find(name="m1.tiny")
    instancename = str(argv[1])
    networkinfo =[{'net-id':netid}]
    
    print "new instance named", instancename,  "will be created"

    #networkinfo = {'uuid':'56b68aef-8080-45de-9206-152b8d0229b6'}

        

    instance = nova.servers.create(name=instancename, image=image, 
                                   flavor=flavor, key_name="mykey", 
                                   nics=networkinfo)

    status = instance.status
    while status =='BUILD':
        time.sleep(5)
        instance = nova.servers.get(instance.id)
        status = instance.status
    print "status: %s" % status


if __name__ == "__main__":
    createinstance()
