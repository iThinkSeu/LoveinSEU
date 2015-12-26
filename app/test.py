
#-*- coding: UTF-8 -*- 
from models import *

name = '，'
tname = '%'+name+'%'
print name
u=User.query.filter(User.name.like(tname))
for temp in u:
	print temp.name

