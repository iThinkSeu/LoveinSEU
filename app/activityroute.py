#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
import models 
from hashmd5 import *
import string
from sqlalchemy import Date, cast

activity_route = Blueprint('activity_route', __name__)

@activity_route.route("/signup",methods=['POST'])
def signup():
	try:
		token = request.json['token']
		activityid = request.json['activity']
		u=getuserinformation(token)
		act = getActivityInformation(activityid)
		if u!=None:
			temp = u.attent(act)
			print temp
			if temp != 2:
				state = "successful"
				reason = ""
			else:
				state ='fail'
				reason ='异常，请重新报名'
		else:
			state = 'fail'
			reason = '用户不存在'

	except Exception, e:
		print e
		state = 'fail'
		reason = 'exception'

	response = jsonify({'state':state,
		                'reason':reason})
	return response

@activity_route.route("/deletesignup",methods=['POST'])
def deletesignup():
	try:
		token = request.json['token']
		activityid = request.json['activityid']
		u=getuserinformation(token)
		act = getActivityInformation(activityid)
		if u!=None:
			temp = u.unattent(act)
			print temp
			if temp != 2:
				state = "successful"
				reason = ""
			else:
				state ='fail'
				reason ='异常，请重新报名'
		else:
			state = 'fail'
			reason = '用户不存在'

	except Exception, e:
		print e
		state = 'fail'
		reason = 'exception'

	response = jsonify({'state':state,
		                'reason':reason})
	return response



@activity_route.route("/getactivityinformation",methods=['POST'])
def getactivityinformation():
	try:
		token = request.json['token']
		page = request.json.get('page','1')
		x=string.atoi(page)
		u=getuserinformation(token)
		if u!=None:
			pagetemp = Activity.query.filter_by(passflag='1').order_by(models.Activity.top.desc()).order_by(models.Activity.timestamp.desc()).paginate(x, per_page=10, error_out=False)
			actlist = pagetemp.items
			pages = pagetemp.pages
			result = []
			state = 'successful'
			reason = ''
			for act in actlist:
				#print act.passflag
				title = act.title if act.title!=None else ''  
				time = act.time if act.time!=None else ''
				location=act.location if act.location!=None else ''
				number=act.number if act.number!=None else ''
				remark = act.remark if act.remark != None else ''
				advertise = act.advertise if act.advertise != None else ''
				#作者信息
				author = act.author.name if act.authorid != None else ''
				authorid = act.authorid if act.authorid != None else ''
				school = act.author.school if act.authorid != None else ''
				gender = act.author.gender if act.authorid != None else ''
				signnumber = act.users.count()
				if u.isattent(act.id) == 0:
					signstate = 'no'
				else:
					signstate = 'yes'
				signnumber = str(signnumber)
				output = {'id':act.id,'author':author,'authorid':authorid,'school':school,'gender':gender,'title':title,'time':time,'location':location,'number':number,'signnumber':signnumber,'remark':remark,'state':signstate,'advertise':advertise}
				result.append(output)
		else:
			state = 'fail'
			reason = '用户不存在'
			result = []
			pages = ''
	except Exception, e:
		print e
		state = 'fail'
		reason = '异常'
		result = []
		pages = ''

	response = jsonify({'result':result,
						'pages':pages,
						'state':state,
						'reason':reason})
	return response

@activity_route.route("/publishactivity",methods=['POST'])
def publishactivity():
	try:
		token = request.json['token']
		title = request.json.get('title','')
		time = request.json.get('time','')
		location = request.json.get('location','')
		number = request.json.get('number','')
		remark = request.json.get('remark','')
		whetherimage = request.json.get('whetherimage','')
		advertise = request.json.get('advertise','')
		detail = request.json.get('detail','')
		label = request.json.get('label','')
		#print whetherimage
		#x=string.atoi(whetherimage)
		#print x
		u = getuserinformation(token)
		if u is not None:
			detail = detail.encode('UTF-8')
			activity1 = Activity(title = title,time = time,location = location,number = number,remark = remark,advertise = advertise,detail = detail,label = label)
			if whetherimage=='0':
				activity1.whetherimage = False
			else:
				activity1.whetherimage = True
			#activity1 = Activity(title = title,time = time,location = location,number = number)
			u.publishactivity(activity1)
			id = activity1.id
			state = 'successful'
			reason = ''
		else:
			id = ''
			state = 'fail'
			reason = 'no user'
	except Exception, e:	
		print e
		id = ''
		state = 'fail'
		reason = 'exception'

	response = jsonify({'state':state,
						'reason':reason,
						'id':id})
	return response

