#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
import models 
import string
from sqlalchemy import Date, cast
import random

report_route = Blueprint('report_route', __name__)

#防止数据库为空
"""define checkdbNone"""
def checkdb(dbNone):
	return dbNone if dbNone!=None else ''

@report_route.route("/publishreport",methods=['POST'])
def publishreport():
	try:
		token = request.json['token']
		body = request.json.get('body','')
		type = request.json.get('type','')
		typeid_string = str(request.json.get('typeid',''))
		typeid = string.atoi(typeid_string)
		u = getuserinformation(token)
		if u is not None:
			if(type in ['post','comment','activity','user']):
				body = body.encode('UTF-8')
				tmpreport = report(body = body,type = type,typeid = typeid)
				u.publishreport(tmpreport)
				state = 'successful'
				reason = ''
			else:
				state = 'fail'
				reason = 'no this type report'				
		else:
			state = 'fail'
			reason = 'no user'
	except Exception, e:	
		print e
		state = 'fail'
		reason = 'exception'

	response = jsonify({'state':state,
						'reason':reason})
	return response

