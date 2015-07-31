#!/bin/bash
for num in `seq 0 255`
do
nmap -p22 10.1.$num.1-254 --host-timeout 2s |tee -a /etc/zabbix/scripts/ipfile/hostnmapssh
done

