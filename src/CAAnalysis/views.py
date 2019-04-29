from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import csv,os,json

filedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
confpath = os.path.join(filedir, "config/config.json")
CAList = ['US','Canada',"FR","DE","IT","JP","GB","TW"]
# Create your views here.
def CAHome_page(request, *args, **kwargs):
	f = open(confpath,"r")
	conf = json.loads(f.read())
	context ={
		"time" : conf['DateList'],
	}
	return render(request,"CAAnalysis/ca.html",context)

def CA_Request(request, *args, **kwargs):
	data = request.POST
	dataDate = data['season']
	country = int(data['filetype'])

	f = open(confpath,"r")
	conf = json.loads(f.read())
	context = {
		"data" : [],
		"message": "no",
		"filetype": "0",
		"Country": "no"
	}
	if str(dataDate) not in conf['DateList']:
		context['message'] = 'season invalid'
		return render(request,"CAAnalysis/ca.html",context)
	if country < 0 or country > 8:
		context['message'] = 'countrycode invalid'
		return render(request,"CAAnalysis/ca.html",context)
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
						tmp =line[23].split("C=")[-1]
						if "DST" in tmp or 'Entrust' in tmp:
							tmp = 'US'
						if "GlobalSign" in tmp:
							tmp = 'Belgium'
						if tmp == CAList[i]:
							cntList[i] += 1
		context['data'] = cntList
		return JsonResponse(context,safe=False)

	else:
		context['filetype'] = '1'
		context["Country"] = conf["CountryList"][country-1]
		tmppath = os.path.join(filedir, conf['Savedir']+str(dataDate)+"/thoroughscan")
		filepath = os.path.join(tmppath, dataDate+"_"+conf['CountryList'][country-1]+"scan_result_stat_final.csv")
		with open(filepath, encoding="utf-8") as f:
			c = csv.reader(f)
			cnt = 0
			for line in c:
				if "Ready" in line[2]:
					tmp =line[23].split("C=")[-1]
					if "DST" in tmp or 'Entrust' in tmp:
						tmp = 'US'
					if "GlobalSign" in tmp:
						tmp = 'Belgium'
					if tmp == CAList[country-1]:
						cnt += 1
			context['data'] = cnt
		print("context = ",context)
		return JsonResponse(context,safe=False)
				
