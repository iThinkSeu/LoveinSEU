
#test
from models import *
comment1 = comment.query.filter_by(id=1).first()
u1= User.query.filter_by(id=2).first()
post1 = post.query.filter_by(id=2).first()
topic1 = topic.query.filter_by(id=1).first()


u1.publishpost(post1)
