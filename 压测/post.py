#!/usr/bin/env python
import requests
import json
import threading
from time import sleep, ctime, time, localtime, strftime
import re
import sys

def postlist(url,data_dict):
    f = file('/data/python/%s.log' % url.split('/')[-1], 'a')
    r = requests.post(url, data=data_dict)
    try:
        f.write(re.search('"status":"200"',str(r.text)).group()+'\n')
    except AttributeError ,e:
	return 'code is error!'
    f.close()

def go():
    f = file('/data/python/post.conf','r')
    v = f.readlines()
    url = []
    data_dict = []
    for i in v:
        u = re.match('^url',i.strip())
        d = re.match('^data_dict',i.strip())
        if u is not None:
	   url += i.strip().split('= ')[1].split(';')
	elif d is not None:
	   data_dict += i.strip().split('= ')[1].split(';')
    for i in range(0,len(url)):
	if url[i].strip() != '':
	    postlist(url[i], eval(data_dict[i]))

def main():
    print datetime.datetime.now()
    sa = strftime("%H%M%S", localtime()) 
    
    threads = []
    nloops = range(0,int(sys.argv[1]))
    
    for i in nloops:
        t = threading.Thread(target=go,args=())
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    sp = datetime.datetime.now()
    print 'stop time', ctime()

    print 'all need time(second):',int(sp) - int(sa)


def lock():
    f = file('/data/python/post.conf','r')
    v = f.readlines()
    url = []
    for i in v:
        u = re.match('^url',i.strip())
        if u is not None:
            url += i.strip().split('= ')[1].split(';')
    for i in range(0,len(url)):
	if url[i].strip() != '':
    	    f = file('/data/python/%s.log' % url[i].split('/')[-1])
	    n = len(f.read().strip().split('\n'))
  	    print '%s success amount:' % url[i], n
	    print '%s failed amount:' % url[i], int(sys.argv[1])*int(sys.argv[2]) - n


if __name__ == '__main__':
    for i in range(0,int(sys.argv[2])):
        main()
    lock()
#for i in range(0,10):
#    print i
