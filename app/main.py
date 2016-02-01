#-*- coding: UTF-8 -*- 
"""
from flask import Flask,jsonify,json
"""
from flask import request
from flask import render_template
from flask import redirect
from models import *
from wtforms import Form,TextField,PasswordField,validators
from hashmd5 import *
import os, stat
#from PIL import Image
#import Image
import shutil
import string;
import datetime
from sqlalchemy import or_
from checkpage import check_page
from uploadimage import upload_image
from activityroute import activity_route
from editprofileroute import editprofile_route
from getprofileroute import getprofile_route
from friendsroute import friends_route
from personalmessageroute import personalmessage_route
from communityroute import community_route
from cardroute import card_route
from report import report_route
from adminuser import adminuser_route
from schoolcertification import certification_route

from share.share import share
from dbSetting import create_app,db 
from push import push

#app = Flask(__name__)
app = create_app()

##注册蓝本路由
app.register_blueprint(check_page)  			#注册与登录
app.register_blueprint(upload_image)			#上传图片
app.register_blueprint(activity_route)			#活动相关
app.register_blueprint(editprofile_route)		#编辑用户个人信息相关
app.register_blueprint(getprofile_route)		#获取用户个人信息
app.register_blueprint(friends_route)			#获取好友关系、搜索好友、推荐好友等相关
app.register_blueprint(personalmessage_route)	#私信相关
app.register_blueprint(community_route)			#社区相关
app.register_blueprint(card_route)				#卡片相关
app.register_blueprint(report_route)			#卡片相关
app.register_blueprint(certification_route)		#校园认证

app.register_blueprint(adminuser_route)			#后台管理相关
app.register_blueprint(share)		#分享
app.register_blueprint(push)


if __name__ == '__main__':
	app.run(host=os.getenv('IP','0.0.0.0'),port=int(os.getenv('PORT',8080)))

