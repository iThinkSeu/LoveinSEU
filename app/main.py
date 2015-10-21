#-*- coding: UTF-8 -*- 
from flask import Flask,jsonify,json
from flask import request
from flask import render_template
from flask import redirect
from models import *
from wtforms import Form,TextField,PasswordField,validators
from hashmd5 import hashToken
import os, stat
from PIL import Image
import shutil

app = Flask(__name__)


@app.route("/register",methods=['POST'])
def register():
	try:
		username=request.json['username']
		password=request.json['password']
		token= hashToken(username,password)
		u=User(username=username,password=password,token=token)
		temp=u.add()
		print temp
		if temp==0:
			state = 'successful'
			reason = ''
			token = hashToken(username,password)
			id=u.id
		else:
			state = 'fail'
			reason = '用户名已被注册'
			token = 'Haveresiger'
			id=''
	except Exception, e:
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


@app.route("/uploadavatar", methods=['POST'])
def uploadavatar():
	try:
		jsonstring = request.form.get('json')
		jsonstring = json.loads(jsonstring)
		token = jsonstring['token']
		type = jsonstring['type'] 
		id = getuserinformation(token).id
		src = request.form.get('avatar_path')
		#print avatar
		#avatar_type =  request.form.get('avatar_content_type').split('/')[-1]
		#print avatar_type
		try:
			if type=="0":
				dst = '/home/www/avatar/' + str(id)
			elif type=="1":
				dst = '/home/www/picture/qianshoudongda/' + str(id)
			elif type=="2":
				dst = '/home/www/picture/autumn-1/' + str(id)
			elif type=="3":
				dst = '/home/www/picture/autumn-2' + str(id)
			elif type =="4":
				dst = '/home/www/picture/autumn-2' + str(id)
			else:
				dst = '/home/www/avatar/' + str(id)

			'''
			if os.path.exists(dst):
				os.remove(dst)
				os.remove(dst + '_thumbnail.jpg')
			'''

			shutil.move(src, dst)
			os.chmod(dst, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP  | stat.S_IROTH)
			if type =="1":
				fp = Image.open(dst)
				fp.thumbnail((100,100))
				fp.save(dst + '_thumbnail.jpg')
			state = 'successful'
			reason = ''
		except Exception, e:
			state = 'fail'
			reason = '非图片文件'
	except Exception, e:
		id=''
		state = 'fail'
		reason='异常'


	response = jsonify({'id':id,
						'state':state,
						'reason':reason})
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
			id = u.id
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



