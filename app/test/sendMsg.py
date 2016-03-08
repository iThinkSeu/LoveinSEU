# -*- coding: utf-8 -*-
import top.api

url = "http://gw.api.taobao.com/router/rest"
req=top.api.AlibabaAliqinFcSmsNumSendRequest(url,port)
req.set_app_info(top.appinfo(appkey,secret))
 
req.extend="123456"
req.sms_type="normal"
req.sms_free_sign_name="阿里大鱼"
req.sms_param="{\"code\":\"1234\",\"product\":\"阿里大鱼\",\"item\":\"阿里大鱼\"}"
req.rec_num="13000000000"
req.sms_template_code="SMS_585014"
try:
    resp= req.getResponse()
    print(resp)
except Exception,e:
    print(e)


