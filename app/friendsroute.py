#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
from hashmd5 import *
import string;
import datetime

friends_route = Blueprint('friends_route', __name__)

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
				L = []
				L.append(tempname)
				if tempname != None:
					state = "successful"
					reason = ''
					result = [{"id":search.id,"name":search.name,"gender":search.gender,"school":search.school} for search in L]

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
	try:
		token = request.json['token']
		u=getuserinformation(token)
 		if u != None:
			L = getranduser(token)
			if len(L)>0:
				state = 'successful'
				reason = ''
				result = [{"id":getuserbyid(recommend).id,"name":getuserbyid(recommend).name,"gender":getuserbyid(recommend).gender,"school":getuserbyid(recommend).school} for recommend in L]
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