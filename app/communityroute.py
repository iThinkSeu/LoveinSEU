#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
import models 
from hashmd5 import *
import string
community_route = Blueprint('community_route', __name__)

@community_route.route("/publishpost",methods=['POST'])
def pubishpost():
	try:
		token = request.json['token']
		title = request.json.get('title','')
		body = request.json.get('body','')
		topicid = request.json['topicid']
		u = getuserinformation(token)
		if u is not None:
			topic = gettopicbyid(topicid)
			post1 = post(title = title,body = body,topic = topic)
			u.publishpost(post1)
			id = post1.id
			topic.postnumber = topic.posts.count()
			state = 'successful'
			reason = ''
		else:
			id = ''
			state = 'fail'
			reason = 'no user'
	except Exception, e:	
		print e
		id = ''
		state = 'fail'
		reason = 'exception'

	response = jsonify({'state':state,
						'reason':reason,
						'id':id})
	return response

@community_route.route("/commenttopost",methods=['POST'])
def commenttopost():
	try:
		token = request.json['token']
		body = request.json.get('body','')
		postid = request.json['postid']
		u = getuserinformation(token)
		if u is not None:
			post1 = getpostbyid(postid)
			comment1 = comment(body = body)
			u.commenttopost(comment1,post1)
			id = comment1.id
			post1.commentnumber = post1.comments.count()
			post1.add()
			state = 'successful'
			reason = ''
		else:
			id = ''
			state = 'fail'
			reason = 'no user'
	except Exception, e:	
		print e
		id = ''
		state = 'fail'
		reason = 'exception'

	response = jsonify({'state':state,
						'reason':reason,
						'id':id})
	return response

@community_route.route("/commenttocomment",methods=['POST'])
def commenttocomment():
	try:
		token = request.json['token']
		body = request.json.get('body','')
		destcommentid = request.json['destcommentid']
		u = getuserinformation(token)
		print destcommentid
		destcomment = getcommentbyid(destcommentid)
		print u
		print destcomment
		if u!=None and destcomment!=None:
			sourcecomment = comment(body = body)
			u.commenttocomment(sourcecomment,destcomment)
			id = sourcecomment.id
			post1 = destcomment.post
			post1.commentnumber = post1.comments.count()
			post1.add()
			state = 'successful'
			reason = ''
		else:
			id = ''
			state = 'fail'
			reason = 'no user or no destcomment'
	except Exception, e:	
		print e
		id = ''
		state = 'fail'
		reason = 'exception'

	response = jsonify({'state':state,
						'reason':reason,
						'id':id})
	return response

@community_route.route("/likepost",methods=['POST'])
def likepost():
	try:
		token = request.json['token']
		postid = request.json['postid']
		u = getuserinformation(token)
		if u is not None:
			post1 = getpostbyid(postid)
			temp = u.likepost(post1)
			if temp == 0:
				post1.likenumber = post1.likeusers.count()
				post1.add()
				state = 'successful'
				reason = ''
				likenumber = post1.likenumber
			elif temp == 1:
				state = 'fail'
				reason = 'already like'
				likenumber = ''
			else:
				state = 'fail'
				reason = 'exception'
				likenumber = ''
		else:
			state = 'fail'
			reason = 'no user'
			likenumber = ''
	except Exception, e:	
		print e
		likenumber = ''
		state = 'fail'
		reason = 'exception'

	response = jsonify({'state':state,
						'reason':reason,
						'likenumber':likenumber})
	return response

@community_route.route("/likecomment",methods=['POST'])
def likecomment():
	try:
		token = request.json['token']
		commentid = request.json['commentid']
		u = getuserinformation(token)
		if u is not None:
			comment1 = getcommentbyid(commentid)
			temp = u.likecomment(comment1)
			if temp == 0:
				comment1.likenumber = comment1.likeusers.count()
				comment1.add()
				state = 'successful'
				reason = ''
				likenumber = comment1.likenumber
			elif temp == 1:
				state = 'fail'
				reason = 'already like'
				likenumber = ''
			else:
				state = 'fail'
				reason = 'exception'
				likenumber = ''
		else:
			state = 'fail'
			reason = 'no user'
			likenumber = ''
	except Exception, e:	
		print e
		likenumber = ''
		state = 'fail'
		reason = 'exception'

	response = jsonify({'state':state,
						'reason':reason,
						'likenumber':likenumber})
	return response

