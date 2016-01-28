#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
from hashmd5 import *
import string;
import datetime
from sqlalchemy import Date, cast
from datetime import date
import re

friends_route = Blueprint('friends_route', __name__)

@friends_route.route("/visit", methods=['POST'])
def visit():
	try:
		token = request.json['token']
		id = request.json['userid']
		u = getuserinformation(token)
		u1 = getuserbyid(id)
		if (u is not None) and (u1 is not None) and (u.id != u1.id):
			lookcount = u1.lookcount if u1.lookcount !=None else 0
			u1.lookcount = lookcount + 1
			u1.add()
			res = u.visit(u1)
			if res == 0:
				state = 'successful'
				reason = ''
			else:
				state = 'fail'
				reason = 'exception'
		else:
			state = 'fail'
			reason = 'exception'
	except Exception, e:
		state = 'fail'
		reason = 'exception'
	response = jsonify({'state':state, 'reason':reason})
	return response

@friends_route.route('/visitinfo', methods=['POST'])
def visitinfo():
	try:
		token = request.json['token']
		id = request.json['userid']
		u = getuserinformation(token)
		u1 = getuserbyid(id)
		if (u is not None) and (u1 is not None):
			lookcount = u1.lookcount if u1.lookcount !=None else 0
			state = 'successful'
			reason = ''
			result = {'total':lookcount, 'today':u1.visitors.filter(cast(Visit.timestamp, Date) == date.today()).count()}

	except Exception, e:
		state = 'fail'
		reason = 'exception'
		result = ''

	return jsonify({'state':state, 'reason':reason, 'result':result})

@friends_route.route("/follow",methods=['GET','POST'])
def follow():
	try:
		token = request.json['token']
		id = request.json['id']
		u=getuserinformation(token)
		u2=User.query.filter_by(id=id).first()
		if (u is not None) and (u2 is not None):
			temp = u.follow(u2);
			if temp == 0:
				state = 'successful'
				reason = ''
			elif temp==1:
				state = 'fail'
				reason = 'already follow';
			else:
				state='fail'
				reason='e'
		else:
			state = 'fail'
			reason = 'Nouser'

	except Exception, e:
			state = 'e'
			reason = 'e'

	response = jsonify({'state':state,
		                'reason':reason})
	return response

@friends_route.route("/unfollow",methods=['GET','POST'])
def unfollow():
	try:
		token = request.json['token']
		id = request.json['id']
		u=getuserinformation(token)
		u2=User.query.filter_by(id=id).first()
		if (u is not None) and (u2 is not None):
			temp = u.unfollow(u2);
			if temp == 0:
				state = 'successful'
				reason = ''
			elif temp ==1:
				state = 'fail'
				reason = 'already unfollow'
			else:
				state='fail'
				reason = 'e';
		else:
			state = 'fail'
			reason = 'Nouser'

	except Exception, e:
			print e
			state = 'e'
			reason = 'e'

	response = jsonify({'state':state,
		                'reason':reason})
	return response

# show the users that follow me or I follow
@friends_route.route("/followview", methods=['POST'])
def followers():
	try:
		token = request.json['token']
		u=getuserinformation(token)
		page = request.json['page']
		#print page
		x=string.atoi(page)
		#print x
		direct = request.json.get('direction', 'followers');
		#print direct 
		if u is not None:
			if direct == 'followers':
				pageitems = u.followers.paginate(x, per_page=10, error_out=False)
				followview = [{'id':item.follower.id,'name':item.follower.name if item.follower.name!=None else '','gender':item.follower.gender if item.follower.gender!=None else '','school':item.follower.school if item.follower.school!=None else '','timestamp':item.timestamp} for item in pageitems.items]
			else:
				pageitems = u.followeds.paginate(x, per_page=10, error_out=False)
				followview = [{'id':item.followed.id, 'name':item.followed.name if item.followed.name!=None else '','gender':item.followed.gender if item.followed.gender!=None else '','school':item.followed.school if item.followed.school!=None else '','timestamp':item.timestamp} for item in pageitems.items]
			#print followview
			state = 'successful'
			reason = ''
		else:
			state = 'fail'
			followview = {};
			reason = 'User not exist'

	except Exception ,e:
		print e
		state = 'fail'
		followview = {};
		reason = 'e'
		direct=''

	response = jsonify({'state':state,
						'reason':reason,
						'result': followview})
	return response;

@friends_route.route("/searchuser",methods = ['GET','POST'])
def searchuser():
	try:
		token = request.json['token']
		text = request.json['text']
		u = getuserinformation(token)
		if u != None:
			L = []
			temp = getuserbyid(text)
			L.append(temp)
			if temp != None:
				state = "successful"
				reason = ''
				result = [{"id":search.id,"name":search.name,"gender":search.gender,"school":search.school} for search in L]
			else:
				tempname = getuserbyname(text)
				state = "successful"
				reason = ''
				result = [{"id":search.id,"name":search.name,"gender":search.gender,"school":search.school} for search in tempname]
		else:
			state = 'fail'
			reason = 'no user'
			result = [];

	except Exception, e:
		print e
		state = 'fail'
		reason = 'exception'
		result = []

	response = jsonify({'state':state,
						'reason':reason,
						'result':result})
	return response


@friends_route.route("/getrecommenduser",methods=['GET','POST'])
def getrecommenduser():
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

	def recommendUser(id):
		u = getuserbyid(id)
		avatarvoice = u.avatarvoices.first()
		constellation = ''
		match = re.match(r'\d{4}-(\d{1,2})-(\d{1,2})', u.birthday)
		if match:
			constellation = getconstelleation(int(match.group(1)), int(match.group(2)))

		return {
			'id':u.id,
			'name':u.name,
			'birthday':u.birthday,
			'gender':u.gender,
			'school':u.school,
			'degree':u.degree,
			'department':u.department,
			'hometown':u.hometown,
			'avatar':avatarvoice.avatarurl if avatarvoice.avatarurl!=None else '',
			'voice':avatarvoice and avatarvoice.voiceurl or '',
			'constellation':constellation
		}
	try:
		token = request.json['token']
		u=getuserinformation(token)
 		if u != None:
			L = getrandcard(u)
			if len(L)>0:
				state = 'successful'
				reason = ''
				result = [ recommendUser(recommend) for recommend in L]
				response = jsonify({'state':state,
									'reason':reason,
									'result':result
				 	                })
			else:
				state = 'fail'
				reason = 'no gender'
				response = jsonify({'state':state,
									'reason':reason,
									'result':[]
									})
		else:
			state = 'fail'
			reason = 'Nouser'
			response = jsonify({'state':state,
								'reason':reason,
								'result':[]
								})

	except Exception, e:
		print e
		state = 'fail'
		reason = 'e'	
		response = jsonify({'state':state,
							'reason':reason,
							'result':[]
							})
	return response