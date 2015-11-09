#-*- coding: UTF-8 -*- 
from flask import Flask,jsonify,json
from flask import request
from flask import render_template
from flask import redirect
from models import *
from wtforms import Form,TextField,PasswordField,validators
from hashmd5 import *
import os, stat
from PIL import Image
import shutil
import string;
import datetime

app = Flask(__name__)


@app.route("/register",methods=['POST'])
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


@app.route("/login",methods=['POST'])
def login():
	try:
		username = request.json['username']
		password = request.json['password']
		u=User(username=username,password=password)
		if u.isExisted():
			state = 'successful'
			token = getTokeninformation(username).token
			reason = ''
			id = getuserinformation(token).id
		else:
			id=''
			state = 'fail'
			token = 'None'
			reason = '用户名密码错误'
	except Exception, e:
		state = 'fail'
		reason='异常'
		token = 'None'
		id = ''

	response = jsonify({'id':id,
						'state':state,
						'reason':reason,
						'token':token})
	return response



@app.route("/uploadavatar", methods=['POST'])
def uploadavatar():
	try:
		jsonstring = request.form.get('json')
		jsonstring = json.loads(jsonstring)
		token = jsonstring['token']
		type = jsonstring['type'] 
		number = jsonstring['number']
		id = getuserinformation(token).id
		src = request.form.get('avatar_path')
		#print avatar
		#avatar_type =  request.form.get('avatar_content_type').split('/')[-1]
		#print avatar_type
		try:
			if type=="0":
				dst = '/home/www/avatar/' + str(id)
			elif type=="1":
				dst = '/home/www/picture/qianshoudongda/' + str(id)+'-'+str(type)+'-'+str(number)
			elif type=="5":
				dst = '/home/www/picture/yaoda/' + str(id)+'-'+str(type)+'-'+str(number)
			elif type=="3":
				dst = '/home/www/picture/autumn-2/' + str(id)+'-'+str(type)+'-'+str(number)
			elif type =="4":
				dst = '/home/www/picture/autumn-3/' + str(id)+'-'+str(type)+'-'+str(number)
			elif type == "-1":
				dst = '/home/www/background/' + str(id) 
			else:
				dst = '/home/www/picture/temp/' + str(id)

			'''
			if os.path.exists(dst):
				os.remove(dst)
				os.remove(dst + '_thumbnail.jpg')
			'''

			shutil.move(src, dst)
			os.chmod(dst, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP  | stat.S_IROTH)
			if type =="0":
				fp = Image.open(dst)
				fp.thumbnail((100,100))
				fp.save(dst + '_thumbnail.jpg')
			state = 'successful'
			reason = ''
		except Exception, e:
			state = 'fail'
			reason = '上传图片失败,请重传'
	except Exception, e:
		id=''
		state = 'fail'
		reason='异常,请重传'


	response = jsonify({'id':id,
						'state':state,
						'reason':reason})
	return response




@app.route("/signup",methods=['POST'])
def signup():
	try:
		token = request.json['token']
		activity = request.json['activity']
		u=getuserinformation(token)

		if u!=None:
			if activity =='1':
				writestate = editDBcolumn(token,'qianshoudongda','yes')
			elif activity == '5':
				writestate=editDBcolumn(token,'yaoda','yes')
			elif activity == '3':
				writestate = editDBcolumn(token,'autumn2','yes')
			elif activity == '4':
				writestate = editDBcolumn(token,'autumn3','yes')
			else:
				writestate = 1
			if not writestate:
				state = 'successful'
				reason = ''
			else:
				state ='fail'
				reason ='异常，请重新报名'
		else:
			state = 'fail'
			reason = '用户不存在'


	except Exception, e:
		state = 'fail'
		reason = 'exception'

	response = jsonify({'state':state,
		                'reason':reason})
	return response



