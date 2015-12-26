#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
import models 
from hashmd5 import *
import string

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
			result = []
			state = 'successful'
			reason = ''
			for act in actlist:
				title = act.title if act.title!=None else ''  
				time = act.time if act.time!=None else ''
				location=act.location if act.location!=None else ''
				number=act.number if act.number!=None else ''
				remark = act.remark if act.remark != None else ''
				advertise = act.advertise if act.advertise != None else ''
				signnumber = act.users.count()
				if u.isattent(act.id) == 0:
					state = 'no'
				else:
					state = 'yes'
				signnumber = str(signnumber)
				output = {'id':act.id,'title':title,'time':time,'location':location,'number':number,'signnumber':signnumber,'remark':remark,'state':state,'advertise':advertise}
				result.append(output)
		else:
			state = 'fail'
			reason = '用户不存在'
			result = []
	except Exception, e:
		print e
		state = 'fail'
		reason = '异常'
		result = []

	response = jsonify({'result':result,
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
		print whetherimage
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
				output = {"postid":toplist[i].activityid,"imageurl":toplist[i].imageurl}
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
			result = []
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
			if u.isattent(act.id) == 0:
				state = 'no'
			else:
				state = 'yes'
			signnumber = str(signnumber)
			templike = act.likeusers.filter_by(userid = u.id).first()
			if templike is None:
				flag = '0'
			else:
				flag = '1'
			output = {'id':act.id,'title':title,'time':time,'location':location,'number':number,'author':act.author.name,'signnumber':signnumber,'remark':remark,'state':state,'detail':detail,'advertise':advertise,'whetherimage':whetherimage,'likeflag':flag}
			result.append(output)
			state = 'successful'
			reason = ''
		else:
			state = 'fail'
			reason = '用户不存在'
			result = []
	except Exception, e:
		print e
		state = 'fail'
		reason = '异常'
		result = []


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
				likenumber = ''
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
@activity_route.route("/searchactivity",methods = ['GET','POST'])
def searchactivity():
	try:
		token = request.json['token']
		text = request.json['text']
		u = getuserinformation(token)
		if u != None:
			title = '%'+text+'%'
			alist=Activity.query.filter(Activity.title.like(title))
			state = "successful"
			reason = ''
			result = [{"id":search.id,"title":search.title,"number":search.number,"location":search.location,"time":search.time} for search in alist]
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
			likeitems = likeactivitypage.items
			result = []
			for temp in likeitems:
				activityid = temp.activityid
				activitytemp = getActivityInformation(activityid)
				title = activitytemp.title if activitytemp.title != None else ''
				number = activitytemp.number if activitytemp.number != None else ''
				location = activitytemp.location if activitytemp.location != None else ''
				time = activitytemp.time if activitytemp.time != None else ''
				output = {"id":activityid,"title":title,"number":number,"location":location,"time":time}
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
			result = []
			for temp in items:
				activityid = temp.activityid
				activitytemp = getActivityInformation(activityid)
				title = activitytemp.title if activitytemp.title != None else ''
				number = activitytemp.number if activitytemp.number != None else ''
				location = activitytemp.location if activitytemp.location != None else ''
				time = activitytemp.time if activitytemp.time != None else ''
				output = {"id":activityid,"title":title,"number":number,"location":location,"time":time}
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
			result = []
			for temp in items:
				activityid = temp.id
				title = temp.title if temp.title != None else ''
				number = temp.number if temp.number != None else ''
				location = temp.location if temp.location != None else ''
				time = temp.time if temp.time != None else ''
				passflag = '1' if temp.passflag == True else '0'
				output = {"id":activityid,"title":title,"number":number,"location":location,"time":time,"passflag":passflag}
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
#获取发布的活动的信息
@activity_route.route("/getpublishactivitydetail",methods=['POST'])
def getpublishactivitydetail():
	try:
		token = request.json['token']
		activityid = request.json['activityid']
		u=getuserinformation(token)
		act = getactivitybyid(activityid)
		if u!=None and act.author.id==u.id:
			result = []
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
			if act.passflag == '1':
				state = 'pass'
			elif act.passflag == '2':
				state = 'nopass'
			else:
				state = 'verify'
			output = {'id':act.id,'title':title,'time':time,'location':location,'number':number,'author':act.author.name if act.authorid!=None else '','signnumber':signnumber,'remark':remark,'state':state,'detail':detail,'advertise':advertise,'whetherimage':whetherimage}
			result.append(output)
			state = 'successful'
			reason = ''
		else:
			state = 'fail'
			reason = '非法用户'
			result = []
	except Exception, e:
		print e
		state = 'fail'
		reason = '异常'
		result = []

	response = jsonify({'result':result,
						'state':state,
						'reason':reason})
	return response
@activity_route.route("/getactivityattentuser",methods=['POST'])
def getactivityattentuser():
	try:
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
			result = []
			for temp in items:
				userid = temp.userid
				usertemp = getuserbyid(userid)
				name = usertemp.name if usertemp.name != None else ''
				school = usertemp.school if usertemp.school != None else ''
				gender = usertemp.gender if usertemp.gender != None else ''
				output = {"id":userid,"name":name,"school":school,"gender":gender}
				result.append(output)
		else:
			state = 'fail'
			reason = '非法用户'
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