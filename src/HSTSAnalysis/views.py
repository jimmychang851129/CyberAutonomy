from django.shortcuts import render
import csv,os,json

confpath = "./config/config.json" # same directory as manage.py

# Create your views here.
def HSTSHome_page(request, *args, **kwargs):
	f = open(confpath,"r")
	conf = json.loads(f.read())
	context ={
		"time" : conf['DateList'],
	}
	return render(request,"HSTSAnalysis/hsts.html",context)