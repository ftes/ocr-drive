#!/usr/bin/python
#Parameters: <output_directory>
#
#Can be set up as cron job:
#* * * * *	<path-to-this-script> <ocr-hot-directory>

import sys

from authorize import getCredentials
from common import *

from tempfile import mkstemp

OCR_FOLDER = "Documents/Pending OCR"


# Obtain connection
credentials = getCredentials()
service = getService(credentials)
ocrFolder = getSubFolderId(service, OCR_FOLDER)
if ocrFolder is None:
	print "No 'Pending OCR' folder exists from which files can be downloaded, exiting"
	sys.exit(1)

files = getFileList(service, ocrFolder)

outputDir = sys.argv[1]

for fileInfo in files:
	fileId = fileInfo["id"]
	driveFile = service.files().get(fileId=fileId).execute()

	# Download and save file
	data = downloadFile(service, driveFile)
	# _, outputFileDir = mkstemp(dir = outputDir, suffix = ".pdf")
        outputFileDir = os.path.join(outputDir, driveFile['title'])
	outputFile = open(outputFileDir, 'w')
	outputFile.write(data)
	outputFile.close()

	# Remove file from GDrive
	service.files().trash(fileId=fileId).execute()

print "Processed " + str(len(files)) + " files"

sys.exit(0)
