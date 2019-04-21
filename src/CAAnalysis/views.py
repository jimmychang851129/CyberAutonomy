from django.shortcuts import render
from django.http import HttpResponse
import csv,os,json

confpath = "./config/config.json" # same directory as manage.py

# Create your views here.
def CAHome_page(request, *args, **kwargs):
	f = open(confpath,"r")
	conf = json.loads(f.read())
	context ={
		"time" : conf['DateList'],
	}
	return render(request,"CAAnalysis/ca.html",context)

