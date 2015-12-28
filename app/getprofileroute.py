#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
from hashmd5 import *
getprofile_route = Blueprint('getprofile_route', __name__)

@getprofile_route.route("/getprofile",methods=['GET','POST'])
def getprofile():
	try:
		token = request.json['token']
		u=getuserinformation(token)
 		if u!=None:
			state = 'successful'
			reason = ''
			username = u.username if u.username!=None else ''
			token = u.token if u.token!=None else ''    
			school = u.school if u.school!=None else '' 				
			degree = u.degree if u.degree!=None else ''
			department = u.department if u.department!=None else ''
			enrollment = u.enrollment if u.enrollment!=None else ''
			name = u.name if u.name!=None else ''
			gender = u.gender if u.gender!=None else ''
			birthday = u.birthday if u.birthday!=None else ''
			hobby = u.hobby if u.hobby!=None else ''
			preference = u.preference if u.preference!=None else '' 
			phone = u.phone if u.phone!=None else ''
			wechat = u.wechat if u.wechat != None else ''
			qq = u.qq if u.qq != None else ''
			hometown = u.hometown if u.hometown != None else ''
			id = u.id if u.id!=None else ''
			lookcount = u.lookcount if u.lookcount !=None else 0

			lookcount = str(lookcount)#所有的返回都转化成string

		else:
			state = 'fail'
			reason = '用户不存在'
			username = 'Nouser'
			token=''
			school=''
			degree=''
			department = ''
			enrollment = ''
			name = ''
			gender = ''
			birthday = ''
			hobby = ''
			preference = ''
			phone = ''
			wechat = ''
			qq =''
			hometown = ''
			id = ''
			qianshoudongda =''
			lookcount = ''



	except Exception, e:
		state = 'fail'
		reason = '异常'	
		username='e'
		token=''
		school=''
		degree=''
		department = ''
		enrollment = ''
		name = ''
		gender = ''
		birthday = ''
		hobby = ''
		preference = ''
		phone = ''
		wechat = ''
		qq = ''
		hometown = ''
		id = ''
		lookcount = ''
		

	response = jsonify({'username':username,
						'token':token,
						'state':state,
						'reason':reason,
	 	                'school':school,
	 	                'degree':degree,
	 	                'department':department,
	 	                'enrollment':enrollment,
	 	                'name':name,
	 	                'gender':gender,
	 	                'birthday':birthday,
	 	                'preference':preference,
	 	                'hobby':hobby,
	 	                'phone':phone,
	 	                'wechat':wechat,
	 	                'qq':qq,
	 	                'hometown':hometown,
	 	                'lookcount':lookcount,
	 	                'id':id})
	return response

@getprofile_route.route("/getprofilebyid",methods=['GET','POST'])
def getprofilebyid():
	try:
		id = request.json['id']
		token = request.json['token']
		u2=getuserinformation(token)
		u=getuserbyid(id)
 		if u!=None and u2!=None:
			state = 'successful'
			reason = ''
			#更新好友查看次数计数器
			lookcount = u.lookcount if u.lookcount !=None else 0
			u.lookcount = lookcount + 1
			u.add()

			lookcount = str(lookcount)
			username = u.username if u.username!=None else '' 
			school = u.school if u.school!=None else '' 				
			degree = u.degree if u.degree!=None else ''
			department = u.department if u.department!=None else ''
			enrollment = u.enrollment if u.enrollment!=None else ''
			name = u.name if u.name!=None else ''
			gender = u.gender if u.gender!=None else ''
			birthday = u.birthday if u.birthday!=None else ''
			hobby = u.hobby if u.hobby!=None else ''
			preference = u.preference if u.preference!=None else '' 
			phone = u.phone if u.phone!=None else ''
			wechat = u.wechat if u.wechat != None else ''
			qq = u.qq if u.qq !=None else ''
			hometown = u.hometown if u.hometown != None else ''
			id = u.id if u.id!=None else ''

		else:
			state = 'fail'
			reason = '用户不存在'
			username = 'Nouser'
			school=''
			degree=''
			department = ''
			enrollment = ''
			name = ''
			gender = ''
			birthday = ''
			hobby = ''
			preference = ''
			phone = ''
			wechat = ''
			qq = ''
			hometown = ''
			id = ''
			lookcount = ''


	except Exception, e:
		print e
		state = 'fail'
		reason = '异常'	
		username='e'
		school=''
		degree=''
		department = ''
		enrollment = ''
		name = ''
		gender = ''
		birthday = ''
		hobby = ''
		preference = ''
		phone = ''
		wechat = ''
		qq = ''
		hometown = ''
		id = ''
		lookcount = ''



	response = jsonify({'username':username,
						'state':state,
						'reason':reason,
	 	                'school':school,
	 	                'degree':degree,
	 	                'department':department,
	 	                'enrollment':enrollment,
	 	                'name':name,
	 	                'gender':gender,
	 	                'birthday':birthday,
	 	                'preference':preference,
	 	                'hobby':hobby,
	 	                'phone':phone,
	 	                'wechat':wechat,
	 	                'qq':qq,
	 	                'hometown':hometown,
	 	                'lookcount':lookcount,
	 	                'id':id})
	return response
