#!/usr/bin/python
#Parameters: <path_to_file>
#
#If experiencing authentication problems (SSL error), cacerts.txt might be root readable only.
#sudo chmod o+r /usr/local/lib/python2.7/dist-packages/httplib2-0.8-py2.7.egg/httplib2/cacerts.txt

import sys

from authorize import getCredentials
from common import *

SCANS_FOLDER = "Documents/Scans"


# Obtain connection
fileName = sys.argv[1]
uploadName = sys.argv[2]
credentials = getCredentials()
service = getService(credentials)
scansFolder = getSubFolderId(service, SCANS_FOLDER)
if scansFolder is None:
	print "No 'Scans' folder exists to which file can be uploaded, exiting"
	sys.exit(1)

#Upload file
uploadFile(service, fileName, scansFolder, uploadName)
print "Uploaded file"

sys.exit(0)
