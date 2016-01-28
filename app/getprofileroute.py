#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
from hashmd5 import *
import re
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
	 	                'phone':phone,
	 	                'wechat':wechat,
	 	                'qq':qq,
	 	                'hometown':hometown,
	 	                'lookcount':lookcount,
	 	                'weme':weme,
	 	                'id':id})
	return response

@getprofile_route.route("/getprofilebyid",methods=['GET','POST'])
def getprofilebyid():
	def getconstelleation(month, day):
		time = [{'sm':3, 'sd':21, 'em':4, 'ed':19},
				{'sm':4, 'sd':20, 'em':5, 'ed':20},
				{'sm':5, 'sd':21, 'em':6, 'ed':20},
				{'sm':6, 'sd':21, 'em':7, 'ed':21},
				{'sm':7, 'sd':22, 'em':8, 'ed':22},
				{'sm':8, 'sd':23, 'em':9, 'ed':22},
				{'sm':9, 'sd':23, 'em':10, 'ed':22},
				{'sm':10, 'sd':23, 'em':11, 'ed':21},
				{'sm':11, 'sd':22, 'em':12, 'ed':21},
				{'sm':12, 'sd':22, 'em':12, 'ed':31},
				{'sm':1, 'sd':1, 'em':1, 'ed':19},
				{'sm':1, 'sd':20, 'em':2, 'ed':18},
				{'sm':2, 'sd':19, 'em':3, 'ed':20}
				]
		name = [
				u'白羊座',
				u'金牛座',
				u'双子座',
				u'巨蟹座',
				u'狮子座',
				u'处女座',
				u'天秤座',
				u'天蝎座',
				u'射手座',
				u'摩羯座',
				u'摩羯座',
				u'水瓶座',
				u'双鱼座',
				]

		for idx, t in enumerate(time):
			if (t['sm'] == month and t['sd'] <= day ) or (month == t['em'] and day <= t['ed']):
				return name[idx] 
		return ''

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
			constellation = ''
			match = re.match(r'\d{4}-(\d{1,2})-(\d{1,2})', u.birthday)
			if match:
				constellation = getconstelleation(int(match.group(1)), int(match.group(2)))
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
	 	                'weme':weme,
	 	                'followflag':followflag,
	 	                'birthflag':birthflag,
	 	                'id':id,
	 	                'constellation':constellation
	 	                })
	return response
