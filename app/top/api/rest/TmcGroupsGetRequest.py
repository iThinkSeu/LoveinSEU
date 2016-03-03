'''
Created by auto_sdk on 2015.12.30
'''
from top.api.base import RestApi
class TmcGroupsGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.group_names = None
		self.page_no = None
		self.page_size = None

	def getapiname(self):
		return 'taobao.tmc.groups.get'
