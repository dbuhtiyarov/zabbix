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


def zbxImport(filename):
    global hash_pass
    with open(filename, 'rb') as fff:
        imprt = {
            "jsonrpc": "2.0",
            "method" : "configuration.import",
            "params" : {
                "format"    :   "xml",
                "rules"     :   {
                    "groups" :   {
                        "createMissing"  :  True,
                        "updateExisting" :  True
                        },
                    "hosts"     :   {
                        "createMissing"   :  True,
                        "updateExisting"  :  True
                        },
                    "templates" :  {
                        "createMissing"   :  True,
                        "updateExisting"  :  True
                        },
                    "triggers"  :  {
                        "createMissing"   :  True,
                        "updateExisting"  :  True
                        },
                    "items"      : {
                        "createMissing"   :   True,
                        "updateExisting"  :   True
                        }
                    },
                    "source" :  fff.read()
                },
            "auth" : hash_pass,
            "id"   : 2
        } 

   
        res = printResult(imprt)


    if 'error' in res:
        print "Import unsuccessful for file: " + str(filename)
        print str(pprint(res))
        sys.exit(-1)

    return res


def printResult(var):
    data = json.dumps(var)
    request = urllib2.Request(url, data, {"Content-Type" : "application/json"})
    response = urllib2.urlopen(request)
    return json.load(response)

zbxAuth()
my_file = os.path.abspath(sys.argv[1])
print "Let's use %s" % my_file
result = zbxImport(my_file)

from pprint import pprint
pprint(result)
