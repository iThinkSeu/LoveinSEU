# -*- coding: utf-8 -*-
import shutil
import os,stat
from tmodels import *

cnt1 = 0
cnt2 = 0
cnt3 = 0
for id in xrange(1,1000):
	#数据库操作
	avatartmp = getavatarvoicebyuserid(id)
	if avatartmp!=None:
		cnt1 = cnt1 + 1
		avatartmp.name = avatartmp.author.name if avatartmp.author.name!=None else ''
		avatartmp.gender = avatartmp.author.gender if avatartmp.author.gender!=None else ''
		avatartmp.disable = 0 if avatartmp.disable==None else avatartmp.disable
		avatartmp.passflag  = 0 if avatartmp.passflag == None else avatartmp.disable
		avatartmp.add()
		print "have done!"
	else:
		cnt2 = cnt2 + 1
		avatarnumber = 1
		source = '/avatar/'
		src = source + str(id)
		dst = source + str(id) + '-' + str(avatarnumber)
		avatarurl = "http://218.244.147.240:80/avatar/" + str(id) + '-' + str(avatarnumber)
		if os.path.exists(src):
			cnt3 = cnt3 + 1
			shutil.copy(src, dst)
			os.chmod(dst, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP  | stat.S_IROTH)
			#第一次上传头像，新增
			tmp = avatarvoice(userid = id,avatarurl = avatarurl,avatar_number = avatarnumber)
			tmp.add()

print "have done = " + str(cnt1)
print "no avatar = " + str(cnt2)
print "add new = " + str(cnt3)