#社区页面1
#1.置顶图片连接
@community_route.route("/topofficial",methods=['POST'])
def topofficial():
	try:
		token = request.json['token']
		u = getuserinformation(token)
		if u is not None:	
			state = 'successful'
			reason = ''
			toplist = gettopofficial()
			result = []
			for i in range(len(toplist)):
				output = {"postid":toplist[i].postid,"imageurl":toplist[i].imageurl}
				result.append(output)
		else:
			state = 'fail'
			reason = 'no user'
			result = ''

	except Exception, e:
		print e
		result = ''
		state = 'fail'
		reason = 'exception'

	response = jsonify({'result':result,
						'state':state,
						'reason':reason})
	return response
#2.社区主题划分
@community_route.route("/gettopiclist",methods=['POST'])
def gettopiclist():
	try:
		token = request.json['token']
		u = getuserinformation(token)
		if u is not None:	
			state = 'successful'
			reason = ''
			topiclist = gettopiclistdb()
			result = []
			for i in range(len(topiclist)):
				output = {"id":topiclist[i].id,"theme":topiclist[i].theme,"imageurl":topiclist[i].imageurl,"note":topiclist[i].note,"number":topiclist[i].number}
				result.append(output)
		else:
			state = 'fail'
			reason = 'no user'
			result = ''

	except Exception, e:
		print e
		result = ''
		state = 'fail'
		reason = 'exception'

	response = jsonify({'result':result,
						'state':state,
						'reason':reason})
	return response
#社区页面2
@community_route.route("/gettopicslogan",methods=['POST'])
def gettopicslogan():
	try:
		token = request.json['token']
		topicid = request.json['topicid']
		topic = gettopicbyid(topicid)
		u = getuserinformation(token)
		if u is not None:	
			state = 'successful'
			reason = ''
			result = {"id":topic.id,"slogan":topic.slogan,"imageurl":topic.imageurl}
		else:
			state = 'fail'
			reason = 'no user'
			result = ''

	except Exception, e:
		print e
		result = ''
		state = 'fail'
		reason = 'exception'

	response = jsonify({'result':result,
						'state':state,
						'reason':reason})
	return response
#获取post列表
@community_route.route("/getpostlist",methods=['POST'])
def getpostlist():
	try:
		token = request.json['token']
		page = request.json['page']
		topicid = request.json['topicid']
		x=string.atoi(page)
		u = getuserinformation(token)
		if u is not None:	
			state = 'successful'
			reason = ''
			pageitems = getpostlistbypage(x,topicid)
			postlist = pageitems.items
			result = []
			for i in range(len(postlist)):
				name = postlist[i].author.name if postlist[i].author.name!=None else ''
				school = postlist[i].author.school if postlist[i].author.school != None else ''
				title = postlist[i].title if postlist[i].title !=None else ''
				body = postlist[i].body if postlist[i].body !=None else ''
				gender =  postlist[i].author.gender if postlist[i].author.gender != None else ''
				postimage = postlist[i].images.all()
				if len(body) > 30:
					body = body[0:29]
				else:
					body = body
				image = []
				thumbnail = []
				for j in range(len(postimage)):
					number = postimage[j].imageid
					url = "http://218.244.147.240:80/community/postattachs/" + str(topicid) + "-" + str(postlist[i].id) + "-" + str(number)
					urlthum = "http://218.244.147.240:80/community/postattachs/" + str(topicid) + "-" + str(postlist[i].id) + "-" + str(number) + "_thumbnail.jpg"
					image.append(url)
					thumbnail.append(urlthum)
				output = {"postid":postlist[i].id,"userid":postlist[i].author.id,"name":name,"school":school,"gender":gender,"timestamp":postlist[i].timestamp,"title":title,"body":body,"likenumber":postlist[i].likenumber,"commentnumber":postlist[i].commentnumber,"imageurl":image,"thumbnail":thumbnail}
				result.append(output)
		else:
			state = 'fail'
			reason = 'no user'
			result = ''
	except Exception, e:
		#raise 
		print e
		result = ''
		state = 'fail'
		reason = 'exception'
	response = jsonify({'result':result,
						'state':state,
						'reason':reason})
	return response