#1.活动置顶图片连接
@activity_route.route("/activitytopofficial",methods=['POST'])
def activitytopofficial():
	try:
		token = request.json['token']
		u = getuserinformation(token)
		if u is not None:	
			state = 'successful'
			reason = ''
			toplist = getactivitytopofficial()
			result = []
			for i in range(len(toplist)):
				output = {"activityid":toplist[i].activityid,"imageurl":toplist[i].imageurl}
				result.append(output)
		else:
			state = 'fail'
			reason = 'no user'
			result = ''

	except Exception, e:
		print e
		result = ''
		state = 'fail'
		reason = 'exception'

	response = jsonify({'result':result,
						'state':state,
						'reason':reason})
	return response
@activity_route.route("/getactivitydetail",methods=['POST'])
def getactivitydetail():
	try:
		token = request.json['token']
		activityid = request.json['activityid']
		u=getuserinformation(token)
		if u!=None:
			#result = []
			act = getactivitybyid(activityid)
			title = act.title if act.title!=None else ''  
			time = act.time if act.time!=None else ''
			location=act.location if act.location!=None else ''
			number=act.number if act.number!=None else ''
			remark = act.remark if act.remark != None else ''
			advertise = act.advertise if act.advertise != None else ''
			detail = act.detail if act.detail != None else ''
			whetherimage = act.whetherimage if act.whetherimage != None else ''
			signnumber = act.users.count()
			signnumber = str(signnumber)
			author = act.author.name if act.authorid != None else ''
			authorid = act.authorid if act.authorid != None else ''
			school = act.author.school if act.authorid != None else ''
			gender = act.author.gender if act.authorid != None else ''
			#是否报名
			signstate = 'no' if u.isattent(act.id) == 0 else 'yes'
			#是否喜欢
			templike = act.likeusers.filter_by(userid = u.id).first()
			flag = '0' if templike is None else '1'
			#获取活动的海报
			poster = activityimageAttach.query.filter_by(activityid = activityid,imageid = 0).first()
			if poster != None:
				image = "http://218.244.147.240:80/activity/activityimages/"+ str(activityid)+'-'+'0'
			else:
				image = ""
			result = {'id':act.id,'author':author,'authorid':authorid,'school':school,'gender':gender,'title':title,'time':time,'location':location,'number':number,'signnumber':signnumber,'remark':remark,'state':signstate,'detail':detail,'advertise':advertise,'whetherimage':whetherimage,'likeflag':flag,"imageurl":image}
			state = 'successful'
			reason = ''
		else:
			state = 'fail'
			reason = '用户不存在'
			result = ''
	except Exception, e:
		print e
		state = 'fail'
		reason = '异常'
		result = ''


	response = jsonify({'result':result,
						'state':state,
						'reason':reason})
	return response
@activity_route.route("/likeactivity",methods=['POST'])
def likeactivity():
	try:
		token = request.json['token']
		activityid = request.json['activityid']
		u = getuserinformation(token)
		if u is not None:
			activity1 = getactivitybyid(activityid)
			temp = u.likeactivity(activity1)
			if temp == 0:
				activity1.likenumber = activity1.likeusers.count()
				activity1.add()
				state = 'successful'
				reason = ''
				likenumber = activity1.likenumber
			elif temp == 1:
				state = 'fail'
				reason = 'already like'
				likenumber = ''
			else:
				state = 'fail'
				reason = 'exception'
				likenumber = ''
		else:
			state = 'fail'
			reason = 'no user'
			likenumber = ''
	except Exception, e:	
		print e
		likenumber = ''
		state = 'fail'
		reason = 'exception'

	response = jsonify({'state':state,
						'reason':reason,
						'likenumber':likenumber})
	return response 
@activity_route.route("/unlikeactivity",methods=['POST'])
def unlikeactivity():
	try:
		token = request.json['token']
		activityid = request.json['activityid']
		u = getuserinformation(token)
		if u is not None:
			activity1 = getactivitybyid(activityid)
			temp = u.unlikeactivity(activity1)
			if temp == 0:
				activity1.likenumber = activity1.likeusers.count()
				activity1.add()
				state = 'successful'
				reason = ''
				likenumber = activity1.likenumber
			elif temp == 1:
				state = 'fail'
				reason = 'already unlike'
				likenumber = ''
			else:
				state = 'fail'
				reason = 'exception'
				likenumber = ''
		else:
			state = 'fail'
			reason = 'no user'
			likenumber = ''
	except Exception, e:	
		print e
		likenumber = ''
		state = 'fail'
		reason = 'exception'

	response = jsonify({'state':state,
						'reason':reason,
						'likenumber':likenumber})
	return response 
