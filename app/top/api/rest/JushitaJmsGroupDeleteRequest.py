'''
Created by auto_sdk on 2016.01.13
'''
from top.api.base import RestApi
class JushitaJmsGroupDeleteRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.group_name = None
		self.nicks = None
		self.user_platform = None

	def getapiname(self):
		return 'taobao.jushita.jms.group.delete'
