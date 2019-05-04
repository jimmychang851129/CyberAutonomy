from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import csv,os,json
# from util.util import hello

filedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
confpath = os.path.join(filedir, "config/config.json")

# Create your views here.
def HTTPSHome_page(request, *args, **kwargs):
	f = open(confpath,"r")
	conf = json.loads(f.read())
	f.close()
	context ={
		"time" : conf['DateList'],
	}
	return render(request,"HTTPSAnalysis/https.html",context) 

def HTTPS_Request(request, *args, **kwargs):
	data = request.POST
	dataDate = data['season']
	country = int(data['filetype'])

	f = open(confpath,"r")
	conf = json.loads(f.read())
	f.close()
	context = {
		"data" : 0,
		"message": "no",
		"filetype": "0",
		"Country" : "no"
	}
	if str(dataDate) not in conf['DateList']:
		context['message'] = 'season invalid : ' + str(dataDate)
		return JsonResponse(context,safe=False)
	if country < 0 or country > 8:
		context['message'] = 'countrycode invalid : ' + str(country)
		return JsonResponse(context,safe=False)

	context['message'] = 'OK'
	if country == 0:
		context['filetype'] = '0'
		cntList = [0,0,0,0,0,0,0,0]
		tmppath = os.path.join(filedir, conf['Savedir']+str(dataDate)+"/thoroughscan")
		for i in range(len(conf['CountryList'])):
			filepath = os.path.join(tmppath, dataDate+"_"+conf['CountryList'][i]+"scan_result_stat_final.csv")
			with open(filepath) as f:
				c = csv.reader(f)
				for line in c:
					if "Ready" in line[2]:
						cntList[i] += 1
		context['data'] = cntList
		print("context = ",context)
		return JsonResponse(context,safe=False)
	else:
		context["Country"] = conf["CountryList"][country-1]
		context['filetype'] = '1'
		filepath = os.path.join(filedir, conf['Savedir']+str(dataDate)+"/thoroughscan")
		filepath = os.path.join(filepath, dataDate+"_"+conf['CountryList'][country-1]+"scan_result_stat_final.csv")
		with open(filepath) as f:
			cnt = 0
			c = csv.reader(f)
			for line in c:
				if "Ready" in line[2]:
					cnt += 1
			context['data'] = cnt
		print("context = ",context)
		return JsonResponse(context,safe=False)


##################
# further detail #
##################
# def HTTPSHSTSDetail(request, *args, **kwargs):
# 	data = request.POST
# 	country = data['country']
# 	season = data['season']

# 	f = open(confpath,"r")
# 	conf = json.loads(f.read())
# 	context = {
# 		"data" : 0,
# 		"message": "no",
# 		"date": "0",
# 		"Country" : "no"
# 	}
# 	if str(dataDate) not in conf['DateList']:
# 		context['message'] = 'season invalid : ' + str(dataDate)
# 		return JsonResponse(context,safe=False)
# 	if country < 0 or country > 8:
# 		context['message'] = 'countrycode invalid : ' + str(country)
# 		return JsonResponse(context,safe=False)
# 	########################
# 	# load data and return #
# 	########################
# 	filepath = os.path.join(filedir, conf['Savedir']+str(dataDate)+"/thoroughscan")
# 	filepath = os.path.join(tmppath, dataDate+"_"+conf['CountryList'][country-1]+"scan_result_stat_final.csv")
# 	TotalList = []
# 	with open(filepath, encoding="utf-8") as f:
# 		for line in f:
# 			line = line.split(',')
# 			if "hostname" not in line[0]:
# 				line[0],

######################
# find non https url #
######################