@app.route("/getactivityinformation",methods=['POST'])
def getactivityinformation():
	try:

		token = request.json['token']
		u=getuserinformation(token)
		act1 = getActivityInformation(5)
		act2 = getActivityInformation(1)
		act3 = getActivityInformation(3)
		act4 = getActivityInformation(4)

 		if u!=None:
 			if u.yaoda!='yes':
 				state1='no'
 			else:
 				state1='yes'

 			if u.qianshoudongda!='yes':
 				state2='no'
 			else:
 				state2='yes'

 			if u.autumn2!='yes':
 				state3='no'
 			else:
 				state3 = 'yes'

 			if u.autumn3!='yes':
 				state4='no'
 			else:
 				state4='yes'

 			if (act1!=None) and (act2!=None) and (act3!=None) and (act4!=None):
 				state = 'successful'
 				reason=''
 				title1 = act1.title if act1.title!=None else ''  
 				time1 = act1.time if act1.time!=None else ''
 				location1=act1.location if act1.location!=None else ''
 				number1=act1.number if act1.number!=None else ''

 				title2 = act2.title if act2.title!=None else ''  
 				time2 = act2.time if act2.time!=None else ''
 				location2=act2.location if act2.location!=None else ''
 				number2=act2.number if act2.number!=None else ''

 				title3 = act3.title if act3.title!=None else ''  
 				time3 = act3.time if act3.time!=None else ''
 				location3=act3.location if act3.location!=None else ''
 				number3=act3.number if act3.number!=None else ''

 				title4 = act4.title if act4.title!=None else ''  
 				time4 = act4.time if act4.time!=None else ''
 				location4=act4.location if act4.location!=None else ''
 				number4=act4.number if act4.number!=None else ''

			else:
				state = 'fail'
				reason = '活动不存在'
 				title1 = 'NoActivity'  
 				time1 =''
 				location1=''
 				number1=''

 				title2 =''  
 				time2 = ''
 				location2=''
 				number2=''

 				title3 =''  
 				time3 = ''
 				location3=''
 				number3=''

 				title4 =''  
 				time4 =''
 				location4=''
 				number4=''
 		else:

 			state = 'fail'
 			reason = '用户不存在'
			title1 = ''  
			time1 =''
			location1=''
			number1=''
			state1=''

			title2 =''  
			time2 = ''
			location2=''
			number2=''
			state2=''

			title3 =''  
			time3 = ''
			location3=''
			number3=''
			state3=''

			title4 =''  
			time4 =''
			location4=''
			number4=''
			state4=''



	except Exception, e:

		state = 'fail'
		reason = '异常'
		title1 = 'e'  
		time1 ='e'
		location1='e'
		number1='e'
		state1='e'

		title2 ='e'  
		time2 = 'e'
		location2='e'
		number2='e'
		state2='e'

		title3 ='e'  
		time3 = 'e'
		location3='e'
		number3='e'
		state3='e'

		title4 ='e'  
		time4 ='e'
		location4='e'
		number4='e'
		state4='e'


	response = jsonify({
							'result':[{
							'id':'5',
							'title':title1,
							'time':time1,
							'location':location1,
							'number':number1,
							'state':state1},
							{
							'id':'1',
							'title':title2,
							'time':time2,
							'location':location2,
							'number':number2,
							'state':state2},
	 	    				
							{  		
							'id':'3',					
							'title':title3,
							'time':time3,
							'location':location3,
							'number':number3,
							'state':state3},
							{
							'id':'4',
							'title':title4,
							'time':time4,
							'location':location4,
							'number':number4,
							'state':state4}],
							'reason':reason,
							'state':state 
							}
						)
	return response



@app.route("/editprofile/editschoolinformation",methods=['POST'])
def editschoolinformation():
	try:
		print 'hello'
		token = request.json[u'token']
		print token
		school = request.json['school']
		degree = request.json['degree']
		department = request.json['department']
		enrollment = request.json['enrollment']

		writestate = editschooldb(token,school,degree,department,enrollment)
		if not writestate:
			state = 'successful'
			reason = ''

		elif writestate == 2:
			state = 'fail'
			reason = 'no user'
		else:
			state = 'fail'
			reason = 'db error'

	except Exception, e:
		print e
		state = 'fail'
		reason ='异常'
	

	response = jsonify({'state':state,
		                'reason':reason})
	return response

