#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
from hashmd5 import *
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
				if u.isattent(act.id) == 0:
					state = 'no'
				else:
					state = 'yes'
				output = {'id':act.id,'title':title,'time':time,'location':location,'number':number,'state':state}
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