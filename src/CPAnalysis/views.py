from django.shortcuts import render
from django.http import HttpResponse
import csv,os,json

confpath = "./config/config.json" # same directory as manage.py

# Create your views here.
def CPHome_page(request, *args, **kwargs):
	f = open(confpath,"r")
	conf = json.loads(f.read())
	context ={
		"time" : conf['DateList'],
	}
	return render(request,"CPAnalysis/CPHomepage.html",context)

def CPDate(request,*args,**kwargs):
	data = request.POST
	dataDate = int(data['Datequery'])
	print("request = ",data['Datequery'])
	path = os.path.join(os.path.abspath(__file__),"CPCrawling/result")
	print("path = ",os.path.abspath(__file__))
	f = open(confpath,"r")
	conf = json.loads(f.read())
	filepath = conf['Savedir']+str(dataDate)+"/"
	print("file path = ",filepath)
	if os.path.isdir(filepath) == True:
		f = open(filepath+"Canada.csv","r")	# modify
		test = f.read()
		return HttpResponse(test)
	else:
		print("File not found")
		return HttpResponse("Date error")