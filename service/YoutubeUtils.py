'''
REQUIREMENTS
pip install google-api-python-client
easy_install oauth2client
'''

import httplib2

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

FEED_URI = 'feed/https://www.youtube.com/feeds/videos.xml?channel_id=%s'
PLAYLIST_URL = 'https://www.youtube.com/playlist?list=%s'
WATCH_URI = 'https://www.youtube.com/watch?v=%s'

class YoutubeAPI:
	def __init__(self, args, client_secrets, storage_path):
		self.args = args
		self.client_secrets = client_secrets
		self.storage_path = storage_path
		self.client = self.authorize()

	def authorize(self):
		### from youtube api samples https://github.com/youtube/api-samples ###
		# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
		# the OAuth 2.0 information for this application, including its client_id and
		# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
		# the {{ Google Cloud Console }} at
		# {{ https://cloud.google.com/console }}.
		# Please ensure that you have enabled the YouTube Data API for your project.
		# For more information about using OAuth2 to access the YouTube Data API, see:
		#   https://developers.google.com/youtube/v3/guides/authentication
		# For more information about the client_secrets.json file format, see:
		#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
		#CLIENT_SECRETS_FILE = "client_secrets.json"
		# This OAuth 2.0 access scope allows for full read/write access to the
		# authenticated user's account.
		YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
		YOUTUBE_API_SERVICE_NAME = "youtube"
		YOUTUBE_API_VERSION = "v3"
		# This variable defines a message to display if the CLIENT_SECRETS_FILE is
		# missing.
		MISSING_CLIENT_SECRETS_MESSAGE = "client secrets file is required"

		flow = flow_from_clientsecrets(self.client_secrets, scope=YOUTUBE_READ_WRITE_SCOPE, message=MISSING_CLIENT_SECRETS_MESSAGE)

		storage = Storage(self.storage_path)
		credentials = storage.get()

		if credentials is None or credentials.invalid:
			credentials = run_flow(flow, storage, self.args)

		return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=credentials.authorize(httplib2.Http()))

	def getSubscriptions(self, channel_id):
		subscriptions = []
		#total = 0

		counter   = 1
		max_count = 5

		next_page = ''
		while True:
			if len(next_page) == 0:
				response = self.client.subscriptions().list(part='snippet', channelId=channel_id, maxResults=50).execute()
			else:
				response = self.client.subscriptions().list(part='snippet', channelId=channel_id, maxResults=50, pageToken=next_page).execute()

			for item in response['items']:
				if item['kind'] == 'youtube#subscription': #'youtube#channel'
					subscriptions.append({'id': FEED_URI % item['snippet']['resourceId']['channelId'], 'title': item['snippet']['title']})

			#if total == 0:
			#	total = int(response['pageInfo']['totalResults'])

			try:
				next_page = response['nextPageToken']
			except KeyError:
				break

			if counter >= max_count: # dummy break
				break

			counter += 1

		#if len(subscriptions) != total: # patrial subscriptions download, blocked channels are not returned
		#	return []

		return subscriptions

	def getPlaylists(self, channel_id):
		playlists = []
		#total = 0

		counter   = 1
		max_count = 5

		next_page = ''
		while True:
			if len(next_page) == 0:
				response = self.client.playlists().list(part='snippet', channelId=channel_id, maxResults=50).execute()
			else:
				response = self.client.playlists().list(part='snippet', channelId=channel_id, maxResults=50, pageToken=next_page).execute()

			for item in response['items']:
				if item['kind'] == 'youtube#playlist':
					playlists.append({'id': item['id'], 'title': item['snippet']['title']})

			#if total == 0:
			#	total = int(response['pageInfo']['totalResults'])

			try:
				next_page = response['nextPageToken']
			except KeyError:
				break

			if counter >= max_count: # dummy break
				break

			counter += 1

		#if len(playlists) != total: # patrial playlists download, blocked channels are not returned
		#	return []

		return playlists

	def getPlaylistItems(self, playlist_id):
		videos = []
		#total = 0

		counter   = 1
		max_count = 5

		next_page = ''
		while True:
			if len(next_page) == 0:
				response = self.client.playlistItems().list(part='snippet', playlistId=playlist_id, maxResults=50).execute()
			else:
				response = self.client.playlistItems().list(part='snippet', playlistId=playlist_id, maxResults=50, pageToken=next_page).execute()

			for item in response['items']:
				if item['kind'] == 'youtube#playlistItem':
					videos.append({'id': item['snippet']['resourceId']['videoId'], 'title': item['snippet']['title']})

			#if total == 0:
			#	total = int(response['pageInfo']['totalResults'])

			try:
				next_page = response['nextPageToken']
			except KeyError:
				break

			if counter >= max_count: # dummy break
				break

			counter += 1

		#if len(videos) != total: # patrial videos download, blocked channels are not returned
		#	return []

		return videos