@app.route("/signup",methods=['POST'])
def signup():
	try:
		print "sign"
		token = request.json['token']
		activity = request.json['activity']
		u=getuserinformation(token)

		if u!=None:
			if activity=='1':
				if u.qianshoudongda!='yes':
					writestate=editDBcolumn(token,'qianshoudongda','yes')
				else:
					writestate=2
			elif activity == '2':
				if u.autumn1!='yes':
					writestate=editDBcolumn(token,'autumn1','yes')
				else:
					writestate=2

			elif activity == '3':
				if u.autumn2!='yes':
					writestate=editDBcolumn(token,'autumn2','yes')
				else:
					writestate=2
			elif activity == '4':
				if u.autumn3!='yes':
					writestate=editDBcolumn(token,'autumn3','yes')
				else:
					writestate=2
			else:
				writestate = 1

			if not writestate:
				state = 'successful'
				reason = ''
			elif writestate==2:
				state = 'fail'
				reason = '已报名'
			else:
				state='fail'
				reason='无此活动'

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
		act1 = getActivityInformation(1)
		act2 = getActivityInformation(2)
		act3 = getActivityInformation(3)
		act4 = getActivityInformation(4)

 		if u!=None:
 			if u.qianshoudongda!='yes':
 				state1='no'
 			else:
 				state1='yes'

 			if u.autumn1!='yes':
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
 				title1 = act1.title if act1.title!=None else 'None'  
 				time1 = act1.time if act1.time!=None else 'None'
 				location1=act1.location if act1.location!=None else 'None'
 				number1=act1.number if act1.number!=None else 'None'

 				title2 = act2.title if act2.title!=None else 'None'  
 				time2 = act2.time if act2.time!=None else 'None'
 				location2=act2.location if act2.location!=None else 'None'
 				number2=act2.number if act2.number!=None else 'None'

 				title3 = act3.title if act3.title!=None else 'None'  
 				time3 = act3.time if act3.time!=None else 'None'
 				location3=act3.location if act3.location!=None else 'None'
 				number3=act3.number if act3.number!=None else 'None'

 				title4 = act4.title if act4.title!=None else 'None'  
 				time4 = act4.time if act4.time!=None else 'None'
 				location4=act4.location if act4.location!=None else 'None'
 				number4=act4.number if act4.number!=None else 'None'

			else:
				state = 'fail'
				reason = '活动不存在'
 				title1 = 'NoActivity'  
 				time1 ='NoActivity'
 				location1='NoActivity'
 				number1='NoActivity'

 				title2 ='NoActivity'  
 				time2 = 'NoActivity'
 				location2='NoActivity'
 				number2='NoActivity'

 				title3 ='NoActivity'  
 				time3 = 'NoActivity'
 				location3='NoActivity'
 				number3='NoActivity'

 				title4 ='NoActivity'  
 				time4 ='NoActivity'
 				location4='NoActivity'
 				number4='NoActivity'
 		else:

 			state = 'fail'
 			reason = '用户不存在'
			title1 = 'Nouser'  
			time1 ='Nouser'
			location1='Nouser'
			number1='Nouser'
			state1='Nouser'

			title2 ='Nouser'  
			time2 = 'Nouser'
			location2='Nouser'
			number2='Nouser'
			state2='Nouser'

			title3 ='Nouser'  
			time3 = 'Nouser'
			location3='Nouser'
			number3='Nouser'
			state3='Nouser'

			title4 ='Nouser'  
			time4 ='Nouser'
			location4='Nouser'
			number4='Nouser'
			state4='Nouser'



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
							'id':'1',
							'title':title1,
							'time':time1,
							'location':location1,
							'number':number1,
							'state':state1},
							{
							'id':'2',
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
		print "editschool"
		token = request.json['token']
		school = request.json['school']
		degree = request.json['degree']
		department = request.json['department']
		enrollment = request.json['enrollment']

		writestate_school = editDBcolumn(token,'school',school)
		writestate_degree = editDBcolumn(token,'degree',degree)
		writestate_department=editDBcolumn(token,'department',department)
		writestate_enrollment=editDBcolumn(token,'enrollment',enrollment)
		if not (writestate_school or writestate_degree or writestate_department or writestate_enrollment):
			state = 'successful'
			reason = ''
		else:
			state = 'fail'
			reason = '用户不存在'
		print token
		print school
		# state='s'
		# reason= 'r'
	except Exception, e:
		state = 'fail'
		reason ='异常'
	

	response = jsonify({'state':state,
		                'reason':reason})
	return response

@app.route("/editprofile/editpersonalinformation",methods=['POST'])
def editpersonalinformation():
	try:
		print "Editpersonal"
		token = request.json['token']
		name = request.json['name']
		gender = request.json['gender']
		birthday = request.json['birthday']
		phone = request.json['phone']

		writestate_name=editDBcolumn(token,'name',name)
		writestate_gender=editDBcolumn(token,'gender',gender)
		writestate_birthday=editDBcolumn(token,'birthday',birthday)
		writestate_phone = editDBcolumn(token,'phone',phone)
		if not (writestate_name or writestate_gender or writestate_birthday or writestate_phone):
			state = 'successful'
			reason = ''
		else:
			state = 'fail'
			reason = '用户不存在'
		print token
	except Exception, e:
		state = 'fail'
		reason ='异常'
	

	response = jsonify({'state':state,
		                'reason':reason})
	return response

@app.route("/editprofile/editpreferinformation",methods=['POST'])
def editpreferinformation():
	try:
		print "Editprefer"
		token = request.json['token']
		hobby = request.json['hobby']
		preference = request.json['preference']

		writestate_hobby=editDBcolumn(token,'hobby',hobby)
		writestate_preference=editDBcolumn(token,'preference',preference)
		if not (writestate_hobby or writestate_preference):
			state = 'successful'
			reason = ''
		else:
			state = 'fail'
			reason = '用户不存在'
		print token
	except Exception, e:
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
				username = u.username if u.username!=None else 'None'
				token = u.token if u.token!=None else 'None'    
				school = u.school if u.school!=None else 'None' 				
				degree = u.degree if u.degree!=None else 'None'
				department = u.department if u.department!=None else 'None'
				enrollment = u.enrollment if u.enrollment!=None else 'None'
				name = u.name if u.name!=None else 'None'
				gender = u.gender if u.gender!=None else 'None'
				birthday = u.birthday if u.birthday!=None else 'None'
				hobby = u.hobby if u.hobby!=None else 'None'
				preference = u.preference if u.preference!=None else 'None' 
				phone = u.phone if u.phone!=None else 'None'
				id = u.id if u.id!=None else 'None'
				qianshoudongda = u.qianshoudongda if u.qianshoudongda!=None else 'None'
				autumn1 = u.autumn1 if u.autumn1!=None else 'None'
				autumn2 = u.autumn2 if u.autumn2!=None else 'None'
				autumn3 = u.autumn3 if u.autumn3!=None else 'None'
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
		 	                'id':id})
		return response




if __name__ == '__main__':
	app.run(host=os.getenv('IP','0.0.0.0'),port=int(os.getenv('PORT',8080)),debug=True)
