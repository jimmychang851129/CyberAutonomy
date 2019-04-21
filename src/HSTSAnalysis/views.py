from django.shortcuts import render
import csv,os,json

filedir = os.path.dirname(os.path.realpath('__file__'))
confpath = os.path.join(filedir, "src/config/config.json")
# confpath = "./config/config.json" # same directory as manage.py

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
		"messge": "no"
	}
	if str(dateDate) not in conf['DateList']:
		context['message'] = 'season invalid'
		return render(request,"HSTSAnalysis/hsts.html",context)
	if country < 0 or country > 8:
		context['message'] = 'countrycode invalid'
		return render(request,"HSTSAnalysis/hsts.html",context)