#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
from hashmd5 import *
check_page = Blueprint('check_page', __name__)

@check_page.route('/', methods = ["GET","POST"])
@check_page.route('/<page>')
@check_page.route("/register",methods=['POST'])
def register():
	try:
		username=request.json[u'username']
		temp = checkName(username)
		if temp==False:		
			response = jsonify({
								'id':'',
								'state':'fail',
								'reason':'用户名不能包含中文且至少要两个字母',
								'token':'chinese'})
			return response
		password=request.json['password']
		token= hashToken(username,password)
		u=User(username=username,password=password,token=token)
		temp=u.add()
		print temp
		if temp==0:
			state = 'successful'
			reason = ''
			token = hashToken(username,password)
			id = getuserinformation(token).id
		else:
			state = 'fail'
			reason = '用户名已被注册'
			token = 'Haveresiger'
			id=''
	except Exception, e:
		print e
		state = 'fail'
		reason ='异常'
		token = 'exception'
		id=''

	response = jsonify({
						'id':id,
						'state':state,
						'reason':reason,
						'token':token})
	return response


@check_page.route("/login",methods=['POST'])
def login():
	try:
		username = request.json['username']
		password = request.json['password']
		print "in1"
		u=User(username=username,password=password)
		if u.isExisted():
			print "in success"
			state = 'successful'
			tmp = getTokeninformation(username)
			token = tmp.token
			id = tmp.id
			reason = ''
		else:
			print "in3"
			tempuser = User.query.filter_by(username=username).first()
			if tempuser != None:
				print "in4"
				pwd = generatemd5(tempuser.password)
				if pwd == password:
					state = 'successful'
					token = tempuser.token
					reason = ''
					id = tempuser.id
					tempuser.password = pwd
					tempuser.addpwd()
				else:
					id=''
					state = 'fail'
					token = 'None'
					reason = '用户名密码错误'
			else:
				id=''
				state = 'fail'
				token = 'None'
				reason = '用户名密码错误'
	except Exception, e:
		print "login error!!"
		print e
		state = 'fail'
		reason='服务器异常'
		token = 'None'
		id = ''

	response = jsonify({'id':id,
						'state':state,
						'reason':reason,
						'token':token})
	return response

