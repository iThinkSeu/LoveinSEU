#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
import models 
import string
from datetime import *

androidapk_route = Blueprint('androidapk_route', __name__)

#防止数据库为空
"""define checkdbNone"""
def checkdb(dbNone):
	return dbNone if dbNone!=None else ''


@androidapk_route.route("/checkapkversion",methods=['POST'])
def checkapkversion():
	try:
		token = request.json['token']
		v1_now = string.atoi(str(request.json.get('v1','1')))
		v2_now = string.atoi(str(request.json.get('v2','0')))
		v3_now = string.atoi(str(request.json.get('v3','0')))
		u = getuserinformation(token)
		if u is not None:
			wemeapk = androidversion.query.filter_by(disable = False).order_by(androidversion.timestamp.desc()).first()
			if wemeapk!=None:
				v1_newest = wemeapk.v1
				v2_newest = wemeapk.v2
				v3_newest = wemeapk.v3
				numNow = v1_now*10000 + v2_now*100 + v3_now
				numNewest = v1_newest*10000 + v2_newest*100 + v3_newest
				print "now" + str(numNow)
				print "newest" + str(numNewest)
				if numNow < numNewest:
					update_flag = "yes"
					apkurl = wemeapk.wemeurl
				else:
					update_flag = "no"
					apkurl = ""
				state = "successful"
				reason = ""
			else:
				state = 'fail'
				reason = 'Not apk in server'
				update_flag = "no"
				apkurl = ""
		else:
			state = 'fail'
			reason = 'no user'
			update_flag = "no"
			apkurl = ""
	except Exception, e:	
		print e
		state = 'fail'
		reason = 'exception'
		update_flag = "no"
		apkurl = ""

	response = jsonify({'updateflag':update_flag,
						'apkurl':apkurl,
						'state':state,
						'reason':reason})
	return response


