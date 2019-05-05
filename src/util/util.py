import json
def ReadFile(data,confpath):
	season = data['season']
	country = int(data['filetype'])
	f = open(confpath,"r")
	conf = json.loads(f.read())
	f.close()
	if str(season) not in conf['DateList']:	# 'season invalid'
		return -1
	if country < 0 or country > 8:	# 'countrycode invalid'
		return -2
	return country # 'OK'
