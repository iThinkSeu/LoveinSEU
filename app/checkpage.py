#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
from hashmd5 import *
from sendMsg import *
import traceback
import sys
check_page = Blueprint('check_page', __name__)


@check_page.route('/sendsmscode', methods=['POST'])
def send_sms_code():
	try:
		phone = request.json['phone']
		type_flag = request.json['type']
		u = User.query.filter_by(username=phone).first()
		if u or str(type_flag) == '1':
			state = 'successful'
			reason = ''
			code = str(random.randint(100000, 999999))
			if str(type_flag) == '1' or str(type_flag) == '2':
				rv = send_sms_code_by_type(str(phone), code, str(type_flag))
				if rv != 0:
					state = 'fail'
					reason = '验证码发送失败'
				else:
					p = checkMsg.query.filter_by(phone = str(phone)).first()
					if p is None:
						sms_code = checkMsg(phone=str(phone), code=code)
						sms_code.add()
					else:
						p.code = code
						p.timestamp = datetime.now()
						p.add()
			else:
				state = 'fail'
				reason = 'invalid'
		else:
			state = 'fail'
			reason = '该手机号尚未注册'
	except Exception, e:
		print e
		state = 'fail'
		reason = '服务器异常'

	print state, reason
	return jsonify({'state':state, 'reason':reason})

@check_page.route('/registerphone', methods=['POST'])
def register_user():
	try:
		id = ''
		token = ''
		phone = request.json['phone']
		password = request.json['password']
		code = request.json['code']
		u = User.query.filter_by(username = str(phone)).first()
		if u is None:
			p = checkMsg.query.filter_by(phone=str(phone)).first()
			if p is None or p.code != str(code) or (datetime.now()-p.timestamp > timedelta(minutes=5)):
				state = 'fail'
				reason = '验证码无效'
			else:
				state = 'successful'
				reason = ''
				token = hashToken(str(phone), password+str(code))
				u = User(username = phone, password = password, token = token, phone = phone)
				u.add()
				id = getuserinformation(token).id


		else:
			state  = 'fail'
			reason = '该手机号已被注册'
	except Exception, e:
		print e
		state = 'fail'
		reason = '服务器异常'

	return jsonify({'state':state, 'reason':reason, 'token':token, 'id':id})

@check_page.route('/resetpassword', methods=['POST'])
def reset_password():
	try:
		id = ''
		token = ''
		phone = request.json['phone']
		password = request.json['password']
		code = request.json['code']
		u = User.query.filter_by(username = str(phone)).first()
		if u is not None:
			p = checkMsg.query.filter_by(phone=str(phone)).first()
			if p is None or p.code != str(code) or (datetime.now()-p.timestamp > timedelta(minutes=5)):
				state = 'fail'
				reason = '验证码无效'
			else:
				state = 'successful'
				reason = ''
				token = hashToken(str(phone), password+str(code))
				u.password = password
				u.token = token
				id = u.id
				try:
					db.session.add(u)
					db.session.commit()
				except Exception, e:
					print e
					db.session.rollback()

		else:
			state  = 'fail'
			reason = '该手机号尚未被注册'

	except Exception, e:
		print e
		state = 'fail'
		reason = '服务器异常'
	return jsonify({'state':state, 'reason':reason, 'token':token, 'id':id})




@check_page.route('/', methods = ["GET","POST"])
@check_page.route('/<page>')
@check_page.route("/register",methods=['POST'])
def register():
	try:
		"""
		username=request.json[u'username']
		password=request.json['password']
		temp = checkName(username)
		if temp==False:		
			response = jsonify({
								'id':'',
								'state':'fail',
								'reason':'用户名不能包含中文且至少要两个字母',
								'token':'chinese'})
			return response
		token= hashToken(username,password)
		u=User(username=username,password=password,token=token)
		if u.isExistedusername() == 0:
			##未完成，加code验证码判断相关逻辑
			u.add()
			state = 'successful'
			reason = ''
			token = hashToken(username,password)
			id = getuserinformation(token).id
		else:
			state = 'fail'
			reason = '用户名已被注册'
			token = 'Haveresiger'
			id=''
		"""
		state = "fail"
		reason = "旧版已废弃，请升级至最新版本（weme.space可下载）"
		id = ''
		token = ''
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
		u=User(username=username,password=password)
		gender = ''
		if u.isExisted():
			state = 'successful'
			tmp = getTokeninformation(username)
			token = tmp.token
			gender = tmp.gender
			id = tmp.id
			reason = ''
		else:
			tempuser = User.query.filter_by(username=username).first()
			if tempuser != None:
				pwd = generatemd5(tempuser.password)
				if pwd == password:
					state = 'successful'
					token = tempuser.token
					reason = ''
					id = tempuser.id
					tempuser.password = pwd
					tempuser.addpwd()
					gender = tempuser.gender
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
						'gender':gender,
						'state':state,
						'reason':reason,
						'token':token})
	#print state, reason
	return response

@check_page.route("/testhello",methods=["GET","POST"])
def testhello():
	return "hello world"

@check_page.route("/testdb",methods=["GET","POST"])
def testdb():
	try:
		username = "ithinker"
		password = "25d55ad283aa400af464c76d713c07ad"
		u=User(username=username,password=password)
		gender = ''
		if u.isExisted():
			state = 'successful'
			tmp = getTokeninformation(username)
			token = tmp.token
			gender = tmp.gender
			id = tmp.id
			reason = ''
		else:
			tempuser = User.query.filter_by(username=username).first()
			if tempuser != None:
				pwd = generatemd5(tempuser.password)
				if pwd == password:
					state = 'successful'
					token = tempuser.token
					reason = ''
					id = tempuser.id
					tempuser.password = pwd
					tempuser.addpwd()
					gender = tempuser.gender
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
						'gender':gender,
						'state':state,
						'reason':reason,
						'token':token})
	#print state, reason
	return response



