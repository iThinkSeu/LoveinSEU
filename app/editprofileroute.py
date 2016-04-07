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
		avatarvoice = u.avatarvoices.first()
		if u != None:
			#print gender

			if gender == u"男":
				if u.gender!=u"女":
					u.gender = gender
					if avatarvoice!=None:
						avatarvoice.gender = gender
						avatarvoice.add()
					state = 'successful'
					reason = ''
				else:
					print u.gender
					state = 'fail'
					reason = '性别只能设置一次，不能更改！'

			elif gender == u"女":
				if u.gender!=u"男":
					u.gender = gender
					if avatarvoice!=None:
						avatarvoice.gender = gender
						avatarvoice.add()
					state = 'successful'
					reason = ''
				else:
					#print u.gender
					state = 'fail'
					reason = '性别只能设置一次，不能更改！'
			else:
				#print u.gender
				state = 'fail'
				reason = '请输入性别信息！'	
			
			if u.certification:
				if u.school != school or u.department != department or u.degree != degree:
					state = 'fail'
					reason = '已认证用户不能修改学校信息'

			u.name = name
			#u.gender = gender
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
		school = request.json.get('school','')
		degree = request.json.get('degree','')
		department = request.json.get('department','')
		enrollment = request.json.get('enrollment','')
		u = getuserinformation(token)
		if u != None:
			u.school = school
			u.degree = degree
			u.department = department
			u.enrollment = enrollment
			try:
				state = 'successful'
				reason = ''
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
		name = request.json.get('name','')
		gender = request.json.get('gender','')
		birthday = request.json.get('birthday','')
		phone = request.json.get('phone','')
		wechat = request.json.get('wechat',' ')
		qq = request.json.get('qq',' ')
		hometown = request.json.get('hometown',' ')
		u = getuserinformation(token)
		if u != None:
			#判断性别是否填写过了
			if gender == u"男":
				if u.gender!=u"女":
					u.gender = gender
					state = 'successful'
					reason = ''
				else:
					print u.gender
					state = 'fail'
					reason = '性别只能设置一次，不能更改！'

			elif gender == u"女":
				if u.gender!=u"男":
					u.gender = gender
					state = 'successful'
					reason = ''
				else:
					#print u.gender
					state = 'fail'
					reason = '性别只能设置一次，不能更改！'
			else:
				#print u.gender
				state = 'fail'
				reason = '请输入性别信息！'	

			u.name = name
			#u.gender = gender
			u.birthday = birthday
			u.phone = phone
			u.wechat = wechat
			u.qq = qq 
			u.hometown = hometown
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
				avatarvoice = u.avatarvoices.first()
				if avatarvoice!=None:
					avatarvoice.cardflag = cardflag
					avatarvoice.add()
				avatarvoice.cardflag = cardflag
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

