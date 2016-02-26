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
		v1_now = string.atoi(str(request.json.get('v1','1')))
		v2_now = string.atoi(str(request.json.get('v2','0')))
		v3_now = string.atoi(str(request.json.get('v3','0')))
		version_newest = {}
		wemeapk = androidversion.query.filter_by(disable = False).order_by(androidversion.timestamp.desc()).first()
		if wemeapk!=None:
			v1_newest = wemeapk.v1
			v2_newest = wemeapk.v2
			v3_newest = wemeapk.v3
			numNow = v1_now*10000 + v2_now*100 + v3_now
			numNewest = v1_newest*10000 + v2_newest*100 + v3_newest
			if numNow < numNewest:
				update_flag = "yes"
				apkurl = wemeapk.wemeurl
			else:
				update_flag = "no"
				apkurl = ""
			state = "successful"
			reason = ""
			version_newest = {"v1":str(v1_newest),"v2":str(v2_newest),"v3":str(v3_newest)}
		else:
			state = 'fail'
			reason = 'Not apk in server'
			update_flag = "no"
			apkurl = ""
	except Exception, e:	
		print e
		state = 'fail'
		reason = 'exception'
		update_flag = "no"
		apkurl = ""

	response = jsonify({'version_newest':version_newest,
						'updateflag':update_flag,
						'apkurl':apkurl,
						'state':state,
						'reason':reason})
	return response


