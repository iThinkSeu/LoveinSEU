#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
import models 
import string
from sqlalchemy import Date, cast
import random

card_route = Blueprint('card_route', __name__)

#防止数据库为空
"""define checkdbNone"""
def checkdb(dbNone):
	return dbNone if dbNone!=None else ''

@card_route.route("/publishcard",methods=['POST'])
def publishactivity():
	try:
		token = request.json['token']
		title = request.json.get('title','')
		location = request.json.get('location','')
		longitude = request.json.get('longitude','')
		latitude = request.json.get('latitude','')
		price = request.json.get('price','')
		comment = request.json.get('comment','')
		u = getuserinformation(token)
		if u is not None:
			comment = comment.encode('UTF-8')
			tmpfoodcard = foodcard(title = title,location = location,longitude = longitude,latitude = latitude,price = price,comment = comment)
			u.publishfoodcard(tmpfoodcard)
			id = tmpfoodcard.id
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

@card_route.route("/getfoodcard",methods=['POST'])
def getfoodcard():
	try:
		token = request.json['token']
		u = getuserinformation(token)
		if u is not None:
			listfoodcard = foodcard.query.filter_by(passflag='1').all()
			tmprand = random.sample(listfoodcard,1)
			if len(tmprand)>0:
				tmpfoodcard = tmprand[0]
				result = {"id":tmpfoodcard.id,"title":checkdb(tmpfoodcard.title),"authorid":checkdb(tmpfoodcard.authorid),"imageurl":checkdb(tmpfoodcard.imageurl),'location':checkdb(tmpfoodcard.location),'longitude':checkdb(tmpfoodcard.longitude),'latitude':checkdb(tmpfoodcard.latitude),'price':checkdb(tmpfoodcard.price),'comment':checkdb(tmpfoodcard.comment),'likenumber':checkdb(tmpfoodcard.likenumber)}
				state = 'successful'
				reason = ''
			else:
				result = ''
				state = 'fail'
				reason = 'no card'				
		else:
			result = ''
			state = 'fail'
			reason = 'no user'
	except Exception, e:	
		print e
		result = ''
		state = 'fail'
		reason = 'exception'

	response = jsonify({'state':state,
						'reason':reason,
						'result':result})
	return response

@card_route.route("/likefoodcard",methods=['POST'])
def likefoodcard():
	try:
		token = request.json['token']
		foodcardid = request.json['foodcardid']
		u = getuserinformation(token)
		if u is not None:
			tmpfoodcard = foodcard.query.filter_by(id = foodcardid).first()
			temp = u.likefoodcard(tmpfoodcard)
			if temp == 0:
				state = 'successful'
				reason = ''
				tmpfoodcard.likenumber = tmpfoodcard.likeusers.count()
				tmpfoodcard.add()
				likenumber = tmpfoodcard.likenumber
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


