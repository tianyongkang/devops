#!/usr/bin/env python
#coding=utf-8
import os,sys
import json
import urllib2
from urllib2 import Request, urlopen, URLError, HTTPError
# based url and required header
url = "http://localhost:8888/api_jsonrpc.php"
header = {"Content-Type": "application/json"}
f=file("/etc/zabbix/scripts/ipfile/notmonitored")
hostlist = []
hostiplist = []
for line in f.readlines():
    hostip=line.split()[0]
    hostiplist.append(hostip)
    hostlst=line.split()
    hostlist.append(hostlst)
    zabbix_list = dict((hostlist))

for ip in zabbix_list:
    data = json.dumps(
    {
        "jsonrpc": "2.0",
        "method": "host.create",
        "params": {
            "host": zabbix_list[ip],
            "interfaces": [
                {
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": ip,
                    "dns": "",
                    "port": "10050"
                }
            ],
            "groups": [
                { 
                    "groupid": "12"
                },
                { 
                    "groupid": "17"
                }
            ],
            "templates": [
                {
                  "templateid": '10198'
                },
                {
                  "templateid": '10265'
                },
                {
                  "templateid": '10319'
                }
            ],
         },    
         "auth":"afa736ff6d58c746efa28194b5e1af9f", # the auth id is what auth script returns, remeber it is string
         "id":0
    })
    # create request object
    
    request = urllib2.Request(url,data)
    for key in header:
        request.add_header(key,header[key])
    # get host list
    try:
        result = urllib2.urlopen(request)
    except URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server could not fulfill the request.'
            print 'Error code: ', e.code
    else:
        response = json.loads(result.read())
        result.close()
        hostid=response['result']
        print "Host ID:",hostid['hostids'],"Host Name:",zabbix_list[ip]
