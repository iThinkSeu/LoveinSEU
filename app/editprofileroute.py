#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
from hashmd5 import *
import string 
editprofile_route = Blueprint('editprofile_route', __name__)


@editprofile_route.route("/editprofileinfo", methods = ['POST'])
def editprofileinfo():
	try:
		token = request.json['token']
		school = request.json.get('school', '')
		degree = request.json.get('degree', '')
		department = request.json.get('department', '')
		enrollment = request.json.get('enrollment', '')
		name = request.json.get('name', '')
		gender = request.json.get('gender', '')
		birthday = request.json.get('birthday', '')
		phone = request.json.get('phone', '')
		wechat = request.json.get('wechat','')
		qq = request.json.get('qq','')
		hometown = request.json.get('hometown','')
		hobby = request.json.get('hobby', '')
		preference = request.json.get('preference','')
		u = getuserinformation(token)
		if u != None:
			state = 'successful'
			reason = ''
			u.name = name
			u.gender = gender
			u.birthday = birthday
			u.phone = phone
			u.wechat = wechat
			u.qq = qq 
			u.hometown = hometown
			u.school = school
			u.degree = degree
			u.department = department
			u.enrollment = enrollment
			u.hobby = hobby
			u.preference = preference
			try:
				db.session.add(u)
				db.session.commit()
				db.session.close()	
			except Exception, e:
				state = 'fail'
				reason = 'exception'
				db.session.rollback() 
		else:
			state = 'fail'
			reason = 'invalid access'
	except Exception, e:
		state = 'fail'
		reason = 'exception'

	return jsonify({'state':state, 'reason':reason})



@editprofile_route.route("/editprofile/editschoolinformation",methods=['POST'])
def editschoolinformation():
	try:
		token = request.json['token']
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
		
		token = request.json['token']
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

@editprofile_route.route("/editprofile/editcardsetting",methods=['POST'])
def editcardsetting():
	try:
		token = request.json['token']
		tmpcardflag = str(request.json['cardflag'])
		u = getuserinformation(token)
		if u !=None:
			if tmpcardflag in ['0','1']:
				cardflag = string.atoi(tmpcardflag)
				u.cardflag = cardflag
				u.addpwd()
				state = 'successful'
				reason = ''
			else:
				state = 'fail'
				reason = 'wrong cardflag'
	except Exception, e:
		print e
		state = 'fail'
		reason ='异常'
	response = jsonify({'state':state,
						'reason':reason})
	return response