@app.route("/editprofile/editpersonalinformation",methods=['POST'])
def editpersonalinformation():
	try:
		
		token = request.json[u'token']
		name = request.json['name']
		gender = request.json['gender']
		birthday = request.json['birthday']
		phone = request.json['phone']
		wechat = request.json.get('wechat',' ')
		qq = request.json.get('qq',' ')
		hometown = request.json.get('hometown',' ')

		writestate = editpersonaldb(token,name,gender,birthday,phone,wechat,qq,hometown)
		if not writestate:
			state = 'successful'
			reason = ''
		elif writestate == 2:
			state = 'fail'
			reason = 'no user'
		else:
			state = 'fail'
			reason = 'db error'

	except Exception, e:
		print e
		state = 'fail'
		reason ='异常'

	response = jsonify({'state':state,
		                'reason':reason})
	return response

@app.route("/editprofile/editpreferinformation",methods=['POST'])
def editpreferinformation():
	try:
		token = request.json['token']
		hobby = request.json['hobby']
		preference = request.json['preference']
		writestate = editpreferdb(token,hobby,preference)
		if not writestate:
			state = 'successful'
			reason = ''
		elif writestate == 2:
			state = 'fail'
			reason = 'no user'
		else:
			state = 'fail'
			reason = 'db error'

	except Exception, e:
		print e
		state = 'fail'
		reason ='异常'
	

	response = jsonify({'state':state,
		                'reason':reason})
	return response



@app.route("/getprofile",methods=['GET','POST'])
def getprofile():
		try:
			token = request.json['token']
			u=getuserinformation(token)
	 		if u!=None:
				state = 'successful'
				reason = ''
				username = u.username if u.username!=None else ''
				token = u.token if u.token!=None else ''    
				school = u.school if u.school!=None else '' 				
				degree = u.degree if u.degree!=None else ''
				department = u.department if u.department!=None else ''
				enrollment = u.enrollment if u.enrollment!=None else ''
				name = u.name if u.name!=None else ''
				gender = u.gender if u.gender!=None else ''
				birthday = u.birthday if u.birthday!=None else ''
				hobby = u.hobby if u.hobby!=None else ''
				preference = u.preference if u.preference!=None else '' 
				phone = u.phone if u.phone!=None else ''
				wechat = u.wechat if u.wechat != None else ''
				qq = u.qq if u.qq != None else ''
				hometown = u.hometown if u.hometown != None else ''
				id = u.id if u.id!=None else ''
				qianshoudongda = u.qianshoudongda if u.qianshoudongda!=None else ''
				autumn1 = u.autumn1 if u.autumn1!=None else ''
				autumn2 = u.autumn2 if u.autumn2!=None else ''
				autumn3 = u.autumn3 if u.autumn3!=None else ''
			else:
				state = 'fail'
				reason = '用户不存在'
				username = 'Nouser'
				token=''
				school=''
				degree=''
				department = ''
				enrollment = ''
				name = ''
				gender = ''
				birthday = ''
				hobby = ''
				preference = ''
				phone = ''
				wechat = ''
				qq =''
				hometown = ''
				id = ''
				qianshoudongda =''
				autumn1 = ''
				autumn2=''
				autumn3 = ''


		except Exception, e:
			state = 'fail'
			reason = '异常'	
			username='e'
			token=''
			school=''
			degree=''
			department = ''
			enrollment = ''
			name = ''
			gender = ''
			birthday = ''
			hobby = ''
			preference = ''
			phone = ''
			wechat = ''
			qq = ''
			hometown = ''
			id = ''
			qianshoudongda=''
			autumn1 = ''
			autumn2 = ''
			autumn3 = ''

			

		response = jsonify({'username':username,
							'token':token,
							'state':state,
							'reason':reason,
		 	                'school':school,
		 	                'degree':degree,
		 	                'department':department,
		 	                'enrollment':enrollment,
		 	                'name':name,
		 	                'gender':gender,
		 	                'birthday':birthday,
		 	                'preference':preference,
		 	                'hobby':hobby,
		 	                'phone':phone,
		 	                'wechat':wechat,
		 	                'qq':qq,
		 	                'hometown':hometown,
		 	                'id':id})
		return response


