#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
import os, stat
from PIL import Image
import string
#import Image
import shutil


upload_image = Blueprint('upload_image', __name__)

@upload_image.route("/uploadavatar", methods=['POST'])
def uploadavatar():
	try:
		jsonstring = request.form.get('json')
		jsonstring = json.loads(jsonstring)
		token = jsonstring['token']
		type = jsonstring['type'] 
		number = jsonstring.get('number', '')
		messageid = jsonstring.get('messageid','')
		postid = jsonstring.get('postid','')
		topicid = jsonstring.get('topicid','')
		topofficialid = jsonstring.get('topofficialid','')
		commentid = jsonstring.get('commentid','')
		activityid = jsonstring.get('activityid','')
		src = request.form.get('avatar_path')

		u = getuserinformation(token)
		id = u.id
		result = {}
		try:
			state = 'successful'
			reason = ''
			if type=="0":
				avatartmp = getavatarvoicebyuserid(id)
				if avatartmp!=None:
					avatarnumber = avatartmp.avatar_number if avatartmp.avatar_number != None else 0
					avatarnumber = avatarnumber + 1
					#路径
					dst = '/home/www/avatar/' + str(id) + '-' + str(avatarnumber)
					avatarurl = "http://218.244.147.240:80/avatar/" + str(id) + '-' + str(avatarnumber)
					#更新数据库
					avatartmp.avatar_number = avatarnumber
					avatartmp.avatarurl = avatarurl
					avatartmp.add()
				else:
					avatarnumber = 1
					#路径
					dst = '/home/www/avatar/' + str(id) + '-' + str(avatarnumber)
					avatarurl = "http://218.244.147.240:80/avatar/" + str(id) + '-' + str(avatarnumber)
					#第一次上传头像，新增
					tmp = avatarvoice(userid = id,avatarurl = avatarurl,avatar_number = avatarnumber)
					tmp.add()
				#移动文件
				shutil.copy(src, dst)
				os.chmod(dst, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP  | stat.S_IROTH)
				#生成卡片头像
				fp = Image.open(dst)
				fp.thumbnail((500,500))
				fp.save(dst + '_card.jpg')
				#生成缩略图
				fp = Image.open(dst)
				fp.thumbnail((200,200))
				fp.save(dst + '_thumbnail.jpg')
				#为了兼容性加的东西
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
				#type = -4 表示上传post的图片附件
				images = getImageURLbyid(number)
				posts = getpostbyid(postid) 
				posts.addimage(images)
				topicid = posts.topic.id
				dst = '/home/www/community/postattachs/' + str(topicid) + '-' + str(postid) + '-' + str(number)
			elif type == "-5":
				#type = -5 表示上传topic的附图
				topictemp = gettopicbyid(topicid)
				dst = '/home/www/community/topics/' + str(topicid)
				topictemp.imageurl = "http://218.244.147.240:80/community/topics/" + str(topicid)
				topictemp.add()
			elif type == "-6":
				#type = -6 表示上传topofficial的图片
				topofficialtemp = gettopofficialbyid(topofficialid)
				dst = '/home/www/community/topofficials/' + str(topofficialid)
				topofficialtemp.imageurl = "http://218.244.147.240:80/community/topofficials/" + str(topofficialid)
				topofficialtemp.add()
			elif type == "-7":
				#type = -7表示上传comment的图片附件
				images = getImageURLbyid(number)
				comments = getcommentbyid(commentid) 
				comments.addimage(images)
				topicid = comments.post.topicid
				dst = '/home/www/community/commentattachs/' + str(topicid) + '-' + str(commentid) + '-' + str(number)
			elif type == "-8":
				#type = -8 表示上传activitytopofficial的图片
				topofficialtemp = getactivitytopofficialbyid(topofficialid)
				dst = '/home/www/activity/activitytopofficials/' + str(topofficialid)
				topofficialtemp.imageurl = "http://218.244.147.240:80/activity/activitytopofficials/" + str(topofficialid)
				topofficialtemp.add()
			elif type == "-9":
				#type = -9 表示上传活动activity的生活照
				dst = '/home/www/picture/activitylifeimages/' + str(activityid)+'-'+str(id)+'-'+str(number)
				a = getactivitybyid(activityid)
				#u = getuserbyid(id)
				m = getImageURLbyid(number)
				a.addlifeimage(u,m)
			elif type == "-10":
				#type = -10 表示上传活动海报照片
				dst = '/home/www/activity/activityimages/' + str(activityid) + '-' +str(number)
				images = getImageURLbyid(number)
				activity = getactivitybyid(activityid)
				activity.addimage(images)
			elif type == "-11":
				#type = -11 表示上传美食卡片
				foodcardid = string.atoi(str(jsonstring.get('foodcardid','0')))
				tmpfoodcard = foodcard.query.filter_by(id = foodcardid).first()
				dst = '/home/www/picture/foodcards/' + str(foodcardid) + '-' +str(id)
				tmpfoodcard.imageurl = "http://218.244.147.240:80/picture/foodcards/" + str(foodcardid) + '-' +str(id)
				tmpfoodcard.add()
			elif type == "-12":
				#type ==12 表示上传个人声音名片
				voicetmp = getavatarvoicebyuserid(id)
				if voicetmp!=None:
					voicenumber = voicetmp.voice_number if voicetmp.voice_number!=None else 0
					voicenumber = voicenumber + 1
					dst = '/home/www/static/personalvoices/' + str(id) + "-" + str(voicenumber)
					#更新数据库
					voicetmp.voice_number = voicenumber
					voicetmp.voiceurl = 'http://218.244.147.240:80/static/personalvoices/' + str(id) + "-" + str(voicenumber)
					voicetmp.add()
				else:
					voicenumber = 1
					dst = '/home/www/static/personalvoices/' + str(id) + "-" + str(voicenumber)
					voiceurl = 'http://218.244.147.240:80/static/personalvoices/' + str(id) + "-" + str(voicenumber)
					tmp = avatarvoice(userid = id,voice_number = voicenumber,voiceurl = voiceurl)
					tmp.add()
			elif type == "-13":
				#type = -13 表示上传cetification的附件图片
				certid = jsonstring.get('certificationid','')
				dst = '/home/www/static/schoolcertifications/' + str(id) + "-" + str(certid)
				tmp = schoolcertification.query.filter_by(id = certid).first()
				if tmp!=None:
					tmp.pictureurl = 'http://218.244.147.240:80/static/schoolcertifications/' + str(id) + "-" + str(certid)
					tmp.add()
				else:
					state = 'fail'
					reason = 'no this certification id'
			elif type == "-14":
				#type = -14表示上传commentact的图片附件
				images = getImageURLbyid(number)
				commentacts = getcommentactbyid(commentid) 
				commentacts.addimage(images)
				activityid = commentacts.activityid
				dst = '/home/www/activity/commentactsImage/' + str(activityid) + '-' + str(commentid) + '-' + str(number)
			elif type == "-15":
				#type = -15 表示上传更新的android APK安装包
				v1 = jsonstring.get('v1','0')
				v2 = jsonstring.get('v2','0')
				v3 = jsonstring.get('v3','0')

				wemeurl = 'http://218.244.147.240:80/static/androidapk/' + "weme_V"+ str(v1) + "." + str(v2) + "." + str(v3) + ".apk"
				apk = androidversion.query.filter_by(v1 = v1,v2 = v2, v3 = v3).first()
				if apk != None:
					dst = '/home/www/picture/temp/' + "weme_V" + str(v1) + "." + str(v2) + "." + str(v3) + ".apk"
					result = {"v1":v1,"v2":v2,"v3":v3,"have":"already have this version"}
				else:
					dst = '/home/www/static/androidapk/'+"weme_V"+ str(v1) + "." + str(v2) + "." + str(v3) + ".apk"
					wemeapktemp = androidversion(v1 = v1,v2 = v2,v3 = v3, wemeurl = wemeurl)
					wemeapktemp.add()
					result = {"v1":v1,"v2":v2,"v3":v3,"have":"update successful"}
				dstnewest = '/home/www/static/androidapk/' + "weme_neweast.apk"
				shutil.copy(src, dstnewest)
				os.chmod(dstnewest, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP  | stat.S_IROTH)
			else:
				state = 'fail'
				reason = 'no this type'				
				dst = '/home/www/picture/temp/' + str(id)


			'''
			if os.path.exists(dst):
				os.remove(dst)
				os.remove(dst + '_thumbnail.jpg')
			'''

			shutil.move(src, dst)
			os.chmod(dst, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP  | stat.S_IROTH)
			if type =="0":
				fp = Image.open(dst)
				fp.thumbnail((200,200))
				fp.save(dst + '_thumbnail.jpg')
			if type == "-4" or type == "-7" or type == "-10" or type == "-9" or type == "-2" or type == "-14":
				fp = Image.open(dst)
				fp.thumbnail((200,200))
				fp.save(dst + '_thumbnail.jpg')
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
						'result':result,
						'state':state,
						'reason':reason})
	return response