#页面3
#返回帖子详细内容
@community_route.route("/getpostdetail",methods=['POST'])
def getpostdetail():
	try:
		token = request.json['token']
		postid = request.json['postid']
		page = "1"
		x=string.atoi(page)
		u = getuserinformation(token)
		if u is not None:	
			state = 'successful'
			reason = ''
			post = getpostbyid(postid)
			name = post.author.name if post.author.name!=None else ''
			school = post.author.school if post.author.school != None else ''
			title = post.title if post.title !=None else ''
			body = post.body if post.body !=None else ''
			gender =  post.author.gender if post.author.gender != None else ''
			topicid = post.topic.id
			postimage = post.images.all()
			image = []
			thumbnail = []
			for j in range(len(postimage)):
				number = postimage[j].imageid
				url = "http://218.244.147.240:80/community/postattachs/"+ str(topicid) + "-" + str(post.id) + "-" + str(number)
				urlthum = "http://218.244.147.240:80/community/postattachs/" + str(topicid) + "-" + str(post.id) + "-" + str(number) + "_thumbnail.jpg"
				image.append(url)
				thumbnail.append(urlthum)
			likeuserpage = post.likeusers.order_by(models.likepost.timestamp.desc()).paginate(x, per_page=10, error_out=False)
			likeitems = likeuserpage.items
			L = [str(temp.userid) for temp in likeitems] 
			#判断自己是否点赞了这篇
			likeuserstemp = post.likeusers.all()
			L = [(temp2.userid) for temp2 in likeuserstemp]
			if u.id in L:
				flag = '1'
			else:
				flag = '0'
			result = {"postid":post.id,"userid":post.author.id,"name":name,"school":school,"gender":gender,"timestamp":post.timestamp,"title":title,"body":body,"likenumber":post.likenumber,"commentnumber":post.commentnumber,"imageurl":image,"thumbnail":thumbnail,"likeusers":L,"flag":flag}
		else:
			state = 'fail'
			reason = 'no user'
			result = ''
	except Exception, e:
		#raise 
		print e
		result = ''
		state = 'fail'
		reason = 'exception'
	response = jsonify({'result':result,
						'state':state,                                                                                                                                                                                  
						'reason':reason})
	return response

#返回post的评论
@community_route.route("/getpostcomment",methods=['POST'])
def getpostcomment():
	try:
		token = request.json['token']
		postid = request.json['postid']
		page = request.json['page']
		x=string.atoi(page)
		u = getuserinformation(token)
		if u is not None:	
			state = 'successful'
			reason = ''
			commentlistpage = getpostcommentbypage(x,postid)
			commentlistitems = commentlistpage.items
			result = []
			for items in commentlistitems:
				#获取这条评论的图片附件链接
				commentimage = items.images.all()
				image = []
				thumbnail = []
				for commentimagetemp in commentimage:
					number = commentimagetemp.imageid
					url = "http://218.244.147.240:80/community/commentattachs/"+ str(items.post.topicid) + "-" + str(items.id) + "-" + str(number)
					urlthum = "http://218.244.147.240:80/community/commentattachs/" + str(items.post.topicid) + "-" + str(items.id) + "-" + str(number) + "_thumbnail.jpg"
					image.append(url)
					thumbnail.append(urlthum)
				#获取回复这条评论的所有评论
				commentinlist = []
				commentinlist.append(items.id)
				tempcontent = commentinlist
				while True:
					temp = getcommenttocommentbyid(tempcontent)
					if len(temp) == 0:
						break
					L = [idtemp.id for idtemp in temp]
					commentinlist.extend(L)
					tempcontent = L
				ctcresult = []
				for i in range(len(commentinlist)):
					if i!=0:
						ctcommenttemp = getcommentbyid(commentinlist[i])
						commentsource = ctcommenttemp
						commentdest = getcommentbyid(ctcommenttemp.commentid)
						ctcoutput = {"id":commentsource.id,"authorid":commentsource.author.id,"name":commentsource.author.name,"body":commentsource.body,"destname":commentdest.author.name,"destuserid":commentdest.author.id,"destcommentid":commentdest.id}
						ctcresult.append(ctcoutput)

				ctcresult.reverse()#逆序下
				#附加这条评论的一些基础信息
				name = items.author.name if items.author.name != None else ''
				school = items.author.school if items.author.school != None else ''
				gender = items.author.gender if items.author.gender != None else ''
				body = items.body if items.body != None else ''
				likeuserstemp = items.likeusers.all()
				L = [(temp2.userid) for temp2 in likeuserstemp]
				if u.id in L:
					flag = '1'
				else:
					flag = '0'
				output = {"id":items.id,"image":image,"thumbnail":thumbnail,"userid":items.author.id,"name":name,"school":school,"gender":gender,"timestamp":items.timestamp,"body":body,"likenumber":items.likenumber,"commentnumber":len(ctcresult),"reply":ctcresult,"flag":flag}
				result.append(output)
		else:
			state = 'fail'
			reason = 'no user'
			result = ''
	except Exception, e:
		#raise 
		print e
		result = ''
		state = 'fail'
		reason = 'exception'
	response = jsonify({'result':result,
						'state':state,                                                                                                                                                                                  
						'reason':reason})
	return response

