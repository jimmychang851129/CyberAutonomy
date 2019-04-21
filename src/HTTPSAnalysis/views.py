from django.shortcuts import render
from django.http import HttpResponse
import csv,os,json

filedir = os.path.dirname(os.path.realpath('__file__'))
confpath = os.path.join(filedir, "src/config/config.json")
# confpath = "./config/config.json" # same directory as manage.py

# Create your views here.
def HTTPSHome_page(request, *args, **kwargs):
	f = open(confpath,"r")
	conf = json.loads(f.read())
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
	context = {
		"data" : 0,
		"message": "no",
		"filetype": "0",
		"Country" : "no"
	}
	if str(dataDate) not in conf['DateList']:
		context['message'] = 'season invalid'
		return render(request,"HTTPSAnalysis/https.html",context)
	if country < 0 or country > 8:
		context['message'] = 'countrycode invalid'
		return render(request,"HTTPSAnalysis/https.html",context)

	context['message'] = 'OK'
	if country == 0:	# not yet implement
		context['filetype'] = '1'
		cntList = [0,0,0,0,0,0,0,0]
		tmppath = os.path.join(filedir, "src/"+conf['Savedir']+str(dataDate)+"/fastscan")
		for i in range(len(conf['CountryList'])):
			filepath = os.path.join(tmppath, dataDate+"_"+conf['CountryList'][i]+"_https_support_website.txt")
			f = open(filepath)
			for line in f:
				cntList[i] += 1
			f.close()
		context['data'] = cntList
		print("context = ",context)
		return HttpResponse(context['data'])
		# return render(request,"HTTPSAnalysis/https.html",context)
	else:
		context["Country"] = conf["CountryList"][country-1]
		context['filetype'] = '0'
		filepath = os.path.join(filedir, "src/"+conf['Savedir']+str(dataDate)+"/fastscan")
		filepath = os.path.join(filepath, dataDate+"_"+conf['CountryList'][country-1]+"_https_support_website.txt")
		print("filepath = ",filepath)
		f = open(filepath)
		cnt = 0
		for line in f:
			cnt += 1
		f.close()
		context['data'] = cnt
		print("context = ",context)
	return HttpResponse(context['data'])
