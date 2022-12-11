#!/usr/bin/python3
#first, install python3 and opendirectory.
#sudo python3 -m pip install pyobjc-framework-opendirectory
#way to run this script is: # sudo python3 ldaps_macos_script.py ldap.google.com.plist
from OpenDirectory import ODNode, ODSession, kODNodeTypeConfigure
from Foundation import NSMutableData, NSData

import os
import sys

# Reading plist
GOOGLELDAPCONFIGFILE = open(sys.argv[1], "r")
CONFIG = GOOGLELDAPCONFIGFILE.read()
GOOGLELDAPCONFIGFILE.close()
#print(CONFIG)
# Write the plist
od_session = ODSession.defaultSession()
od_conf_node, err = ODNode.nodeWithSession_type_error_(od_session, kODNodeTypeConfigure, None)
request = NSMutableData.dataWithBytes_length_(b'\x00'*32, 32)
str_as_bytes=str.encode(CONFIG)
request.appendData_(NSData.dataWithBytes_length_(str_as_bytes, len(str_as_bytes)))
##request.appendData_(NSData.dataWithBytes_length_(CONFIG, len(CONFIG)))
print(request)
response, err = od_conf_node.customCall_sendData_error_(99991, request, None)
# Edit the default search path and append the new node to allow for login
os.system("dscl -q localhost -append /Search CSPSearchPath /LDAPv3/ldap.google.com")
os.system("bash -c 'echo -e \"TLS_IDENTITY\tLDAP Client\" >> /etc/openldap/ldap.conf' ")