@app.route("/getprofilebyid",methods=['GET','POST'])
def getprofilebyid():
		try:
			id = request.json['id']
			u=getuserbyid(id)
	 		if u!=None:
				state = 'successful'
				reason = ''
				username = u.username if u.username!=None else ''
				token = u.token if u.token!=None else ''    
				school = u.school if u.school!=None else '' 				
				degree = u.degree if u.degree!=None else ''
				department = u.department if u.department!=None else ''
				enrollment = u.enrollment if u.enrollment!=None else ''
				name = u.name if u.name!=None else ''
				gender = u.gender if u.gender!=None else ''
				birthday = u.birthday if u.birthday!=None else ''
				hobby = u.hobby if u.hobby!=None else ''
				preference = u.preference if u.preference!=None else '' 
				phone = u.phone if u.phone!=None else ''
				wechat = u.wechat if u.wechat != None else ''
				qq = u.qq if u.qq !=None else ''
				hometown = u.hometown if u.hometown != None else ''
				id = u.id if u.id!=None else ''
				qianshoudongda = u.qianshoudongda if u.qianshoudongda!=None else ''
				autumn1 = u.autumn1 if u.autumn1!=None else ''
				autumn2 = u.autumn2 if u.autumn2!=None else ''
				autumn3 = u.autumn3 if u.autumn3!=None else ''
			else:
				state = 'fail'
				reason = '用户不存在'
				username = 'Nouser'
				token=''
				school=''
				degree=''
				department = ''
				enrollment = ''
				name = ''
				gender = ''
				birthday = ''
				hobby = ''
				preference = ''
				phone = ''
				wechat = ''
				qq = ''
				hometown = ''
				id = ''
				qianshoudongda =''
				autumn1 = ''
				autumn2=''
				autumn3 = ''


		except Exception, e:
			state = 'fail'
			reason = '异常'	
			username='e'
			token=''
			school=''
			degree=''
			department = ''
			enrollment = ''
			name = ''
			gender = ''
			birthday = ''
			hobby = ''
			preference = ''
			phone = ''
			wechat = ''
			qq = ''
			hometown = ''
			id = ''
			qianshoudongda=''
			autumn1 = ''
			autumn2 = ''
			autumn3 = ''

		response = jsonify({'username':username,
							'token':token,
							'state':state,
							'reason':reason,
		 	                'school':school,
		 	                'degree':degree,
		 	                'department':department,
		 	                'enrollment':enrollment,
		 	                'name':name,
		 	                'gender':gender,
		 	                'birthday':birthday,
		 	                'preference':preference,
		 	                'hobby':hobby,
		 	                'phone':phone,
		 	                'wechat':wechat,
		 	                'qq':qq,
		 	                'hometown':hometown,
		 	                'id':id})
		return response

@app.route("/follow",methods=['GET','POST'])
def follow():
	try:
		token = request.json['token']
		id = request.json['id']
		u=getuserinformation(token)
		u2=User.query.filter_by(id=id).first()
		if (u is not None) and (u2 is not None):
			temp = u.follow(u2);
			if temp == 0:
				state = 'successful'
				reason = ''
			elif temp==1:
				state = 'fail'
				reason = 'already follow';
			else:
				state='fail'
				reason='e'
		else:
			state = 'fail'
			reason = 'Nouser'

	except Exception, e:
			state = 'e'
			reason = 'e'

	response = jsonify({'state':state,
		                'reason':reason})
	return response

