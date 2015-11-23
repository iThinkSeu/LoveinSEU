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
		activity = request.json['activity']
		u=getuserinformation(token)

		if u!=None:
			if activity =='1':
				writestate = editDBcolumn(token,'qianshoudongda','yes')
			elif activity == '5':
				writestate=editDBcolumn(token,'yaoda','yes')
			elif activity == '3':
				writestate = editDBcolumn(token,'autumn2','yes')
			elif activity == '4':
				writestate = editDBcolumn(token,'autumn3','yes')
			else:
				writestate = 1
			if not writestate:
				state = 'successful'
				reason = ''
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
		act1 = getActivityInformation(5)
		act2 = getActivityInformation(1)
		act3 = getActivityInformation(3)
		act4 = getActivityInformation(4)

 		if u!=None:
 			if u.yaoda!='yes':
 				state1='no'
 			else:
 				state1='yes'

 			if u.qianshoudongda!='yes':
 				state2='no'
 			else:
 				state2='yes'

 			if u.autumn2!='yes':
 				state3='no'
 			else:
 				state3 = 'yes'

 			if u.autumn3!='yes':
 				state4='no'
 			else:
 				state4='yes'

 			if (act1!=None) and (act2!=None) and (act3!=None) and (act4!=None):
 				state = 'successful'
 				reason=''
 				title1 = act1.title if act1.title!=None else ''  
 				time1 = act1.time if act1.time!=None else ''
 				location1=act1.location if act1.location!=None else ''
 				number1=act1.number if act1.number!=None else ''

 				title2 = act2.title if act2.title!=None else ''  
 				time2 = act2.time if act2.time!=None else ''
 				location2=act2.location if act2.location!=None else ''
 				number2=act2.number if act2.number!=None else ''

 				title3 = act3.title if act3.title!=None else ''  
 				time3 = act3.time if act3.time!=None else ''
 				location3=act3.location if act3.location!=None else ''
 				number3=act3.number if act3.number!=None else ''

 				title4 = act4.title if act4.title!=None else ''  
 				time4 = act4.time if act4.time!=None else ''
 				location4=act4.location if act4.location!=None else ''
 				number4=act4.number if act4.number!=None else ''

			else:
				state = 'fail'
				reason = '活动不存在'
 				title1 = 'NoActivity'  
 				time1 =''
 				location1=''
 				number1=''

 				title2 =''  
 				time2 = ''
 				location2=''
 				number2=''

 				title3 =''  
 				time3 = ''
 				location3=''
 				number3=''

 				title4 =''  
 				time4 =''
 				location4=''
 				number4=''
 		else:

 			state = 'fail'
 			reason = '用户不存在'
			title1 = ''  
			time1 =''
			location1=''
			number1=''
			state1=''

			title2 =''  
			time2 = ''
			location2=''
			number2=''
			state2=''

			title3 =''  
			time3 = ''
			location3=''
			number3=''
			state3=''

			title4 =''  
			time4 =''
			location4=''
			number4=''
			state4=''



	except Exception, e:

		print e
		state = 'fail'
		reason = '异常'
		title1 = 'e'  
		time1 ='e'
		location1='e'
		number1='e'
		state1='e'

		title2 ='e'  
		time2 = 'e'
		location2='e'
		number2='e'
		state2='e'

		title3 ='e'  
		time3 = 'e'
		location3='e'
		number3='e'
		state3='e'

		title4 ='e'  
		time4 ='e'
		location4='e'
		number4='e'
		state4='e'


	response = jsonify({
							'result':[{
							'id':'5',
							'title':title1,
							'time':time1,
							'location':location1,
							'number':number1,
							'state':state1},
							{
							'id':'1',
							'title':title2,
							'time':time2,
							'location':location2,
							'number':number2,
							'state':state2},
	 	    				
							{  		
							'id':'3',					
							'title':title3,
							'time':time3,
							'location':location3,
							'number':number3,
							'state':state3},
							{
							'id':'4',
							'title':title4,
							'time':time4,
							'location':location4,
							'number':number4,
							'state':state4}],
							'reason':reason,
							'state':state 
							}
						)
	return response
