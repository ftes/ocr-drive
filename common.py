import httplib2
import sys

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from apiclient import errors

def getService(credentials):
	# Create an httplib2.Http object and authorize it with our credentials
	http = httplib2.Http()
	http = credentials.authorize(http)

	service = build('drive', 'v2', http=http)

	return service

def getFolderId(service, folderName, parentId="root"):
	folder = service.children().list(
			folderId=parentId, q="title = '" + folderName + "'").execute().get('items', [])
	if len(folder) == 1:
		folder = folder[0]['id']
	else:
		return None
	return folder
	
def getSubFolderId(service, folderName, parentId="root"):
	left, sep, right = folderName.partition("/")
	if len(sep) == 0:
		# No further sub-folder
		return getFolderId(service, left, parentId)
	parentId = getFolderId(service, left, parentId)
	return getSubFolderId(service, right, parentId)

def uploadFile(service, filePath, parentId, uploadName):
	# Insert a file
	media_body = MediaFileUpload(filePath, mimetype='application/pdf', resumable=True)
	body = {
		'title': uploadName,
		'parents': [{
		'kind': 'drive#fileLink',
		'id': parentId
		}],
		'mimeType': 'application/pdf'
	}

	file = service.files().insert(body=body, media_body=media_body).execute()

def getFileList(service, folderId):
	children = service.children().list(
		folderId=folderId, q="trashed = false").execute()

	return children.get('items', [])

def downloadFile(service, driveFile):
	"""Download a file's content.

	Args:
		service: Drive API service instance.
		drive_file: Drive File instance.

	Returns:
		File's content if successful, None otherwise.
	"""
	download_url = driveFile.get('downloadUrl')
	if download_url:
		resp, content = service._http.request(download_url)
		if resp.status == 200:
			return content
		else:
			print 'An error occurred: %s' % resp
			return None
	else:
		# The file doesn't have any content stored on Drive.
		return None
