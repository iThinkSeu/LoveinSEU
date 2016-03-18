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
from cache import *


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
		result = []
		if u != None:
			L = []
			temp = getuserbyid(text)
			L.append(temp)
			if temp != None:
				state = "successful"
				reason = ''
				for search in L:
					if search.id>1000:
						output = {"id":search.id,"name":search.name,"gender":search.gender,"school":search.school} 
						result.append(output)
			else:
				tempname = getuserbyname(text)
				state = "successful"
				reason = ''
				for search in tempname:
					if search.id>1000:
						output = {"id":search.id,"name":search.name,"gender":search.gender,"school":search.school} 
						result.append(output)
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

@friends_route.route('/getrecommenduser', methods=['POST'])
def get_recommend_user():
	def recommendUser(utoken,id):
		u = getuserbyid(id)
		avatarvoice = u.avatarvoices.first()
		if avatarvoice:
			return {
				'id':u.id,
				'name':u.name,
				'birthday':u.birthday,
				'gender':u.gender,
				'school':u.school,
				'degree':u.degree,
				'department':u.department,
				'hometown':u.hometown,
				'likeflag':'1' if utoken.is_likeuser(u) else '0',
				'match':'1' if(utoken.is_likeuser(u) and u.is_likeuser(utoken)) else '0', 
				'avatar':(avatarvoice.avatarurl + "_card.jpg") if avatarvoice.avatarurl!=None else '',
				'voice':avatarvoice and avatarvoice.voiceurl or '',
			}
		else:
			return None
	try:
		token = request.json['token']
		u=getuserinformation(token)
 		if u != None:
 			state = "successful"
 			reason = ''

 			if not redis_store.exists(RECOMMEND_USER_FLAG):
 				redis_store.set(RECOMMEND_USER_FLAG, "1")
 				redis_store.expire(RECOMMEND_USER_FLAG, 60*60)
				# print "create newly register users"
				new_male = User.query.filter(and_(cast(User.timestamp, Date) == date.today(), User.gender==u'男')).all()
				new_female = User.query.filter(and_(cast(User.timestamp, Date) == date.today(), User.gender==u'女')).all()
				redis_store.ltrim(RECOMMEND_USER_NEW_REGISTERED_FEMALE_KEY, 1, 0)
				redis_store.ltrim(RECOMMEND_USER_NEW_REGISTERED_MALE_KEY, 1, 0)
				for m in new_male:
					avatar_voice = m.avatarvoices.first()
					if avatar_voice and avatar_voice.cardflag != 1 and avatar_voice.disable == 0:
						redis_store.lpush(RECOMMEND_USER_NEW_REGISTERED_MALE_KEY, str(m.id))
				for f in new_female:
					avatar_voice = m.avatarvoices.first()
					if avatar_voice and avatar_voice.cardflag != 1 and avatar_voice.disable == 0:
						redis_store.lpush(RECOMMEND_USER_NEW_REGISTERED_FEMALE_KEY, str(f.id))

			if  not redis_store.hexists(RECOMMEND_USER_PREF_KEY, str(u.id)):
				liked_users = []
				like_user = u.bewhatuserlikeds.all()
				for l_u in like_user:
					avatar_voice = User.query.filter_by(id=l_u.likeid).first().avatarvoices.first()
					if avatar_voice and avatar_voice.cardflag != 1 and avatar_voice.disable == 0:
						liked_users.append(str(l_u.likeid))

				followed_users = []
				follow_user = u.followers.all()
				for f_u in follow_user:
					uu = User.query.filter_by(id=f_u.follower_id).first()
					if (u.gender == u'男' and uu.gender == u'女') or (u.gender == u'女' and uu.gender == u'男'):
						avatar_voice = uu.avatarvoices.first()
						if avatar_voice and avatar_voice.cardflag != 1 and avatar_voice.disable == 0:
							followed_users.append(str(f_u.follower_id))

				pref = {'liked':liked_users, 'followed':followed_users}
				redis_store.hset(RECOMMEND_USER_PREF_KEY, str(u.id), json.dumps(pref))

 			if (u.gender == u"男" and redis_store.exists(RECOMMEND_USER_FEMALE_KEY)) or (u.gender == u'女' and redis_store.exists(RECOMMEND_USER_MALE_KEY)):
 				is_male = u.gender == u'男'
 				total = 10
 				result = []
 				rec = []
 				new_user_len = redis_store.llen(is_male and RECOMMEND_USER_NEW_REGISTERED_FEMALE_KEY or RECOMMEND_USER_NEW_REGISTERED_MALE_KEY)
 				new_rec = random.sample(xrange(new_user_len), min(3, new_user_len)) if new_user_len else []
 				# print "fetch %s from new users" % len(new_rec)
 				for n in new_rec:
 					rec.append(redis_store.lindex(is_male and RECOMMEND_USER_NEW_REGISTERED_FEMALE_KEY or RECOMMEND_USER_NEW_REGISTERED_MALE_KEY, n))

 				if redis_store.hexists(RECOMMEND_USER_PREF_KEY, str(u.id)):
 					pref = json.loads(redis_store.hget(RECOMMEND_USER_PREF_KEY, str(u.id)))
 					like_len = len(pref['liked'])
 					like_user = random.sample(xrange(like_len), min(1, like_len)) if like_len else []
 					# print "fetch %s from like users" % len(like_user)
 					for l in like_user:
 						rec.append(pref['liked'][l])
 						# print "like id  %s" % pref['liked'][l]
 					# print rec

 					follow_len = len(pref['followed'])
 					follow_user = random.sample(xrange(follow_len), min(1, follow_len)) if follow_len else []
 					# print "fetch %s from follow users" % len(follow_user)
 					for f in follow_user:
 						rec.append(pref['followed'][f])
 					# print rec

 				length = redis_store.llen(is_male and RECOMMEND_USER_FEMALE_KEY or RECOMMEND_USER_MALE_KEY)
 				other  = random.sample(xrange(length), min(length, 10-len(rec)))
 				for o in other:
 					key = redis_store.lindex(is_male and RECOMMEND_USER_FEMALE_KEY or RECOMMEND_USER_MALE_KEY, o)
 					if not key in rec:
 						rec.append(key)

 				# print rec
 				for r in rec:
 					if int(r) == u.id :
 						continue
 					if redis_store.hexists(RECOMMEND_USER_KEY, r):
 						# print "fetch from redis"
 						result.append(json.loads(redis_store.hget(RECOMMEND_USER_KEY, r)))
 					else:
 						# print "fetch from mysql"
 						uu = recommendUser(u,int(r))
 						if uu:
 							result.append(uu)
 							redis_store.hset(RECOMMEND_USER_KEY, r, json.dumps(uu))				

			elif (u.gender == u'男' or u.gender == u'女') and ((not redis_store.exists(RECOMMEND_USER_FEMALE_KEY)) or (not redis_store.exists(RECOMMEND_USER_MALE_KEY))):  				
 				female = avatarvoice.query.filter(and_(avatarvoice.gender==u"女", avatarvoice.cardflag != 1)).filter(avatarvoice.disable == 0).all()
 				male = avatarvoice.query.filter(and_(avatarvoice.gender==u"男", avatarvoice.cardflag != 1)).filter(avatarvoice.disable == 0).all()
 				redis_store.ltrim(RECOMMEND_USER_FEMALE_KEY, 1, 0)
 				redis_store.ltrim(RECOMMEND_USER_MALE_KEY, 1, 0)
 				for f in female:
 					redis_store.lpush(RECOMMEND_USER_FEMALE_KEY,str(f.userid))
 				for m in male:
 					redis_store.lpush(RECOMMEND_USER_MALE_KEY,str(m.userid))

 				redis_store.expire(RECOMMEND_USER_FEMALE_KEY, 60*60)
 				redis_store.expire(RECOMMEND_USER_MALE_KEY, 60*60)
 				redis_store.expire(RECOMMEND_USER_KEY, 60*60)
 				redis_store.expire(RECOMMEND_USER_PREF_KEY, 60*60)
 				if u.gender == u'男':
 					length = len(female)
 					rec = random.sample(xrange(length), 10)
 					result = [ recommendUser(u, female[r].userid) for r in rec]
 				else:
 					length = len(male)
 					rec = random.sample(xrange(length), 10)
 					result = [ recommendUser(u, male[r].userid) for r in rec]

 			else:
 				state = 'fail'
 				reason = 'gender unclear'
 				result = ''	


 		else:
 			state = 'fail'
 			reason = 'invalid'
 			result = ''
 	except Exception, e:
 		print e
 		state = 'fail'
 		reason = 'exception'
  		result = ''

  	return jsonify({
  		'state':state, 
  		'reason':reason,
  		'result':result
  		})

@friends_route.route("/getrecommendusers",methods=['GET','POST'])
def getrecommenduser():
	
	def recommendUser(utoken,id):
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
			'likeflag':'1' if utoken.is_likeuser(u) else '0',
			'match':'1' if(utoken.is_likeuser(u) and u.is_likeuser(utoken)) else '0', 
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
				result = [ recommendUser(u,recommend) for recommend in L]
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
			if temp == 0 or temp == 1:
				if u2.is_likeuser(u):
					flag = "1"
				state = 'successful'
				reason = ''
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

@friends_route.route("/getlikeusernumber",methods=['POST'])
def getlikeusernumber():
	try:
		token = request.json['token']
		u=getuserinformation(token)
		likenumber = ''
		if (u is not None):
			likenumber = u.bewhatuserlikeds.count()
			state = 'successful'
			reason = ''
		else:
			state = 'fail'
			reason = 'Nouser'

	except Exception, e:
			state = 'e'
			reason = 'e'

	response = jsonify({'likenumber':likenumber,
						'state':state,
		                'reason':reason})
	return response
