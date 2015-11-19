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
			qianshoudongda = u.qianshoudongda if u.qianshoudongda!=None else ''
			autumn1 = u.autumn1 if u.autumn1!=None else ''
			autumn2 = u.autumn2 if u.autumn2!=None else ''
			autumn3 = u.autumn3 if u.autumn3!=None else ''
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
			autumn1 = ''
			autumn2=''
			autumn3 = ''


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
		qianshoudongda=''
		autumn1 = ''
		autumn2 = ''
		autumn3 = ''

		

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
	 	                'id':id})
	return response

@getprofile_route.route("/getprofilebyid",methods=['GET','POST'])
def getprofilebyid():
	try:
		id = request.json['id']
		u=getuserbyid(id)
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
			qq = u.qq if u.qq !=None else ''
			hometown = u.hometown if u.hometown != None else ''
			id = u.id if u.id!=None else ''
			qianshoudongda = u.qianshoudongda if u.qianshoudongda!=None else ''
			autumn1 = u.autumn1 if u.autumn1!=None else ''
			autumn2 = u.autumn2 if u.autumn2!=None else ''
			autumn3 = u.autumn3 if u.autumn3!=None else ''
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
			qq = ''
			hometown = ''
			id = ''
			qianshoudongda =''
			autumn1 = ''
			autumn2=''
			autumn3 = ''


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
		qianshoudongda=''
		autumn1 = ''
		autumn2 = ''
		autumn3 = ''

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
	 	                'id':id})
	return response
