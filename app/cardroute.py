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
				result = {"id":tmpfoodcard.id,"title":checkdb(tmpfoodcard.title),"authorid":checkdb(tmpfoodcard.authorid),"imageurl":checkdb(tmpfoodcard.imageurl),'location':checkdb(tmpfoodcard.location),'longitude':checkdb(tmpfoodcard.longitude),'latitude':checkdb(tmpfoodcard.latitude),'price':checkdb(tmpfoodcard.price),'comment':checkdb(tmpfoodcard.comment)}
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