@app.route("/unfollow",methods=['GET','POST'])
def unfollow():
	try:
		token = request.json['token']
		id = request.json['id']
		u=getuserinformation(token)
		u2=User.query.filter_by(id=id).first()
		if (u is not None) and (u2 is not None):
			temp = u.unfollow(u2);
			if temp == 0:
				state = 'successful'
				reason = ''
			elif temp ==1:
				state = 'fail'
				reason = 'already unfollow'
			else:
				state='fail'
				reason = 'e';
		else:
			state = 'fail'
			reason = 'Nouser'

	except Exception, e:
			print e
			state = 'e'
			reason = 'e'

	response = jsonify({'state':state,
		                'reason':reason})
	return response

# show the users that follow me or I follow
@app.route("/followview", methods=['POST'])
def followers():
	try:
		token = request.json['token']
		u=getuserinformation(token)
		page = request.json['page']
		#print page
		x=string.atoi(page)
		#print x
		direct = request.json.get('direction', 'followers');
		#print direct 
		if u is not None:
			if direct == 'followers':
				pageitems = u.followers.paginate(x, per_page=10, error_out=False)
				followview = [{'id':item.follower.id,'name':item.follower.name if item.follower.name!=None else '','gender':item.follower.gender if item.follower.gender!=None else '','school':item.follower.school if item.follower.school!=None else '','timestamp':item.timestamp} for item in pageitems.items]
			else:
				pageitems = u.followeds.paginate(x, per_page=10, error_out=False)
				followview = [{'id':item.followed.id, 'name':item.followed.name if item.followed.name!=None else '','gender':item.followed.gender if item.followed.gender!=None else '','school':item.followed.school if item.followed.school!=None else '','timestamp':item.timestamp} for item in pageitems.items]
			#print followview
			state = 'successful'
			reason = ''
		else:
			state = 'fail'
			followview = {};
			reason = 'User not exist'

	except Exception ,e:
		state = 'fail'
		followview = {};
		reason = 'e'
		direct=''

	response = jsonify({'state':state,
						'reason':reason,
						'result': followview})
	return response;

@app.route("/getrecommenduser",methods=['GET','POST'])
def getrecommenduser():
		try:
			token = request.json['token']
			u=getuserinformation(token)
	 		if u != None:
				L = getranduser(token)
				if len(L)>0:
					state = 'successful'
					reason = ''
					result = [{"id":getuserbyid(recommend).id,"name":getuserbyid(recommend).name,"gender":getuserbyid(recommend).gender,"school":getuserbyid(recommend).school} for recommend in L]
					response = jsonify({'state':state,
										'reason':reason,
										'result':result
					 	                })
				else:
					state = 'fail'
					reason = 'no gender'
					response = jsonify({'state':state,
										'reason':reason,
										'result':[]
										})
			else:
				state = 'fail'
				reason = 'Nouser'
				response = jsonify({'state':state,
									'reason':reason,
									'result':[]
									})

		except Exception, e:
			print e
			state = 'fail'
			reason = 'e'	
			response = jsonify({'state':state,
								'reason':reason,
								'result':[]
								})
		return response

@app.route("/searchuser",methods = ['GET','POST'])
def searchuser():
	try:
		token = request.json['token']
		text = request.json['text']
		u = getuserinformation(token)
		if u != None:
			L = []
			temp = getuserbyid(text)
			L.append(temp)
			if temp != None:
				state = "successful"
				reason = ''
				result = [{"id":search.id,"name":search.name,"gender":search.gender,"school":search.school} for search in L]
			else:
				tempname = getuserbyname(text)
				L = []
				L.append(tempname)
				if tempname != None:
					state = "successful"
					reason = ''
					result = [{"id":search.id,"name":search.name,"gender":search.gender,"school":search.school} for search in L]

		else:
			state = 'fail'
			reason = 'no user'
			result = [];

	except Exception, e:
		print e
		state = 'fail'
		reason = 'exception'
		result = []

	response = jsonify({'state':state,
						'reason':reason,
						'result':result})
	return response


