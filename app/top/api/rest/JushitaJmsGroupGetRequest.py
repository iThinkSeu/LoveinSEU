'''
Created by auto_sdk on 2016.01.13
'''
from top.api.base import RestApi
class JushitaJmsGroupGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.group_names = None
		self.page_no = None
		self.page_size = None

	def getapiname(self):
		return 'taobao.jushita.jms.group.get'
