import os
import sys
import urllib2
import os
import sys
import urllib2
import hashlib
try:
    import json
except ImportError:
    import simplejson as json

from pprint import pprint

url     = "http://192.168.56.109/zabbix/api_jsonrpc.php"
usr     = "admin"
passwrd = "zabbix"

hash_pass = ""

def zbxAuth():
    global hash_pass
    login = {
        "jsonrpc" : "2.0",
        "method"  : "user.login",
        "params"  : {
           "user"     : usr,
           "password" : passwrd
        },
        "id"     : 1
    }
    res = printResult(login)

    if 'error' in res:
        print "Error: Connection Unsuccessful"
        sys.exit(-1)
    hash_pass=res["result"]
    print "Successfully Authenticated. Auth ID: " + hash_pass

    return res

def printResult(var):
    data = json.dumps(var)
    request = urllib2.Request(url, data, {"Content-Type" : "application/json"})
    response = urllib2.urlopen(request)
    return json.load(response)

zbxAuth()


def register_host():

    post_data = {
        "jsonrpc": "2.0",
        "method": "host.create",
        "params": {
            "host": "hostname",
            "templates": [{"templateid": "10001"}],
            "interfaces": [{"type": 1, "main": 1, "useip": 1, "ip": "127.0.0.1", "dns": "", "port": "10050"}],
            "groups": [{"groupid": "1"},{"groupid": "2"}],
        },
        "auth": hash_pass,
        "id": 1
    }

    res = printResult(post_data)
    if 'error' in res:
        print str(pprint(res))
        sys.exit(-1)
    return res

zbxAuth()
pprint(register_host())

