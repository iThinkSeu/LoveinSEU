#-*- coding: UTF-8 -*- 
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

sqlurl = "mysql://root:root@localhost:3306/flasktestdb?charset=utf8"
#sqlurl = "mysql://root:SEUqianshou2015@218.244.147.240:3306/flasktestdb?charset=utf8"
#sqlurl = "mysql://root:0596@223.3.36.246:3306/flasktestdb?charset=utf8"
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']=sqlurl
    db.init_app(app)
    return app
