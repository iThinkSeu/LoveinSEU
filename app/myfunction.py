#-*- coding: UTF-8 -*- 
import time
#计算星座
def Zodiac(month, day):
	n = (u'摩羯座',u'水瓶座',u'双鱼座',u'白羊座',u'金牛座',u'双子座',u'巨蟹座',u'狮子座',u'处女座',u'天秤座',u'天蝎座',u'射手座')
	d = ((1,20),(2,19),(3,21),(4,21),(5,21),(6,22),(7,23),(8,23),(9,23),(10,23),(11,23),(12,23))
	return n[len(filter(lambda y:y<=(month,day), d))%12]


def getmonthday(s):
	t = time.strptime(s, "%Y-%m-%d")
	y,m,d = t[0:3]
	print y
	print m
	print d
	return[m,d]
