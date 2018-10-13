import httplib2, json
try:
	from urllib.parse import urlencode
except ImportError:
	from urllib import urlencode

class IpInfoAPI:
	CURL_HEADERS = {'User-Agent': 'curl/7.43.0'}

	@classmethod
	def getIp(IpInfoAPI):
		result = None
		response = httplib2.Http().request('http://ifconfig.me/all.json', 'GET', headers=IpInfoAPI.CURL_HEADERS)
		if response[0].status == 200:
			result = json.loads(response[1])['ip_addr']
		return result

	@classmethod
	def getIpInfo(IpInfoAPI, ip_addr):
		headers = IpInfoAPI.CURL_HEADERS
		headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
		data = {'ip': ip_addr}
		result = None
		response = httplib2.Http().request('https://iplocation.com', 'POST', headers=headers, body=urlencode(data))
		if response[0].status == 200:
			result = json.loads(response[1])
		return result