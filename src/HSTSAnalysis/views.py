from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import csv,os,json

filedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
confpath = os.path.join(filedir, "config/config.json")

# Create your views here.
def HSTSHome_page(request, *args, **kwargs):
	f = open(confpath,"r")
	conf = json.loads(f.read())
	context ={
		"time" : conf['DateList'],
	}
	return render(request,"HSTSAnalysis/hsts.html",context)

def HSTS_Request(request, *args, **kwargs):
	data = request.POST
	dataDate = data['season']
	country = int(data['filetype'])

	f = open(confpath,"r")
	conf = json.loads(f.read())
	context = {
		"data" : [],
		"message": "no",
		"filetype": "0",
		"Country" : "no"
	}
	if str(dataDate) not in conf['DateList']:
		context['message'] = 'season invalid'
		return JsonResponse(context,safe=False)
	if country < 0 or country > 8:
		context['message'] = 'countrycode invalid'
		return JsonResponse(context,safe=False)
	
	context['message'] = 'OK'
	if country == 0:		# all countries
		context['filetype'] = '0'
		cntList = [0,0,0,0,0,0,0,0]
		tmppath = os.path.join(filedir, conf['Savedir']+str(dataDate)+"/thoroughscan")
		for i in range(len(conf['CountryList'])):
			filepath = os.path.join(tmppath, dataDate+"_"+conf['CountryList'][i]+"scan_result_stat_final.csv")
			print("filepath = ",filepath)
			f = open(filepath, encoding="utf-8")
			c = csv.reader(f)
			for line in c:
				if "Ready" in line[2] and 'present' in line[17]:
					cntList[i] += 1
				
			f.close()
		context['data'] = cntList
		print("context = ",context)
		return JsonResponse(context,safe=False)
	else:				# one country
		context["Country"] = conf["CountryList"][country-1]
		context['filetype'] = '1'
		filepath = os.path.join(filedir, conf['Savedir']+str(dataDate)+"/thoroughscan")
		filepath = os.path.join(filepath, dataDate+"_"+conf['CountryList'][country-1]+"scan_result_stat_final.csv")
		print("filepath = ",filepath)
		f = open(filepath, encoding="utf-8")
		c = csv.reader(f)
		cnt = 0
		for line in c:
			if "Ready" in line[2] and'present' in line[17]:
				cnt += 1
			
		f.close()
		context['data'] = cnt
		print("context = ",context)
		return JsonResponse(context,safe=False)
