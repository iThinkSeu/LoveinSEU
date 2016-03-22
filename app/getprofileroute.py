#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
from hashmd5 import *
from utility import *
getprofile_route = Blueprint('getprofile_route', __name__)

#防止数据库为空
"""define checkdbNone"""
def checkdb(dbNone):
	return dbNone if dbNone!=None else ''

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
			weme = str(u.weme) 
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
			weme = ''


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
		weme = ''

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
	 	                'phone':"",
	 	                'wechat':wechat,
	 	                'qq':qq,
	 	                'hometown':hometown,
	 	                'lookcount':lookcount,
	 	                'weme':weme,
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
			lookcount = u.lookcount if u.lookcount !=None else 0
			lookcount = str(lookcount)
			username = checkdb(u.username) 
			school = checkdb(u.school) 				
			degree = checkdb(u.degree)
			department = checkdb(u.department)
			enrollment = checkdb(u.enrollment)
			name = checkdb(u.name)
			gender = checkdb(u.gender)
			birthday = checkdb(u.birthday)
			hobby = checkdb(u.hobby)
			preference = checkdb(u.preference) 
			phone = checkdb(u.phone)
			wechat = checkdb(u.wechat)
			qq = checkdb(u.qq)
			hometown = checkdb(u.hometown)
			id = checkdb(u.id)
			weme = str(u.weme)
			#好友关系
			uFollowList = u2.followeds.all()
			FollowuList = u2.followers.all()
			ufollowFlag = id in [y.followed_id for y in uFollowList]
			followuFlag = id in [x.follower_id for x in FollowuList]
			if ufollowFlag==False and followuFlag == False:
				followflag = '0'
			elif ufollowFlag and followuFlag == False:
				followflag = '1'
			elif followuFlag and ufollowFlag == False:
				followflag = '2'
			elif ufollowFlag == True and followuFlag == True:
				followflag = '3'
			else:
				followflag = '4'
			#比较大小
			if u2.birthday < u.birthday:
				birthflag = '1'
			elif u2.birthday > u.birthday:
				birthflag = '-1'
			else:
				birthflag = '0' 
			
			constellation = getconstelleation(u.birthday)
			certification = checkdb(u.certification)

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
			weme = ''
			followflag = ''
			birthflag = '' 
			certification = ''

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
		weme = ''
		followflag = ''
		birthflag = '' 
		certification = ''

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
	 	                'phone':"",
	 	                'wechat':wechat,
	 	                'qq':qq,
	 	                'hometown':hometown,
	 	                'lookcount':lookcount,
	 	                'weme':weme,
	 	                'followflag':followflag,
	 	                'birthflag':birthflag,
	 	                'id':id,
	 	                'certification':certification,
	 	                'constellation':constellation
	 	                })
	return response
