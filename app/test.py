
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