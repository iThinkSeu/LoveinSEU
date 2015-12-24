#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
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
		state = 'fail'
		reason = 'exception'

	response = jsonify({'state':state,
		                'reason':reason})
	return response

@activity_route.route("/getactivityinformation",methods=['POST'])
def getactivityinformation():
	try:
		token = request.json['token']
		u=getuserinformation(token)

		if u!=None:
			actlist = getactivityall()
			result = []
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
