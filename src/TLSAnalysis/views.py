from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import csv,os,json
from util.util import ReadFile
filedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
confpath = os.path.join(filedir, "config/config.json")

# Create your views here.
def TLSHome_page(request, *args, **kwargs):
	f = open(confpath,"r")
	conf = json.loads(f.read())
	f.close()
	context ={
		"time" : conf['DateList'],
	}
	return render(request,"TLSAnalysis/tls.html",context)

def TLS_Request(request, *args, **kwargs):
	data = request.POST
	dataDate = data['season']
	country = int(data['filetype'])

	f = open(confpath,"r")
	conf = json.loads(f.read())
	f.close()
	context = {
		"data" : [],
		"message": "no",
		"filetype": "0",
		"Country": "no"
	}
	if str(dataDate) not in conf['DateList']:
		context['message'] = 'season invalid'
		return render(request,"TLSAnalysis/tls.html",context)
	if country < 0 or country > 8:
		context['message'] = 'countrycode invalid'
		return render(request,"TLSAnalysis/tls.html",context)

	context['message'] = "OK"
	if country == 0:
		context['filetype'] = '0'
		TotalData = []
		tmppath = os.path.join(filedir, conf['Savedir']+str(dataDate)+"/thoroughscan")
		for i in range(len(conf['CountryList'])):
			cntList = [0]*12
			filepath = os.path.join(tmppath, dataDate+"_"+conf['CountryList'][i]+"scan_result_stat_final.csv")
			with open(filepath, encoding="utf-8") as f:
				c = csv.reader(f)
				for line in c:
					if "Ready" in line[2]:
						cntList[int(line[-1])] += 1
			for k in range(1,len(cntList)):
				cntList[k] += cntList[k-1]
			TotalData.append(cntList)
		context['data'] = TotalData
		print("context = ",context)
		return JsonResponse(context,safe=False)
	else:
		context['filetype'] = '1'
		context["Country"] = conf["CountryList"][country-1]
		cntList = [0]*12
		tmppath = os.path.join(filedir, conf['Savedir']+str(dataDate)+"/thoroughscan")
		filepath = os.path.join(tmppath, dataDate+"_"+conf['CountryList'][country-1]+"scan_result_stat_final.csv")
		with open(filepath, encoding="utf-8") as f:
			c = csv.reader(f)
			for line in c:
				if "Ready" in line[2]:
					for j in range(4,15):
						if "False" not in line[j]:
							cntList[j-4] += 1
					if 'present' not in line[17]:
						cntList[11] += 1
		context['data'] = cntList
		print("context = ",context)
		return JsonResponse(context,safe=False)


def OverallTLSDetail(request, *args, **kwargs):
	data = request.POST
	season = data['season']
	country = int(data['filetype'])

	f = open(confpath,"r")
	conf = json.loads(f.read())
	f.close()
	context = {
		"data" : [],
		"message": "no",
		"date": "0",
		"Country": "no",
	}
	if str(season) not in conf['DateList']:
		context['message'] = 'season invalid'
		return render(request,"TLSAnalysis/tlsDetail.html",context)
	if country < 1 or country > 8:
		context['message'] = 'countrycode invalid'
		return render(request,"TLSAnalysis/tlsDetail.html",context)

	context['message'] = "OK"
	context['date'] = season
	context['Country'] = conf['CountryList'][country-1]
	tmppath = os.path.join(filedir, conf['Savedir']+str(season)+"/thoroughscan")
	filepath = os.path.join(tmppath, season+"_"+conf['CountryList'][country-1]+"scan_result_stat_final.csv")
	Total = []
	with open(filepath, encoding="utf-8") as f:
		c = csv.reader(f)
		for line in c:
			if "Ready" in line[2]:
				Total.append([line[0],line[-1]]+line[4:15])
			elif line[0] != "host_name":
				Total.append([line[0],0]+[0]*11)
	context['data'] = Total
	print("context = ",context)
	# return JsonResponse(context,safe=False)
	return render(request,"TLSAnalysis/tlsDetail.html",context)

def SpecificTLSDetail(request, *args, **kwargs):
	data = request.POST
	season = data['season']
	country = int(data['country'])
	attack = int(data['attack'])

	f = open(confpath,"r")
	conf = json.loads(f.read())
	f.close()
	context = {
		"data" : [],
		"message": "no",
		"date": "0",
		"Country": "no"
	}
	if str(season) not in conf['DateList']:
		context['message'] = 'season invalid'
		return render(request,"TLSAnalysis/tls.html",context)	# return message
	if country < 1 or country > 8:
		context['message'] = 'countrycode invalid'
		return render(request,"TLSAnalysis/tls.html",context)
	context['message'] = 'OK'
	context['Country'] = conf['CountryList'][country-1]
	context['date'] = season
	tmppath = os.path.join(filedir, conf['Savedir']+str(season)+"/thoroughscan")
	filepath = os.path.join(tmppath, season+"_"+conf['CountryList'][country-1]+"scan_result_stat_final.csv")
	UrlCollection = []
	with open(filepath, encoding="utf-8") as f:
		c = csv.reader(f)
		for line in c:
			if "True" in line[4+attack]:
				UrlCollection.append(line[0])
	context["data"] = UrlCollection
	return JsonResponse(context,safe=False)

