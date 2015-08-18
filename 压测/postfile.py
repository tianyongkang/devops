#!/usr/bin/python

import requests
import json
from PIL import Image
import urllib2, os
import threading
from time import sleep, ctime

url = 'http://10.1.11.31:8081/upload'

def post(code):
    print 'ctime %d start time:' % code, ctime()
    payload = {'appid':'1000', 'x:uid':'1000', 'uploadToken':'16ea8772e383bb56b9bf0be63b3dd1fc:LqByZ-1SvOluAXfizqYQ2QVv9WM=:eyJkZWFkbGluZSI6MTQ0Mzc3ODA1NiwiY2FsbGJhY2tCb2R5IjpbXX0=', 'filename':'test', 'sha1':'test'}
    fn = os.popen("find /data/%d -type f" % code)
    f = fn.readlines()
    for i in range(len(f)):
        fjpeg = f[i].strip()
        jpeg = f[i].strip().split('/')[-1]
        files = {'file': (jpeg, file(fjpeg, 'rb'), 'image/jpeg', {'Expires': '0'})}
        r = requests.post(url,data=payload,files=files)

    print 'ctime %d stop time: ' % code, ctime()



def main():
    threads = []
    nloops = [1,2,3,4,5,6,7,8,9]
    
    for i in nloops:
        t = threading.Thread(target=post,args=(i,))
        threads.append(t)

    for i in range(0,9):
        threads[i].start()

    for i in range(0,9):
        threads[i].join()


if __name__ == '__main__':
    main()
