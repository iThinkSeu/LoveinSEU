__author__ = 'liewli'

from flask import Blueprint, render_template, abort
from jinja2 import  TemplateNotFound
from models import *

share = Blueprint('share', __name__, template_folder="templates", static_folder="static", url_prefix="/post_share")

@share.route('/<int:postid>', methods=['GET'])
def show(postid):
    try:
    	post = getpostbyid(postid)
    	userid = post.author.id
    	avatar = "http://218.244.147.240:80/avatar/" + str(userid)
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

        return render_template('post.html', title=title, body=body, images=image, avatar = avatar, name=name, school = school)
    except TemplateNotFound:
        abort(404)
    except Exception,e:
    	print e
    	abort(404)