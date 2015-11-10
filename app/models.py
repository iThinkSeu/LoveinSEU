# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import *
import random
from sqlalchemy import or_
from sqlalchemy import and_

#from flask.ext.sqlalchemy import SQLALchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:SEUqianshou2015@218.244.147.240:3306/flasktestdb?charset=utf8"
#app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:SEUqianshou2015@101.200.201.22:3306/flasktestdb?charset=utf8"

db = SQLAlchemy(app)

class Follow(db.Model):
	__tablename__='follows'
	follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
	followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
	timestamp = db.Column(db.DateTime, default = datetime.now)


class User(db.Model):
	__tablename__='users'
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(32),unique = True)
	password = db.Column(db.String(32))
	token = db.Column(db.String(32))
	school = db.Column(db.String(32))
	degree = db.Column(db.String(32))
	department = db.Column(db.String(32))
	enrollment = db.Column(db.String(32))
	name = db.Column(db.String(32))
	gender = db.Column(db.String(32))
	phone = db.Column(db.String(32))
	birthday = db.Column(db.String(32))
	wechat = db.Column(db.String(32))
	qq = db.Column(db.String(32))
	hometown = db.Column(db.String(32))
	hobby = db.Column(db.String(128))
	preference = db.Column(db.String(128))
	qianshoudongda = db.Column(db.String(32))
	autumn1=db.Column(db.String(32))
	autumn2=db.Column(db.String(32))
	autumn3=db.Column(db.String(32))
	yaoda = db.Column(db.String(32))

	#relation
	#all users followed by this
	followeds = db.relationship('Follow', foreign_keys = [Follow.follower_id], backref = db.backref('follower', lazy='joined'), lazy='dynamic', cascade = 'all, delete-orphan')
	#all users that follow this
	followers = db.relationship('Follow', foreign_keys = [Follow.followed_id], backref = db.backref('followed', lazy='joined'), lazy='dynamic', cascade = 'all, delete-orphan')


	def add(self):
		try:
			
			tempuser = User.query.filter_by(username=self.username).first()
			if tempuser is None:
				db.session.add(self)
				db.session.commit()
				return 0
			else:
				return 1

		except Exception, e:
			db.session.rollback()
			return 2
		
	def isExisted(self):
		tempuser = User.query.filter_by(username=self.username,password=self.password).first()
		if tempuser is None:
			return 0
		else:
			return 1

	def is_following(self, user):
		u=self.followeds.filter_by(followed_id=user.id).first()
		return  u is not None

	def is_followed_by(self, user):
		return self.followers.filter_by(follower_id=user.id).first() is not None

	def follow(self, user):
		try:
			if not self.is_following(user):
				f = Follow(follower=self, followed=user)
				db.session.add(f)
				db.session.commit()
				return 0
			else:
				return 1	
		except Exception, e:
			db.session.rollback()
			return 2

	def unfollow(self, user):
		try:
			f = self.followeds.filter_by(followed_id=user.id).first()
			if f:
				db.session.delete(f)
				db.session.commit()
				return 0
			else:
				return 1
		except Exception, e:
			db.session.rollback()
			return 2


class Activity(db.Model):
	__tablename__="activitys"
	id = db.Column(db.Integer,primary_key=True)
	rank = db.Column(db.String(32),unique = True)
	title=db.Column(db.String(32),primary_key=True)
	time=db.Column(db.String(32))
	location=db.Column(db.String(32))
	number=db.Column(db.String(32))
	state = db.Column(db.String(32))


class Message(db.Model):
	__tablename__ = "Message"
	id = db.Column(db.Integer,primary_key = True)
	SendId = db.Column(db.String(32))
	RecId = db.Column(db.String(32))
	MessageId = db.Column(db.Integer, db.ForeignKey('MessageContent.id'))
	state = db.Column(db.String(32),default = '1')
	sendtime = db.Column(db.DateTime, default = datetime.now)

	def add(self):
		try:
			db.session.add(self)
			db.session.commit()
		except Exception, e:
			db.session.rollback()
			return 2


class MessageContent(db.Model):
	__tablename__ = "MessageContent"
	id = db.Column(db.Integer,primary_key = True)
	text = db.Column(db.String(128))
	image = db.Column(db.String(32))
	vedio = db.Column(db.String(32))
	messages = db.relationship('Message',backref = 'messagecontents')

	def add(self):
		try:
			db.session.add(self)
			db.session.commit()
		except Exception, e:
			db.session.rollback()
			return 2

