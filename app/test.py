#-*- coding: UTF-8 -*- 
from models import *
from hashmd5 import *

"""
name = '，'
tname = '%'+name+'%'
print name
u=User.query.filter(User.name.like(tname))
for temp in u:
	print temp.name

"""
"""
a = Activity.query.filter_by(id =1).first()
u = User.query.filter_by(id = 72).first()
m = imageURL.query.filter_by(id = 1).first()

a.addlifeimage(u,m)
"""

password = "12345678"
pwd = generatemd5(password)
print pwd

#计算星座
def Zodiac(month, day):
	n = (u'摩羯座',u'水瓶座',u'双鱼座',u'白羊座',u'金牛座',u'双子座',u'巨蟹座',u'狮子座',u'处女座',u'天秤座',u'天蝎座',u'射手座')
	d = ((1,20),(2,19),(3,21),(4,21),(5,21),(6,22),(7,23),(8,23),(9,23),(10,23),(11,23),(12,23))
	return n[len(filter(lambda y:y<=(month,day), d))%12]
