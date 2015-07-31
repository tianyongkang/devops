#!/usr/bin/env python2.7
#coding=utf-8
import json
import urllib2
# based url and required header
url = "http://localhost:8888/api_jsonrpc.php"
header = {"Content-Type": "application/json"}
# request json
data = json.dumps(
{
    "jsonrpc":"2.0",
    "method":"hostgroup.get",
    "params":{
        "output":["groupid","name"],
        "filter":{"groups":""}
    },
    "auth":"afa736ff6d58c746efa28194b5e1af9f", # the auth id is what auth script returns, remeber it is string
    "id":1,
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
#    print (response)
    print "Number Of Hostgroups: ", len(response['result'])
    for hostgroup in response['result']:
        print "Hostgroup ID:",hostgroup['groupid'],"Hostgroup Name:",hostgroup['name']
