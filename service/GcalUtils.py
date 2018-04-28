'''
REQUIREMENTS
pip install google-api-python-client
easy_install oauth2client

NOTE
images for events can be attached through Google Drive
'''

from httplib2 import Http

from apiclient.discovery import build
from oauth2client import file, client, tools

class GcalAPI:
	def __init__(self, client_secrets, storage_path):
		self.client_secrets = client_secrets
		self.storage_path = storage_path
		self.client = self.authorize()

	def authorize(self):
		SCOPES = 'https://www.googleapis.com/auth/calendar'
		store = file.Storage(self.storage_path)
		creds = store.get()
		if not creds or creds.invalid:
			flow = client.flow_from_clientsecrets(self.client_secrets, SCOPES)
			creds = tools.run_flow(flow, store)
		return build('calendar', 'v3', http=creds.authorize(Http()))

	def getCalendarsList(self):
		return self.client.calendarList().list().execute()

	def insertEvent(self, calendar_id, event):
		return self.client.events().insert(calendarId=calendar_id, body=event).execute()