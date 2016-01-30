#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
import models 
import string
from datetime import *

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

@certification_route.route("/getallcertification",methods=['POST'])
def getallcertification():
	try:
		token = request.json['token']
		page = request.json.get('page','1')
		x=string.atoi(str(page))
		u=getuserinformation(token)
		pages = 0
		if u!=None and u.username == 'administrator':
			pagetemp = schoolcertification.query.order_by(models.schoolcertification.timestamp.desc()).paginate(x, per_page=10, error_out=False)
			certlist = pagetemp.items
			pages = pagetemp.pages
			result = []
			state = 'successful'
			reason = ''
			for cert in certlist:
				output = {	'id':cert.id,
							'userid':cert.userid,
							'name':checkdb(cert.name),
							'school':checkdb(cert.school),
							'studentid':checkdb(cert.studentID),
							'location':checkdb(cert.location),
							'pictureurl':checkdb(cert.pictureurl),
							'location':checkdb(cert.location),
							'checkflag':checkdb(cert.checkflag),
							'timestamp':checkdb(cert.timestamp)
						 }
				result.append(output)
		else:
			state = 'fail'
			reason = '非法用户'
			result = []
	except Exception, e:
		print e
		state = 'fail'
		reason = '异常'
		result = []

	response = jsonify({'result':result,
						'state':state,
						'reason':reason,
						'pages':pages})
	return response

@certification_route.route("/setpasscertification",methods=['POST'])
def setpasscertification():
	try:
		token = request.json['token']
		certlist = request.json['certlist']
		u = getuserinformation(token)	
		if u != None and u.username == 'administrator':	
			state = 'successful'
			reason = ''
			for certid in certlist:
				cert = schoolcertification.query.filter_by(id = certid).first()
				if cert != None:
					cert.checkflag = True
					cert.checktime = datetime.now()
					cert.checkresult = True
					cert.add()
					upass = User.query.filter_by(id = cert.userid).first()
					upass.certification = True
					upass.addpwd()
		else:
			state = 'fail'
			reason = '非法用户'
			result = ''
	except Exception, e:
		print e
		result = ''
		state = 'fail'
		reason = 'exception'
	response = jsonify({'state':state,
						'reason':reason})
	return response
@certification_route.route("/setnopasscertification",methods=['POST'])
def setnopasscertification():
	try:
		token = request.json['token']
		certlist = request.json['certlist']
		u = getuserinformation(token)	
		if u != None and u.username == 'administrator':	
			state = 'successful'
			reason = ''
			for certid in certlist:
				cert = schoolcertification.query.filter_by(id = certid).first()
				if cert != None:
					cert.checkflag = True
					cert.checktime = datetime.now()
					cert.checkresult = False
					cert.add()
					upass = User.query.filter_by(id = cert.userid).first()
					upass.certification = False
					upass.addpwd()
		else:
			state = 'fail'
			reason = '非法用户'
			result = ''
	except Exception, e:
		print e
		result = ''
		state = 'fail'
		reason = 'exception'
	response = jsonify({'state':state,
						'reason':reason})
	return response