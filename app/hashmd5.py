# -*- coding: utf-8 -*-
import hashlib
import re

def hashToken(username,password):
    password_md5 = hashlib.md5()
    password_md5.update(username)
    password_md5.update(password)
    return password_md5.hexdigest()
def generatemd5(password):
    password_md5 = hashlib.md5()
    password_md5.update(password)
    return password_md5.hexdigest()
    
def Regular_Express_Mail(email):

    p=re.compile('[^\._-][\w\.-]+@(?:[A-Za-z0-9]+\.)')
    isMatch=p.match(email)
    if isMatch:  
        print ("Success!!")
    else:  
        print ("Failure!!")


def checkName(Name):
    pattern =re.compile('^[a-zA-z][a-zA-Z0-9_]{1,19}$')
    match=pattern.match(Name)
    if match:
        return True
    else:
        return False
