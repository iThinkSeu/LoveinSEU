# -*- coding: utf-8 -*-
import shutil
import os,stat
from tmodels import *

for id in xrange(1,1000):
	#数据库操作
	avatartmp = getavatarvoicebyuserid(id)
	if avatartmp!=None:
		print "have done!"
	else:
		avatarnumber = 1
		source = '/avatar/'
		src = source + str(id)
		dst = source + str(id) + '-' + str(avatarnumber)
		avatarurl = "http://218.244.147.240:80/avatar/" + str(id) + '-' + str(avatarnumber)
		if os.path.exists(src):
			shutil.copy(src, dst)
			os.chmod(dst, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP  | stat.S_IROTH)
			#第一次上传头像，新增
			tmp = avatarvoice(userid = id,avatarurl = avatarurl,avatar_number = avatarnumber)
			tmp.add()

