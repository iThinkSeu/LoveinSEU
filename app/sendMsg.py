# -*- coding: utf-8 -*-
import top.api
 
def sendMsg(phone,code):
	appkey = "23319113"
	secret = "19400b4f2c9da8cb8659d2b82ea8c4ba"
	req=top.api.AlibabaAliqinFcSmsNumSendRequest()
	req.set_app_info(top.appinfo('23319113','19400b4f2c9da8cb8659d2b82ea8c4ba'))

	req.extend="123456"
	req.sms_type="normal"
	req.sms_free_sign_name="WEME唯觅"
	req.sms_param={"code":str(code),"product":"WEME","item":"WEME唯觅"}
	req.rec_num=str(phone)
	req.sms_template_code="SMS_5375426"
	try:
		resp= req.getResponse()
		print(resp)
	except Exception,e:
		print(e)

