#!/bin/bash
hostip_zabbix=`grep 'open  ssh' -B 3 /etc/zabbix/scripts/ipfile/hostnmapssh|awk '/scan report/{print $5,$6}'|awk '/^[{a-z}]/{print $0}'|awk '{split($0,ip,"(");print ip[1],ip[2]}'|awk '{split($0,ip,")");print ip[1]}'|awk '{split($0,ip," ");print ip[2]}'|sort -t. -k 4 -n`

zabbix_interface=`mysql -uroot -pyeah.mobi zabbix -e "select ip from interface\G"|awk '/ip/{print $2}'|awk '/^10.1./{print $0}'`

for inter in $zabbix_interface
do
touch /tmp/$inter
done

if [ $? = 0 ]
then 
for ip in $hostip_zabbix
do
if [ -e /tmp/$ip ]
   then
echo $ip >> /etc/zabbix/scripts/ipfile/monitored
else 
echo $ip >> /etc/zabbix/scripts/ipfile/notmonitored
fi
done
fi