@activity_route.route("/searchactivity",methods = ['GET','POST'])
def searchactivity():
	try:
		token = request.json['token']
		text = request.json['text']
		u = getuserinformation(token)
		if u != None:
			title = '%'+text+'%'
			alist=Activity.query.filter_by(passflag='1').filter(Activity.title.like(title))
			state = "successful"
			reason = ''
			result = []
			for act in alist:
				title = act.title if act.title!=None else ''  
				time = act.time if act.time!=None else ''
				location=act.location if act.location!=None else ''
				number=act.number if act.number!=None else ''
				remark = act.remark if act.remark != None else ''
				advertise = act.advertise if act.advertise != None else ''
				#作者信息
				author = act.author.name if act.authorid != None else ''
				authorid = act.authorid if act.authorid != None else ''
				school = act.author.school if act.authorid != None else ''
				gender = act.author.gender if act.authorid != None else ''
				signnumber = act.users.count()
				if u.isattent(act.id) == 0:
					signstate = 'no'
				else:
					signstate = 'yes'
				signnumber = str(signnumber)
				output = {'id':act.id,'author':author,'authorid':authorid,'school':school,'gender':gender,'title':title,'time':time,'location':location,'number':number,'signnumber':signnumber,'remark':remark,'state':signstate,'advertise':advertise}
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
#返回喜欢的活动
@activity_route.route("/getlikeactivity",methods=['POST'])
def getlikeactivity():
	try:
		token = request.json['token']
		page = request.json.get('page','1')
		x=string.atoi(page)
		u = getuserinformation(token)
		if u is not None:	
			state = 'successful'
			reason = ''
			likeactivitypage = u.likeactivitys.order_by(models.likeactivity.timestamp.desc()).paginate(x, per_page=10, error_out=False)
			pages = likeactivitypage.pages
			likeitems = likeactivitypage.items
			result = []
			for temp in likeitems:
				activityid = temp.activityid
				act = getActivityInformation(activityid)
				title = act.title if act.title != None else ''
				number = act.number if act.number != None else ''
				location = act.location if act.location != None else ''
				time = act.time if act.time != None else ''
				remark = act.remark if act.remark != None else ''
				advertise = act.advertise if  act.advertise != None else ''
				signnumber = act.users.count()
				signnumber = str(signnumber)
				signstate = 'no' if u.isattent(act.id) == 0 else 'yes'
				#作者信息
				author = act.author.name if act.authorid != None else ''
				authorid = act.authorid if act.authorid != None else ''
				school = act.author.school if act.authorid != None else ''
				gender = act.author.gender if act.authorid != None else ''

				output = {'id':act.id,'author':author,'authorid':authorid,'school':school,'gender':gender,'title':title,'time':time,'location':location,'number':number,'signnumber':signnumber,'remark':remark,'state':signstate,'advertise':advertise}
				result.append(output)
		else:
			state = 'fail'
			reason = 'no user'
			result = ''
			pages = ''
	except Exception, e:
		print e
		result = ''
		state = 'fail'
		reason = 'exception'
		pages = ''
	response = jsonify({'result':result,
						'pages':pages,
						'state':state,                                                                                                                                                                                  
						'reason':reason})
	return response
#返回参加的活动
@activity_route.route("/getattentactivity",methods=['POST'])
def getattentactivity():
	try:
		token = request.json['token']
		page = request.json.get('page','1')
		x=string.atoi(page)
		u = getuserinformation(token)
		if u is not None:	
			state = 'successful'
			reason = ''
			temppage = u.activitys.order_by(models.attentactivity.timestamp.desc()).paginate(x, per_page=10, error_out=False)
			items = temppage.items
			pages = temppage.pages
			result = []
			for temp in items:
				activityid = temp.activityid
				act = getActivityInformation(activityid)
				title = act.title if act.title != None else ''
				number = act.number if act.number != None else ''
				location = act.location if act.location != None else ''
				time = act.time if act.time != None else ''
				remark = act.remark if act.remark != None else ''
				advertise = act.advertise if  act.advertise != None else ''
				signstate = 'no' if u.isattent(act.id) == 0 else 'yes'
				signnumber = act.users.count()
				signnumber = str(signnumber)
				#作者信息
				author = act.author.name if act.authorid != None else ''
				authorid = act.authorid if act.authorid != None else ''
				school = act.author.school if act.authorid != None else ''
				gender = act.author.gender if act.authorid != None else ''

				output = {'id':act.id,'author':author,'authorid':authorid,'school':school,'gender':gender,'title':title,'time':time,'location':location,'number':number,'signnumber':signnumber,'remark':remark,'state':signstate,'advertise':advertise}
				result.append(output)
		else:
			state = 'fail'
			reason = 'no user'
			result = ''
			pages = ''
	except Exception, e:
		print e
		result = ''
		state = 'fail'
		reason = 'exception'
		pages = ''
	response = jsonify({'result':result,
						'pages':pages,
						'state':state,                                                                                                                                                                                  
						'reason':reason})
	return response
