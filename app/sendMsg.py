# -*- coding: utf-8 -*-
import top.api

appkey = "23319113"
secret = "19400b4f2c9da8cb8659d2b82ea8c4ba"


def send_sms_code_by_type(phone, code, t):
	if str(t) == '1':
		return send_register_code(phone, code)
	elif str(t) == '2':
		return send_reset_password_code(phone, code)
	else: 
		return 1

def send_register_code(phone,code):
	req=top.api.AlibabaAliqinFcSmsNumSendRequest()
	req.set_app_info(top.appinfo(appkey,secret))

	req.sms_type="normal"
	req.sms_free_sign_name="WEME唯觅"
	req.sms_param={"code":str(code),"product":"WEME"}
	req.rec_num=str(phone)
	req.sms_template_code="SMS_5375426"
	try:
		resp= req.getResponse()
		print(resp)
		return 0
	except Exception,e:
		print(e)
		return 1

def send_reset_password_code(phone, code):
	req=top.api.AlibabaAliqinFcSmsNumSendRequest()
	req.set_app_info(top.appinfo(appkey,secret))

	req.sms_type="normal"
	req.sms_free_sign_name="WEME唯觅"
	req.sms_param={"code":str(code),"product":"WEME"}
	req.rec_num=str(phone)
	req.sms_template_code="SMS_5375424"
	try:
		resp= req.getResponse()
		print(resp)
		return 0
	except Exception,e:
		print(e)
		return 1
def zhengqingnian():
	print "hi SEU!^^"
	pass