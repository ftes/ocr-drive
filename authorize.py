#!/usr/bin/python

from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets

import os
import sys


# Path to client-secrets.json which should contain a JSON document such as:
#   {
#     "web": {
#       "client_id": "[[YOUR_CLIENT_ID]]",
#       "client_secret": "[[YOUR_CLIENT_SECRET]]",
#       "redirect_uris": [],
#       "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#       "token_uri": "https://accounts.google.com/o/oauth2/token"
#     }
#   }
CLIENTSECRETS_LOCATION = 'client-secrets.json'
SCOPES = ['https://www.googleapis.com/auth/drive']
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

# Path to stored OAuth credentials
CRED_FILENAME = 'credentials'


def getCredentials():
	credPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), CRED_FILENAME)
	storage = Storage(credPath)
	credentials = storage.get()
	if not credentials:
		print "Get credentials before trying to upload (authorize.py)"
		sys.exit(1)

	return credentials


if __name__=="__main__":
	storage = Storage(CRED_FILENAME)

	if not storage.get():
		print "Getting and saving credentials"

		# Run through the OAuth flow and retrieve authorization code
		flow = flow_from_clientsecrets(CLIENTSECRETS_LOCATION, ' '.join(SCOPES))
		flow.redirect_uri = REDIRECT_URI
		authorize_url = flow.step1_get_authorize_url()
		print 'Go to the following link in your browser: ' + authorize_url
		code = raw_input('Enter verification code: ').strip()
		credentials = flow.step2_exchange(code)

		### Storing access token and a refresh token in CRED_FILENAME
		storage.put(credentials)
	else:
		print "Credentials already available"