#返回发布的活动
@activity_route.route("/getpublishactivity",methods=['POST'])
def getpublishactivity():
	try:
		token = request.json['token']
		page = request.json.get('page','1')
		x=string.atoi(page)
		u = getuserinformation(token)
		if u is not None:	
			state = 'successful'
			reason = ''
			temppage = u.publishactivitys.order_by(models.Activity.timestamp.desc()).paginate(x, per_page=10, error_out=False)
			items = temppage.items
			pages = temppage.pages
			result = []
			for act in items:
				title = act.title if act.title != None else ''
				number = act.number if act.number != None else ''
				location = act.location if act.location != None else ''
				time = act.time if act.time != None else ''
				remark = act.remark if act.remark != None else ''
				advertise = act.advertise if  act.advertise != None else ''
				signnumber = act.users.count()
				signnumber = str(signnumber)
				#作者信息
				author = act.author.name if act.authorid != None else ''
				authorid = act.authorid if act.authorid != None else ''
				school = act.author.school if act.authorid != None else ''
				gender = act.author.gender if act.authorid != None else ''
				if act.passflag == '1':
					vstate = '通过'
				elif act.passflag == '2':
					vstate = '未通过'
				else:
					vstate = '审核中'
				output = {'id':act.id,'author':author,'authorid':authorid,'school':school,'gender':gender,'title':title,'time':time,'location':location,'number':number,'signnumber':signnumber,'remark':remark,'status':vstate,'advertise':advertise}
				result.append(output)
		else:
			state = 'fail'
			reason = 'no user'
			result = ''
			pages = ''
	except Exception, e:
		print e
		result = ''
		state = 'fail'
		reason = 'exception'
		pages = ''
	response = jsonify({'result':result,
						'state':state,   
						'pages':pages,                                                                                                                                                                               
						'reason':reason})
	return response
#获取发布的活动的信息
@activity_route.route("/getpublishactivitydetail",methods=['POST'])
def getpublishactivitydetail():
	try:
		token = request.json['token']
		activityid = request.json['activityid']
		u=getuserinformation(token)
		act = getactivitybyid(activityid)
		if u!=None and act.author.id==u.id:
			title = act.title if act.title != None else ''  
			time = act.time if act.time != None else ''
			location=act.location if act.location!= None else ''
			number=act.number if act.number!= None else ''
			remark = act.remark if act.remark != None else ''
			advertise = act.advertise if act.advertise != None else ''
			detail = act.detail if act.detail != None else ''
			whetherimage = act.whetherimage if act.whetherimage != None else ''
			signnumber = act.users.count()
			signnumber = str(signnumber)
			#作者信息
			author = act.author.name if act.authorid != None else ''
			authorid = act.authorid if act.authorid != None else ''
			school = act.author.school if act.authorid != None else ''
			gender = act.author.gender if act.authorid != None else ''
			if act.passflag == '1':
				passflag = '通过'
			elif act.passflag == '2':
				passflag = '未通过'
			else:
				passflag = '审核中'
			#获取活动的海报
			poster = activityimageAttach.query.filter_by(activityid = activityid,imageid = 0).first()
			if poster != None:
				image = "http://218.244.147.240:80/activity/activityimages/"+ str(activityid)+'-'+ '0'
			else:
				image = ""
			result = {'id':act.id,'author':author,'authorid':authorid,'school':school,'gender':gender,'title':title,'time':time,'location':location,'number':number,'signnumber':signnumber,'remark':remark,'status':passflag,'detail':detail,'advertise':advertise,'whetherimage':whetherimage,"imageurl":image}
			state = 'successful'
			reason = ''
		else:
			state = 'fail'
			reason = '非法用户'
			result = ''
	except Exception, e:
		print e
		state = 'fail'
		reason = '异常'
		result = ''

	response = jsonify({'result':result,
						'state':state,
						'reason':reason})
	return response


