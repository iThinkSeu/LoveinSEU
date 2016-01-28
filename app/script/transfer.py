# -*- coding: utf-8 -*-
import shutil
import os,stat
from PIL import Image
from tmodels import *

"""define checkdbNone"""
def checkdb(dbNone):
	return dbNone if dbNone!=None else ''

cnt1 = 0
cnt2 = 0
cnt3 = 0
cnt4 = 0
cnt5 = 0
for id in xrange(1,1050):
	#数据库操作
	avatartmp = getavatarvoicebyuserid(id)
	source = '/avatar/'
	if avatartmp!=None:
		cnt1 = cnt1 + 1
		avatartmp.disable = False 
		avatartmp.cardflag  = False
		try:
			avatartmp.name = avatartmp.author.name if avatartmp.author.name!=None else ''
			avatartmp.gender = avatartmp.author.gender if avatartmp.author.gender!=None else ''
			#print " in try"
		except Exception, e:
			cnt4 = cnt4 + 1
			print "None author"

		avatartmp.add()
		print str(id) + ':havedone'
		#print str(id) + ":" + checkdb(avatartmp.author.name) +"," + checkdb(avatartmp.name) + checkdb(avatartmp.author.gender)+"," + checkdb(avatartmp.gender) + "have done!"
		#转存卡片缩略图
		avatarnumber = avatartmp.avatar_number
		src = source + str(id) + '-' + str(avatarnumber)
		dst = source + str(id) + '-' + str(avatarnumber)
		if os.path.exists(dst):
			cnt5 = cnt5 + 1
			#print dst
			try:
				fp = Image.open(dst)
				fp.thumbnail((500,500))
				fp.save(dst + '_card.jpg')
				#生成缩略图
				fp = Image.open(dst)
				fp.thumbnail((200,200))
				fp.save(dst + '_thumbnail.jpg')
			except Exception, e:
				print dst +　"image error"

	else:
		cnt2 = cnt2 + 1
		avatarnumber = 1
		src = source + str(id)
		dst = source + str(id) + '-' + str(avatarnumber)
		avatarurl = "http://218.244.147.240:80/avatar/" + str(id) + '-' + str(avatarnumber)
		if os.path.exists(src):
			cnt3 = cnt3 + 1
			shutil.copy(src, dst)
			os.chmod(dst, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP  | stat.S_IROTH)
			#第一次上传头像，新增
			print str(id)+":add new"
			tmp = avatarvoice(userid = id,avatarurl = avatarurl,avatar_number = avatarnumber)
			tmp.add()
			tmp.name = tmp.author.name if tmp.author.name!=None else ''
			tmp.gender = tmp.author.gender if tmp.author.gender!=None else ''
			tmp.add()
			#生成中等缩略图
			fp = Image.open(dst)
			fp.thumbnail((500,500))
			fp.save(dst + '_card.jpg')
			#生成缩略图
			fp = Image.open(dst)
			fp.thumbnail((200,200))
			fp.save(dst + '_thumbnail.jpg')
print "have done = " + str(cnt1)
print "no author = " + str(cnt4)
print "no avatar = " + str(cnt2)
print "add new = " + str(cnt3)

