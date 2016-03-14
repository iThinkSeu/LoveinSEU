#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
import models 
import string
from sqlalchemy import Date, cast
import random 
from sqlalchemy.sql import text


recommendAlgorithm_route = Blueprint('recommendAlgorithm_route', __name__)


"""
sql = text(
			"SELECT  *"
			"FROM 	("
					"SELECT @cnt:=COUNT(*) + 1,@lim:=10"
					"FROM avatarvoice"
					")vars"
			"STRAIGHT_JOIN"
					"("
					"SELECT "


"""
sql = "SELECT * FROM avatarvoice ORDER BY RAND(20090301) LIMIT 10"

result= db.engine.execute(sql)
for temp in result:
	print temp.id
	print temp.name
