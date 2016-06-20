# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import request,jsonify,json
from models import *
import string
from apns import APNs, Payload

client = APNs(use_sandbox=False, cert_file="cert/cert.pem", key_file="cert/key.pem", enhanced = False)

def send_notification(token_hex, payload):
	client.gateway_server.send_notification(token_hex, payload)

def notify_follow_to_user(u, friend):
	try:
		if (u is not None) and (u.iosdevicetoken is not None) and (friend is not None):
			alert = friend.name + u' 关注了你'
			payload = Payload(alert=alert, sound="default", custom = {'type':'follow', 'userid':friend.id})
			send_notification(u.iosdevicetoken.devicetoken, payload)
	except Exception, e:
		print e

def notify_message_to_user(u, friend):
	try:
		if (u is not None) and (u.iosdevicetoken is not None) and (friend is not None):
			alert = friend.name + u' 给你发了一条私信'
			payload = Payload(alert=alert, sound="default", custom = {'type':'message', 'userid':friend.id})
			send_notification(u.iosdevicetoken.devicetoken, payload)
	except Exception, e:
		print e

push = Blueprint('push', __name__)

@push.route('/uploadiosdevicetoken', methods = ['POST'])
def uploadIOSDeviceToken():
	"""
	upload ios device token for push notifications (APNs)
	"""
	try:
		token = request.json['token']
		devicetoken = str(request.json['devicetoken'])
		u = getuserinformation(token)
		if (u is not None) and len(devicetoken) > 0:
			state = 'successful'
			reason = ''
			if u.iosdevicetoken is not None:
				u.iosdevicetoken.devicetoken = devicetoken
				u.iosdevicetoken.timestamp = datetime.now()
				try:
					db.session.add(u)
					db.session.commit()
				except:
					db.session.rollback()
			else:
				iosdevicetoken = IOSDeviceToken(devicetoken = devicetoken)
				u.add_ios_device_token(iosdevicetoken)
		else:
			state = 'fail'
			reason = 'invalid access'

	except Exception, e:
		print e
		state = 'fail'
		reason = 'exception'

	return jsonify({'state':state, 'reason':reason})



