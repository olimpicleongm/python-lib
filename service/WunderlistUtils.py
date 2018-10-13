'''
NOTE
images for tasks can be attached through multipart upload on Amazon
'''

import urllib2, json

API_ENDPOINT = 'https://a.wunderlist.com/api/v1'

class WunderlistAPI:
	def __init__(self, client_id, access_token):
		self.client_id = client_id
		self.access_token = access_token

	def fetchFromAPI(self, fetch_url):
		uri = fetch_url % (self.access_token, self.client_id)
		response = urllib2.urlopen(uri).read()
		result = json.loads(response)
		return result

	def pushToAPI(self, push_url, payload, patch=False):
		headers = {'X-Access-Token': self.access_token, 'X-Client-ID': self.client_id, 'Content-Type': 'application/json'}
		request = urllib2.Request(push_url, json.dumps(payload), headers)
		if patch:
			request.get_method = lambda: 'PATCH'
		return json.loads(urllib2.urlopen(request).read())

	def getLists(self):
		return self.fetchFromAPI(API_ENDPOINT + '/lists?access_token=%s&client_id=%s')

	def createTask(self, task):
		return self.pushToAPI(API_ENDPOINT + '/tasks', task)

	def updateTask(self, task):
		task_id = str(task['task_id'])
		del(task['task_id'])
		return self.pushToAPI(API_ENDPOINT + '/tasks/' + task_id, task, True)

	def createNoteForTask(self, note):
		return self.pushToAPI(API_ENDPOINT + '/notes', note)

	def createReminderForTask(self, reminder):
		return self.pushToAPI(API_ENDPOINT + '/reminders', reminder)