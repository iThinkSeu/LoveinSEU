#-*- coding: UTF-8 -*- 
import re

def getconstelleation(birthday):
	"""get constelleation 
		birthday format: yyyy-mm-dd
	"""
	match = re.match(r'\d{4}-(\d{1,2})-(\d{1,2})', birthday)
	if match:
		month = int(match.group(1))
		day = int(match.group(2))
	else:
		return ''

	time = [{'sm':3, 'sd':21, 'em':4, 'ed':19},
			{'sm':4, 'sd':20, 'em':5, 'ed':20},
			{'sm':5, 'sd':21, 'em':6, 'ed':20},
			{'sm':6, 'sd':21, 'em':7, 'ed':21},
			{'sm':7, 'sd':22, 'em':8, 'ed':22},
			{'sm':8, 'sd':23, 'em':9, 'ed':22},
			{'sm':9, 'sd':23, 'em':10, 'ed':22},
			{'sm':10, 'sd':23, 'em':11, 'ed':21},
			{'sm':11, 'sd':22, 'em':12, 'ed':21},
			{'sm':12, 'sd':22, 'em':1, 'ed':19},
			{'sm':1, 'sd':20, 'em':2, 'ed':18},
			{'sm':2, 'sd':19, 'em':3, 'ed':20}
			]
	name = [
			u'白羊座',
			u'金牛座',
			u'双子座',
			u'巨蟹座',
			u'狮子座',
			u'处女座',
			u'天秤座',
			u'天蝎座',
			u'射手座',
			u'摩羯座',
			u'水瓶座',
			u'双鱼座',
			]

	for idx, t in enumerate(time):
		if (t['sm'] == month and t['sd'] <= day ) or (month == t['em'] and day <= t['ed']):
			return name[idx] 
	return ''