@app.route("/sendmessage",methods = ['POST'])
def sendmessage():
	try:
		token = request.json['token']
		text = request.json.get('text','')
		RecId = request.json.get('RecId','-1')
		u = getuserinformation(token)
		if u != None:
			SendId = u.id
			messageContentTemp = MessageContent(text = text)
			messageTemp = Message(SendId = SendId, RecId = RecId, messagecontents = messageContentTemp)
			messageContentTemp.add()		
			messageTemp.add()
			id = messageTemp.id
			state = 'successful'
			reason = ''

		else:
			state = 'fail'
			reason = 'no user'
			id = ''
	
		
	except Exception, e:
		print e
		state = 'fail'
		reason = 'exception'
		id = ''

	response = jsonify({'id':id,
						'state':state,
						'reason':reason})
	return response

@app.route("/readmessage",methods = ['POST'])
def readmessage():
	try:
		token = request.json['token']
		id = request.json.get('id','')
		u = getuserinformation(token)
		m = getMessagebyid(id)
		if u != None:
			print 'sss'
			m.state = 0
			m.add()			
			state = 'successful'
			reason = ''

		else:
			state = 'fail'
			reason = 'no user'
	
		
	except Exception, e:
		print e
		state = 'fail'
		reason = 'exception'

	response = jsonify({'state':state,
						'reason':reason})
	return response
@app.route("/getSendUserList",methods = ['POST'])
def getSendUserList():
	try:
		token = request.json['token']
		u = getuserinformation(token)
		if u != None:
			id = u.id
			m = getMessageList(id)
			L = [x.SendId for x in m]
			L = list(set(L))
			result = []
			for i in range(len(L)):
				unReadnum = 0
				SendId = L[i]
				mSendi = getMessageTwoid(SendId,id)
				mSendi.reverse()
				text = mSendi[0].messagecontents.text
				for j in range(len(mSendi)):
					if mSendi[j].state == '1':
						unReadnum=unReadnum+1
				senduser = getuserbyid(SendId)
				output = {"SendId":SendId,"unreadnum":unReadnum,"name":senduser.name,"gender":senduser.gender,"school":senduser.school,"text":text}
				result.append(output)
			state = 'successful'
			reason = ''

		else:
			state = 'fail'
			reason = 'no user'
			result = ''
	
		
	except Exception, e:
		print e
		state = 'fail'
		reason = 'exception'
		result = ''

	response = jsonify({'state':state,
						'reason':reason,
						'result':result})
	return response

@app.route("/getMessageDetailList", methods = ['POST'])
def getMessageDetailList():
	try:
		token = request.json['token']
		SendId = request.json['SendId']
		page = request.json['page']
		#print page
		x=string.atoi(page)
		u = getuserinformation(token)
		if u != None:
			id = u.id
			result = []
			senduser = getuserbyid(SendId)
			pageitems = getMessageTwoidPage(SendId,id,x)
			L = pageitems.items
			for i in range(len(L)):
				text = L[i].messagecontents.text
				image = L[i].messagecontents.image
				vedio = L[i].messagecontents.vedio
				time = L[i].sendtime
				readstate = L[i].state
				output = {"text":text,"image":image,"vedio":vedio,"time":time,"readstate":readstate}
				result.append(output)
			name = senduser.name
			gender = senduser.gender
			school = senduser.school
			state = 'successful'
			reason = ''

		else:
			state = 'fail'
			reason = 'no user'
			result = ''
	except Exception, e:
		print e
		state = 'fail'
		reason = 'exception'
		result = ''

	response = jsonify({'state':state,
						'reason':reason,
						'SendId':SendId,
						'name':name,
						'gender':gender,
						'school':school,
						'result':result})
	return response

if __name__ == '__main__':
	app.run(host=os.getenv('IP','0.0.0.0'),port=int(os.getenv('PORT',8080)))
