#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
from hashmd5 import *
import string;
import datetime

personalmessage_route = Blueprint('personalmessage_route', __name__)


@personalmessage_route.route("/sendmessage",methods = ['POST'])
def sendmessage():
	try:
		token = request.json['token']
		text = request.json.get('text','')
		RecId = request.json.get('RecId','-1')
		u = getuserinformation(token)
		if u != None:
			SendId = u.id
			messageTemp = Message(SendId = SendId, RecId = RecId, text = text)
			messageTemp.add()
			id = messageTemp.id
			state = 'successful'
			reason = ''
		else:
			state = 'fail'
			reason = 'no user'
			id = ''
		
	except Exception, e:
		print e
		state = 'fail'
		reason = 'exception'
		id = ''

	response = jsonify({'id':id,
						'state':state,
						'reason':reason})
	return response

@personalmessage_route.route("/readmessage",methods = ['POST'])
def readmessage():
	try:
		token = request.json['token']
		id = request.json.get('id','')
		u = getuserinformation(token)
		m = getMessagebyid(id)
		if u != None:
			if m.RecId == str(u.id):
				m.state = 0
				m.add()			
			state = 'successful'
			reason = ''
		else:
			state = 'fail'
			reason = 'no user'
	
		
	except Exception, e:
		print e
		state = 'fail'
		reason = 'exception'

	response = jsonify({'state':state,
						'reason':reason})
	return response
@personalmessage_route.route("/getSendUserList",methods = ['POST'])
def getSendUserList():
	try:
		token = request.json['token']
		u = getuserinformation(token)
		if u != None:
			id = u.id
			#m = getMessageList(id)
			m = getMessageListByID(id)
			L = [ x.SendId if x.RecId == str(id) else x.RecId for x in m]
			L = list(set(L))
			print L
			result = []
			for i in range(len(L)):
				unReadnum = 0
				Id = L[i]
				mSendi = getMessageTwoid(Id,id) or getMessageTwoid(id, Id)
				mSendi.reverse()
				if len(mSendi) > 0:
					text = mSendi[0].text
					lasttime = mSendi[0].sendtime
					for j in range(len(mSendi)):
						if mSendi[j].RecId == str(id) and mSendi[j].state == '1':
							unReadnum=unReadnum+1
					senduser = getuserbyid(Id)
					if senduser != None:
						print Id, unReadnum
						output = {"SendId":Id ,"unreadnum":unReadnum,"name":senduser.name,"gender":senduser.gender,"school":senduser.school,"text":text,"lasttime":lasttime}
						result.append(output)
			state = 'successful'
			reason = ''
		else:
			state = 'fail'
			reason = 'no user'
			result = ''
	
		
	except Exception, e:
		print e
		state = 'fail'
		reason = 'exception'
		result = ''

	response = jsonify({'state':state,
						'reason':reason,
						'result':result})
	return response

@personalmessage_route.route("/getMessageDetailList", methods = ['POST'])
def getMessageDetailList():
	try:
		token = request.json['token']
		SendId = request.json['SendId']
		page = request.json['page']
		#print page
		x=string.atoi(page)
		u = getuserinformation(token)
		if u != None:
			id = u.id
			result = []
			pageitems = getMessageTwoidPage(SendId,id,x)
			L = pageitems.items
			for i in range(len(L)):
				senduser = getuserbyid(L[i].SendId)
				name = senduser.name if senduser.name !=None else ''
				gender = senduser.gender if senduser.gender !=None else ''
				school = senduser.school if senduser.school !=None else ''
				text = L[i].text if L[i].text != None else ''
				Limage=L[i].imagedb.all()
				image = []
				for j in range(len(Limage)):
					number = Limage[j].image_id
					url = "http://218.244.147.240:80/message/image/" + str(L[i].id) + "-" + str(number)
					image.append(url)
				vedio = ''
				time = L[i].sendtime
				readstate = L[i].state

				output = {"messageid":L[i].id,"text":text,"image":image,"vedio":vedio,"time":time,"readstate":readstate,"SendId":L[i].SendId,"name":name,"school":school}
				result.append(output)

			state = 'successful'
			reason = ''
		else:
			state = 'fail'
			reason = 'no user'
			result = ''
	except Exception, e:
		print e
		state = 'fail'
		reason = 'exception'
		result = ''

	response = jsonify({'state':state,
						'reason':reason,
						'result':result})
	return response

@personalmessage_route.route("/getmessageunreadnumber",methods = ['POST'])
def getmessageunreadnumber():
	try:
		token = request.json['token']
		u = getuserinformation(token)
		if u != None:
			id = u.id
			m = getMessageList(id)
			unReadnum = 0
			for j in range(len(m)):
				if m[j].state == '1':
					unReadnum=unReadnum+1
			state = 'successful'
			reason = ''
		else:
			state = 'fail'
			reason = 'no user'
			number = ''
	except Exception, e:
		print e
		state = 'fail'
		reason = 'exception'
		number = ''

	response = jsonify({'state':state,
						'reason':reason,
						'number':str(unReadnum)})
	return response
