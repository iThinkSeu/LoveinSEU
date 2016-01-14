#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
import models 
from hashmd5 import *
import string
from sqlalchemy import Date, cast

card_route = Blueprint('card_route', __name__)

"""" define  """

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




