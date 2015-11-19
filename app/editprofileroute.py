#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
from hashmd5 import *
editprofile_route = Blueprint('editprofile_route', __name__)

@editprofile_route.route("/editprofile/editschoolinformation",methods=['POST'])
def editschoolinformation():
	try:
		print 'hello'
		token = request.json[u'token']
		print token
		school = request.json['school']
		degree = request.json['degree']
		department = request.json['department']
		enrollment = request.json['enrollment']

		writestate = editschooldb(token,school,degree,department,enrollment)
		if not writestate:
			state = 'successful'
			reason = ''

		elif writestate == 2:
			state = 'fail'
			reason = 'no user'
		else:
			state = 'fail'
			reason = 'db error'

	except Exception, e:
		print e
		state = 'fail'
		reason ='异常'
	

	response = jsonify({'state':state,
		                'reason':reason})
	return response

@editprofile_route.route("/editprofile/editpersonalinformation",methods=['POST'])
def editpersonalinformation():
	try:
		
		token = request.json[u'token']
		name = request.json['name']
		gender = request.json['gender']
		birthday = request.json['birthday']
		phone = request.json['phone']
		wechat = request.json.get('wechat',' ')
		qq = request.json.get('qq',' ')
		hometown = request.json.get('hometown',' ')

		writestate = editpersonaldb(token,name,gender,birthday,phone,wechat,qq,hometown)
		if not writestate:
			state = 'successful'
			reason = ''
		elif writestate == 2:
			state = 'fail'
			reason = 'no user'
		else:
			state = 'fail'
			reason = 'db error'

	except Exception, e:
		print e
		state = 'fail'
		reason ='异常'

	response = jsonify({'state':state,
		                'reason':reason})
	return response

@editprofile_route.route("/editprofile/editpreferinformation",methods=['POST'])
def editpreferinformation():
	try:
		token = request.json['token']
		hobby = request.json['hobby']
		preference = request.json['preference']
		writestate = editpreferdb(token,hobby,preference)
		if not writestate:
			state = 'successful'
			reason = ''
		elif writestate == 2:
			state = 'fail'
			reason = 'no user'
		else:
			state = 'fail'
			reason = 'db error'

	except Exception, e:
		print e
		state = 'fail'
		reason ='异常'
	

	response = jsonify({'state':state,
		                'reason':reason})
	return response