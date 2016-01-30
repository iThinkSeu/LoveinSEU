#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
import string

certification_route = Blueprint('certification_route', __name__)

#防止数据库为空
"""define checkdbNone"""
def checkdb(dbNone):
	return dbNone if dbNone!=None else ''

@certification_route.route("/publishcertification",methods=['POST'])
def publishcertification():
	try:
		token = request.json['token']
		studentID = request.json.get('studentid','')
		location = request.json.get('location','')
		u = getuserinformation(token)
		if u is not None:
			state = "successful"
			reason = ""
			cert = schoolcertification(userid = u.id,name =u.name,school =u.school,studentID = studentID, location = location)
			cert.add()
			id = cert.id
		else:
			state = 'fail'
			reason = 'no user'
			id = ''
	except Exception, e:	
		print e
		state = 'fail'
		reason = 'exception'
		id = ''

	response = jsonify({'certificationid':id,
						'state':state,
						'reason':reason})
	return response



