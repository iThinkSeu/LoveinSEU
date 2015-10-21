
import hashlib

def hashToken(username,password):
    password_md5 = hashlib.md5()
    password_md5.update(username)
    password_md5.update(password)
    return password_md5.hexdigest()
