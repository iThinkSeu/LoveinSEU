#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
from hashmd5 import *
import string;
import datetime
from sqlalchemy import Date, cast
from datetime import date
from push import *


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
				notify_follow_to_user(u2, u)
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
	
	def recommendUser(id):
		u = getuserbyid(id)
		avatarvoice = u.avatarvoices.first()

		return {
			'id':u.id,
			'name':u.name,
			'birthday':u.birthday,
			'gender':u.gender,
			'school':u.school,
			'degree':u.degree,
			'department':u.department,
			'hometown':u.hometown,
			'avatar':(avatarvoice.avatarurl + "_card.jpg") if avatarvoice.avatarurl!=None else '',
			'voice':avatarvoice and avatarvoice.voiceurl or '',
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

@friends_route.route("/likeusercard",methods=['POST'])
def likeusercard():
	try:
		token = request.json['token']
		userid = request.json['userid']
		u=getuserinformation(token)
		u2=User.query.filter_by(id=userid).first()
		flag = "0"
		if (u is not None) and (u2 is not None):
			temp = u.likeuser(u2)
			if temp == 0:
				if u2.is_likeuser(u):
					flag = "1"
				state = 'successful'
				reason = ''
			elif temp==1:
				if u2.is_likeuser(u):
					flag = "1"
				state = 'fail'
				reason = 'already like';
			else:
				state='fail'
				reason='e'
		else:
			state = 'fail'
			reason = 'Nouser'

	except Exception, e:
			state = 'e'
			reason = 'e'

	response = jsonify({'flag':flag,
						'state':state,
		                'reason':reason})
	return response

@friends_route.route("/unlikeusercard",methods=['POST'])
def unlikeusercard():
	try:
		token = request.json['token']
		userid = request.json['userid']
		u=getuserinformation(token)
		u2=User.query.filter_by(id=userid).first()
		if (u is not None) and (u2 is not None):
			temp = u.unlikeuser(u2)
			if temp == 0:
				state = 'successful'
				reason = ''
			elif temp==1:
				state = 'fail'
				reason = 'already unlike';
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