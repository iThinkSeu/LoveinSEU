'''
Created by auto_sdk on 2015.12.17
'''
from top.api.base import RestApi
class TmcMessagesConfirmRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.f_message_ids = None
		self.group_name = None
		self.s_message_ids = None

	def getapiname(self):
		return 'taobao.tmc.messages.confirm'
