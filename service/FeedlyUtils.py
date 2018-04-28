'''
NOTE
refresh token at Feedly (cloud scope) every 30 days - free account limitation
'''

import httplib2, json

API_ENDPOINT  = 'https://cloud.feedly.com/v3/subscriptions'

class FeedlyAPI:
	def __init__(self, access_token, rss_max_count=100): # free account limitation
		self.access_token = access_token
		self.rss_max_count = rss_max_count
		self.headers = {'Authorization': 'OAuth ' + self.access_token, 'Content-Type': 'application/json'}
		self.client = httplib2.Http()

	def getSubscriptions(self):
		response = self.client.request(API_ENDPOINT, 'GET', headers=self.headers) # export opml https://feedly.com/v3/opml?feedlyToken=...
		if response[0].status == 200:
			return json.loads(response[1]) # also check {"errorCode":,"message":""}
		else:
			return []

	def subscribe(self, items):
		result = []
		for i in items:
			response = self.client.request(API_ENDPOINT, 'POST', headers=self.headers, body=json.dumps(i))
			if response[0].status == 200:
				result.append(response)
		if len(result) == len(items): # everything is good
			return True
		else:
			return False

	def unsubscribe(self, items):
		ids = [i['id'] for i in items]
		response = self.client.request(API_ENDPOINT + '/.mdelete', 'DELETE', headers=self.headers, body=json.dumps(ids))
		if response[0].status == 200:
			return True
		else:
			return False