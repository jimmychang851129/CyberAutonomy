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

def HTTPS_Request(requst, *args, **kwargs):
	data = request.POST
	dataDate = data['season']
	country = int(data['filetype'])

	f = open(confpath,"r")
	conf = json.loads(f.read())
	context = {
		"data" : [],
		"messge": "no",
		"filetype": "0"
	}
	if str(dateDate) not in conf['DateList']:
		context['message'] = 'season invalid'
		return render(request,"HTTPSAnalysis/https.html",context)
	if country < 0 or country > 8:
		context['message'] = 'countrycode invalid'
		return render(request,"HTTPSAnalysis/https.html",context)

	context['message'] = 'OK'
	if country == 0:	# not yet implement
		context['filetype'] = '1'
		return render(request,"HTTPSAnalysis/https.html",context)
	else:
		context['filetype'] = '0'
		filepath = conf['Savedir']+str(dataDate)+"/"
		print("filepath = ",filepath)

