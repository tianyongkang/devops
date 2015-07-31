from credentials import get_nova_credentials_v2
from novaclient.client import Client
import os

credentials = get_nova_credentials_v2()
nova_client = Client(**credentials)

print nova_client.servers.list()
print nova_client.images.list()
print nova_client.flavors.list()
print nova_client.networks.list()
print nova_client.keypairs.list()

os.system('neutron net-list')

nics = [{'net-id': 'ca6ed3aa-b12c-41ed-b8e7-08347a5278f1'}]
instance = nova_client.servers.create(name='debian', image=2, flavor='m1.small', key_name='open', nics=nics)
print instance
#for i in dir(nova_client):
#    print i