@activity_route.route("/getactivitystatistic", methods=['POST'])
def getactivitystatistic():
	"""get activity statistic information"""
	try:
		token = request.json['token']
		activityid = request.json['activityid']
		activity = getactivitybyid(activityid)
		u = getuserinformation(token)
		if u != None and activity != None:
			state = 'successful'
			reason = ''

			registeredTotal = activity.users.count()
			registeredToday = activity.users.filter(cast(models.attentactivity.timestamp, Date) == date.today()).count()
			likedTotal = activity.likeusers.count()
			likedToday = activity.likeusers.filter(cast(models.likeactivity.timestamp, Date) == date.today()).count()
			
			result = {
					  'activity':activity.title,
					  'registeredTotal':registeredTotal,
					  'registeredToday':registeredToday,
					  'likedTotal':likedTotal, 
					  'likedToday':likedToday, 
					 }

		else:
			state = 'fail'
			reason = 'invalid access'
			result = ''

	except Exception,e:
		print e
		state = 'fail'
		reason = 'exception'
		result = ''

	return jsonify({'state':state, 'reason':reason, 'result':result})

@activity_route.route("/getactivityattentuser",methods=['POST'])
def getactivityattentuser():
	try:
		"""get user life images"""
		def lifeimage_url(activityid,userid,imgid):
			return 'http://218.244.147.240:80/picture/activitylifeimages/' + str(activityid)+'-'+str(userid)+'-'+str(imgid)
		def lifeimage_url_thumbnail(activityid,userid,imgid):
			return 'http://218.244.147.240:80/picture/activitylifeimages/' + str(activityid)+'-'+str(userid)+'-'+str(imgid) + '_thumbnail.jpg'

		token = request.json['token']
		activityid = request.json['activityid']
		page = request.json.get('page','1')
		x=string.atoi(page)
		u = getuserinformation(token)
		activity = getactivitybyid(activityid)
		if u != None and activity.author.id == u.id:	
			state = 'successful'
			reason = ''
			temppage = activity.users.order_by(models.attentactivity.timestamp.desc()).paginate(x, per_page=10, error_out=False)
			items = temppage.items
			pages = temppage.pages
			result = []

			for temp in items:
				userid = temp.userid
				usertemp = getuserbyid(userid)
				lifelist = activitylifeimage.query.filter_by(activityid = activityid,userid = userid).all()
				image = []
				thumbnail = []
				for lifeimage in lifelist:
					image.append(lifeimage_url(lifeimage.activityid, lifeimage.userid, lifeimage.imageid))
					thumbnail.append(lifeimage_url_thumbnail(lifeimage.activityid, lifeimage.userid, lifeimage.imageid))

				name = usertemp.name if usertemp.name != None else ''
				school = usertemp.school if usertemp.school != None else ''
				gender = usertemp.gender if usertemp.gender != None else ''
				flag = '0' if temp.state == 0 else '1'
				output = {"id":userid,"name":name,"school":school,"gender":gender,'flag':flag,'image':image,'thumbnail':thumbnail}
				result.append(output)
		else:
			state = 'fail'
			reason = '非法用户'
			result = ''
			pages = ''
	except Exception, e:
		print e
		result = ''
		state = 'fail'
		reason = 'exception'
		pages = ''
	response = jsonify({'result':result,
						'state':state,    
						'pages':pages,                                                                                                                                                                              
						'reason':reason})
	return response

@activity_route.route("/setpassuser",methods=['POST'])
def setpassuser():
	try:
		token = request.json['token']
		activityid = request.json['activityid']
		userlist = request.json['userlist']
		u = getuserinformation(token)
		activity = getactivitybyid(activityid)
		if u != None and activity.author.id == u.id:	
			state = 'successful'
			reason = ''
			for userid in userlist:
				temp = attentactivity.query.filter_by(userid = userid, activityid = activityid).first()
				if temp != None:
					temp.state = True
					temp.add()
		else:
			state = 'fail'
			reason = '非法用户'
			result = ''
	except Exception, e:
		print e
		result = ''
		state = 'fail'
		reason = 'exception'
	response = jsonify({'state':state,                                                                                                                                                                                  
						'reason':reason})
	return response

@activity_route.route("/deletepassuser",methods=['POST'])
def deletepassuser():
	try:
		token = request.json['token']
		activityid = request.json['activityid']
		userlist = request.json['userlist']
		u = getuserinformation(token)
		activity = getactivitybyid(activityid)
		if u != None and activity.author.id == u.id:	
			state = 'successful'
			reason = ''
			for userid in userlist:
				temp = attentactivity.query.filter_by(userid = userid, activityid = activityid).first()
				if temp != None:
					temp.state = False
					temp.add()
		else:
			state = 'fail'
			reason = '非法用户'
			result = ''
	except Exception, e:
		print e
		result = ''
		state = 'fail'
		reason = 'exception'
	response = jsonify({'state':state,                                                                                                                                                                                  
						'reason':reason})
	return response

