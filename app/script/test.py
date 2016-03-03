
from tmodels import *

a = getpostcommentactbylimit(4,3)

for aa in a:
	print aa.id

username = 'ithinker'
password = '123456'
u = User(username=username,password=password)
print u.isExistedusername()