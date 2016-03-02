#!/bin/bash

server=$SERVER
ipaddr=`ifconfig | grep inet | grep -v inet6 | grep -v 127.0.0.1 | cut -d: -f2 | awk '{printf $1"\n"}'`
log=$LOG
pass=$PASS


curl -i -k -u $LOG:$PASS -X POST -H 'Content-Type: application/json' -d '{
    "jsonrpc": "2.0",
    "method": "host.create",
    "params": {
        "host": "'$HOSTNAME'",
        "interfaces": [
            {
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": "'$ipaddr'",
                "dns": "",
                "port": "10050"
            }
        ],
         "groups": [
            {
                "groupid": "'$GROUP_ID'"
            }
        ],
        "templates": [
            {
                "templateid": "'$TEMPLEATE_ID'"
            }
           ]
            },
    "auth": "1613e658c2b15feda6d4360da0e3f5e8",
    "id": 1
}' http://$server/zabbix/api_jsonrpc.php
