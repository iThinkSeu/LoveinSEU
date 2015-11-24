#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
import os, stat
from PIL import Image
import shutil


upload_image = Blueprint('upload_image', __name__)

@upload_image.route("/messageAppendix",methods=['POST'])
@upload_image.route("/uploadavatar", methods=['POST'])
def uploadavatar():
	try:
		jsonstring = request.form.get('json')
		jsonstring = json.loads(jsonstring)
		token = jsonstring['token']
		type = jsonstring['type'] 
		number = jsonstring['number']
		messageid = jsonstring.get('messageid','')
		postid = jsonstring.get('postid','')
		topicid = jsonstring.get('topicid','')
		topofficialid = jsonstring.get('topofficialid','')
		id = getuserinformation(token).id
		src = request.form.get('avatar_path')

		#print avatar
		#avatar_type =  request.form.get('avatar_content_type').split('/')[-1]
		#print avatar_type
		try:
			if type=="0":
				dst = '/home/www/avatar/' + str(id)
			elif type=="1":
				dst = '/home/www/picture/qianshoudongda/' + str(id)+'-'+str(type)+'-'+str(number)
			elif type=="5":
				dst = '/home/www/picture/yaoda/' + str(id)+'-'+str(type)+'-'+str(number)
			elif type=="3":
				dst = '/home/www/picture/autumn-2/' + str(id)+'-'+str(type)+'-'+str(number)
			elif type =="4":
				dst = '/home/www/picture/autumn-3/' + str(id)+'-'+str(type)+'-'+str(number)
			elif type == "-1":
				dst = '/home/www/background/' + str(id)
			elif type == "-2":
				image_number = getImageURLbyid(number)
				message_send = getMessagebyid(messageid)
				message_send.addimage(image_number)
				dst = '/home/www/message/image/' + str(messageid) + '-' + str(number)
			elif type == "-3":
				dst = '/home/www/message/vedio/' + str(messageid) + '-' + str(number)
			elif type == "-4":
				images = getImageURLbyid(number)
				posts = getpostbyid(postid) 
				posts.addimage(images)
				topicid = posts.topic.id
				dst = '/home/www/community/postattachs/' + str(topicid) + '-' + str(postid) + '-' + str(number)
			elif type == "-5":
				topictemp = gettopicbyid(topicid)
				dst = '/home/www/community/topics/' + str(topicid)
				topictemp.imageurl = "http://218.244.147.240:80/community/topics/" + str(topicid)
				topictemp.add()
			elif type == "-6":
				topofficialtemp = gettopofficialbyid(topofficialid)
				dst = '/home/www/community/topofficials/' + str(topofficialid)
				topofficialtemp.imageurl = "http://218.244.147.240:80/community/topofficials/" + str(topofficialid)
				topofficialtemp.add()
			else:
				dst = '/home/www/picture/temp/' + str(id)

			'''
			if os.path.exists(dst):
				os.remove(dst)
				os.remove(dst + '_thumbnail.jpg')
			'''

			shutil.move(src, dst)
			os.chmod(dst, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP  | stat.S_IROTH)
			if type =="0" or type == "-2" or type == "-4":
				fp = Image.open(dst)
				fp.thumbnail((100,100))
				fp.save(dst + '_thumbnail.jpg')
			state = 'successful'
			reason = ''
		except Exception, e:
			print e 
			state = 'fail'
			reason = '上传图片失败,请重传'
	except Exception, e:
		print e 
		id=''
		state = 'fail'
		reason='异常,请重传'


	response = jsonify({'id':id,
						'state':state,
						'reason':reason})
	return response

