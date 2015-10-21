from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
#from flask.ext.sqlalchemy import SQLALchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="mysql://admin:admin@123.57.2.8:3306/flasktestdb?charset=utf8"

db = SQLAlchemy(app)

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
	hobby = db.Column(db.String(128))
	preference = db.Column(db.String(128))
	qianshoudongda = db.Column(db.String(32))
	autumn1=db.Column(db.String(32))
	autumn2=db.Column(db.String(32))
	autumn3=db.Column(db.String(32))


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

class Activity(db.Model):
	__tablename__="activitys"
	id = db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(32),primary_key=True)
	time=db.Column(db.String(32))
	location=db.Column(db.String(32))
	number=db.Column(db.String(32))
	state = db.Column(db.String(32))

	
		


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
	
def getActivityInformation(id):
	a=Activity.query.filter_by(id=id).first()
	return a 