class ImageURL(db.Model):
	__tablename__ = "ImageURL"
	id = db.Column(db.Integer,primary_key = True)
	image1 = db.Column(db.String(32))
	image2 = db.Column(db.String(32))
	image3 = db.Column(db.String(32))
	image4 = db.Column(db.String(32))
	image5 = db.Column(db.String(32))
	image6 = db.Column(db.String(32))
	image7 = db.Column(db.String(32))

			
def editschooldb(token,school,degree,department,enrollment):
	u=User.query.filter_by(token=token).first()
	if u!=None:
		u.school = school
		u.degree = degree
		u.department = department
		u.enrollment = enrollment
		try:
			db.session.add(u)
			db.session.commit()
			return 0
		except Exception, e:
			db.session.rollback()
			return 1   
	else:
		return 2 

def editpersonaldb(token,name,gender,birthday,phone,wechat,qq,hometown):
	u=User.query.filter_by(token=token).first()
	if u!=None:
		u.name = name
		u.gender = gender
		u.birthday = birthday
		u.phone = phone
		u.wechat = wechat
		u.qq = qq 
		u.hometown = hometown
		try:
			db.session.add(u)
			db.session.commit()
			return 0
		except Exception, e:
			db.session.rollback()
			return 1
	else:
		return 2 

def editpreferdb(token,hobby,preference):
	u=User.query.filter_by(token=token).first()
	if u!=None:
		u.hobby = hobby
		u.preference = preference
		try:
			db.session.add(u)
			db.session.commit()
			return 0
		except Exception, e:
			db.session.rollback()
			return 1   
	else:
		return 2 



def editDBcolumn(token,modifycol,valuecol):
	u=User.query.filter_by(token=token).first()
	#if modifycol=='password':
	#return valuecol
	if u!=None:
		if modifycol=='password':
			u.password = valuecol
		if modifycol=='school':
			u.school = valuecol
		if modifycol=='degree':
			u.degree = valuecol
		if modifycol=='department':
			u.department = valuecol
		if modifycol=='enrollment':
			u.enrollment = valuecol
		if modifycol=='name':
			u.name = valuecol
		if modifycol=='gender':
			u.gender = valuecol
		if modifycol=='birthday':
			u.birthday = valuecol	
		if modifycol=='hobby':
			u.hobby = valuecol
		if modifycol=='preference':
			u.preference = valuecol
		if modifycol=='qianshoudongda':
			u.qianshoudongda = valuecol
		if modifycol=='autumn1':
			u.autumn1=valuecol
		if modifycol=='autumn2':
			u.autumn2=valuecol
		if modifycol=='autumn3':
			u.autumn3=valuecol
		if modifycol=='phone':
			u.phone=valuecol
		if modifycol == 'yaoda':
			u.yaoda = valuecol
			
	else:#
		return 1 

	try:
		db.session.add(u)
		db.session.commit()
		return 0
	except Exception, e:
		db.session.rollback()
		return 1   
	

def getuserinformation(token):
	u=User.query.filter_by(token=token).first()
	return u 

def getTokeninformation(username):
	u=User.query.filter_by(username=username).first()
	return u 

def getuserbyid(id):
	u=User.query.filter_by(id=id).first()
	return u 

def getuserbyname(name):
	u=User.query.filter_by(name=name).first()
	return u 			

	
def getActivityInformation(id):
	a = Activity.query.filter_by(id = id).first()
	return a 

def getranduser(token):
	u = getuserinformation(token)
	gender = u.gender

	if gender == u'男':
		udif = User.query.filter_by(gender=u"女").all()
	else:
		udif = User.query.filter_by(gender=u"男").all()

	L1 = [x.id for x in udif]
	f2 = u.followeds.all()
	L2 = [y.followed_id for y in f2]
	L = list(set(L1).difference(set(L2)))
	if len(L)>7:	
		return random.sample(L,8)
	elif len(L)==0:
		return []
	else:
		return L

def getMessagebyid(id):
	a = Message.query.filter_by(id = id).first()
	return a 

def getMessageList(RecId):
	a = Message.query.filter_by(RecId = RecId).all()
	return a

def getMessageTwoid(SendId, RecId):
	a = Message.query.filter_by(SendId = SendId, RecId = RecId).all()
	return a

#
def getMessageTwoidPage(SendId, RecId, page):
	m = Message.query.filter(or_(and_(Message.SendId == SendId, Message.RecId == RecId), and_(Message.SendId == RecId, Message.RecId == SendId))).order_by(Message.sendtime.desc()).paginate(page, per_page=5, error_out=False)
	return m
