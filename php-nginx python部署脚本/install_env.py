#!/usr/bin/env python
from os import rename,system,unlink
from os.path import exists,isfile
from platform import uname,linux_distribution


source1404 = '''
deb http://mirrors.163.com/ubuntu/ trusty main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ trusty-security main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ trusty-updates main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ trusty-proposed main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ trusty-backports main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ trusty main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ trusty-security main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ trusty-updates main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ trusty-proposed main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ trusty-backports main restricted universe multiverse
'''

source1410 = '''
deb http://mirrors.163.com/ubuntu/ utopic main restricted universe multiverse 
deb http://mirrors.163.com/ubuntu/ utopic-security main restricted universe multiverse 
deb http://mirrors.163.com/ubuntu/ utopic-updates main restricted universe multiverse 
deb http://mirrors.163.com/ubuntu/ utopic-proposed main restricted universe multiverse 
deb http://mirrors.163.com/ubuntu/ utopic-backports main restricted universe multiverse 
deb-src http://mirrors.163.com/ubuntu/ utopic main restricted universe multiverse 
deb-src http://mirrors.163.com/ubuntu/ utopic-security main restricted universe multiverse 
deb-src http://mirrors.163.com/ubuntu/ utopic-updates main restricted universe multiverse 
deb-src http://mirrors.163.com/ubuntu/ utopic-proposed main restricted universe multiverse 
deb-src http://mirrors.163.com/ubuntu/ utopic-backports main restricted universe multiverse 
'''

cmd = 'apt-get install php5 php5-fpm php5-curl php5-gd php5-imagick php5-mysql php5-redis php5-mongo php5-memcache php5-imagick memcached nginx mongodb redis-server -y'
class Sourcefile(object):
    version = linux_distribution()[1]
    u1404 = source1404.strip()
    u1410 = source1410.strip()
    filelist = '/etc/apt/sources.list'
    def editsource(self):
	if exists(self.filelist) and isfile(self.filelist):
    	    rename(self.filelist,'/etc/apt/sources.list.bak')
	
        if linux_distribution()[1] == '14.04':
	    source = self.u1404
	else:
	    source = self.u1410
        file = open(self.filelist,'w')
	file.write(source+'\n')
        file.close()
	return system('apt-get update')

class Webinstall(object):
    def web(self):
        try:
	    system(cmd)
	except:
	    print "have a error!"

    def percona(self):
        pcmd = 'apt-get install percona-server-server-5.6 percona-server-client-5.6 -y '
	system('apt-key adv --keyserver keys.gnupg.net --recv-keys 1C4CBDCDCD2EFD2A')
        if exists('/etc/apt/sources.list.d/percona.list'):
	    unlink('/etc/apt/sources.list.d/percona.list')
        file = open('/etc/apt/sources.list.d/percona.list','a')
        if '14.04' in linux_distribution():
            file.write('deb http://repo.percona.com/apt trusty main'+'\n')	
            file.write('deb-src http://repo.percona.com/apt trusty main'+'\n')
            file.close()
	    system('apt-get update')
        
        if linux_distribution()[1] == '14.10':
            file.write('deb http://repo.percona.com/apt utopic main'+'\n')      
            file.write('deb-src http://repo.percona.com/apt utopic main'+'\n')
            file.close()
            system('apt-get update')
	system(pcmd)


def main():
     p=Sourcefile()
     p.editsource()
     p1=Webinstall()
     p1.web()
     p1.percona()

if __name__ == '__main__':
    main()