#根据post得到所有点赞用户
@community_route.route("/getpostlikeusers",methods=['POST'])
def getpostlikeusers():
	try:
		token = request.json['token']
		postid = request.json['postid']
		page = request.json['page']
		x=string.atoi(page)
		u = getuserinformation(token)
		if u is not None:	
			state = 'successful'
			reason = ''
			post = getpostbyid(postid)
			likeuserpage = post.likeusers.order_by(models.likepost.timestamp.desc()).paginate(x, per_page=10, error_out=False)
			likeitems = likeuserpage.items
			result = []
			for temp in likeitems:
				userid = temp.userid
				usertemp = getuserbyid(userid)
				name = usertemp.name if usertemp.name != None else ''
				school = usertemp.school if usertemp.school != None else ''
				gender = usertemp.gender if usertemp.gender != None else ''
				output = {"id":usertemp.id,"name":name,"school":school,"gender":gender}
				result.append(output)
		else:
			state = 'fail'
			reason = 'no user'
			result = ''
	except Exception, e:
		print e
		result = ''
		state = 'fail'
		reason = 'exception'
	response = jsonify({'result':result,
						'state':state,                                                                                                                                                                                  
						'reason':reason})
	return response
#根据commentid得到这个comment的所有评论

@community_route.route("/getcommentbycommentid",methods=['POST'])
def getcommentbycommentid():
	try:
		token = request.json['token']
		commentid = request.json['commentid']
		u = getuserinformation(token)
		if u is not None:	
			state = 'successful'
			reason = ''
			items = getcommentbyid(commentid)
			#获取这条评论的图片附件链接
			commentimage = items.images.all()
			image = []
			thumbnail = []
			for commentimagetemp in commentimage:
				number = commentimagetemp.imageid
				url = "http://218.244.147.240:80/community/commentattachs/"+ str(items.post.topicid) + "-" + str(items.id) + "-" + str(number)
				urlthum = "http://218.244.147.240:80/community/commentattachs/" + str(items.post.topicid) + "-" + str(items.id) + "-" + str(number) + "_thumbnail.jpg"
				image.append(url)
				thumbnail.append(urlthum)		
			commentinlist = []
			commentinlist.append(items.id)
			tempcontent = commentinlist
			while True:
				temp = getcommenttocommentbyid(tempcontent)
				if len(temp) == 0:
					break
				L = [idtemp.id for idtemp in temp]
				commentinlist.extend(L)
				tempcontent = L
			ctcresult = []
			for i in range(len(commentinlist)):
				if i!=0:
					ctcommenttemp = getcommentbyid(commentinlist[i])
					commentsource = ctcommenttemp
					commentdest = getcommentbyid(ctcommenttemp.commentid)
					ctcoutput = {"id":commentsource.id,"authorid":commentsource.author.id,"name":commentsource.author.name,"body":commentsource.body,"destname":commentdest.author.name,"destuserid":commentdest.author.id,"destcommentid":commentdest.id}
					ctcresult.append(ctcoutput)
			#逆序下
			ctcresult.reverse()
			#基本信息
			name = items.author.name if items.author.name != None else ''
			school = items.author.school if items.author.school != None else ''
			gender = items.author.gender if items.author.gender != None else ''
			body = items.body if items.body != None else ''
			likeuserstemp = items.likeusers.all()
			L = [(temp2.userid) for temp2 in likeuserstemp]
			if u.id in L:
				flag = '1'
			else:
				flag = '0'
			result = {"id":items.id,"userid":items.author.id,"image":image,"thumbnail":thumbnail,"name":name,"school":school,"gender":gender,"timestamp":items.timestamp,"body":body,"likenumber":items.likenumber,"commentnumber":len(ctcresult),"reply":ctcresult,"flag":flag}
		else:
			state = 'fail'
			reason = 'no user'
			result = ''
	except Exception, e:
		#raise 
		print e
		result = ''
		state = 'fail'
		reason = 'exception'
	response = jsonify({'result':result,
						'state':state,                                                                                                                                                                                  
						'reason':reason})
	return response
