'''
Created by auto_sdk on 2015.12.04
'''
from top.api.base import RestApi
class TmcUserGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.fields = None
		self.nick = None
		self.user_platform = None

	def getapiname(self):
		return 'taobao.tmc.user.get'
