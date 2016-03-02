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
    "auth": "93573a1afa67028fd0b074ca9e00df1f",
    "id": 1
}' http://$server/zabbix/api_jsonrpc.php
