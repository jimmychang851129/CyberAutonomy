from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import csv,os,json

filedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
confpath = os.path.join(filedir, "config/config.json")

# Create your views here.
def TLSHome_page(request, *args, **kwargs):
	f = open(confpath,"r")
	conf = json.loads(f.read())
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
			f = open(filepath, encoding="utf-8")
			c = csv.reader(f)
			for line in c:
				if "Ready" in line[2]:
					cntList[int(line[-1])] += 1
			f.close()
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
		f = open(filepath, encoding="utf-8")
		c = csv.reader(f)
		for line in c:
			if "Ready" in line[2]:
				for j in range(4,15):
					if "False" not in line[j]:
						cntList[j-4] += 1
				if 'present' not in line[17]:
					cntList[11] += 1
		f.close()
		print("cntList = ",cntList)
		context['data'] = cntList
		print("context = ",context)
		return JsonResponse(context,safe=False)

