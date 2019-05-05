from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import csv,os,json
from urllib.parse import urlparse

filedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
confpath = os.path.join(filedir, "config/config.json")
CountryList = ["United States","Canada","France","Germany","Italy","Japan","United Kingdom","Taiwan"]

def parseurl(longurl):
	uri = urlparse(longurl)
	result = '{uri.scheme}://{uri.netloc}/'.format(uri=uri)
	return result

# Create your views here.
def CPHome_page(request, *args, **kwargs):
	f = open(confpath,"r")
	conf = json.loads(f.read())
	f.close()
	context ={
		"time" : conf['DateList'],
	}
	return render(request,"CPAnalysis/CPHomepage.html",context)

def CP_Request(request, *args, **kwargs):
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
		return render(request,"CPAnalysis/CPHomepage.html",context)
	if country < 0 or country > 8:
		context['message'] = 'countrycode invalid'
		return render(request,"CPAnalysis/CPHomepage.html",context)
	context['message'] = 'OK'
	######################
	# read dependentsite #
	######################
	dependent = set()
	dependentpath = os.path.join(filedir, conf['Savedir']+"dependentList.csv")
	with open(dependentpath) as f:
		for row in f:
			dependent.add(row.split('\t')[0])
	#########################################
	# Overall compare, remove dependentsite #
	#########################################
	if country == 0:
		context['filetype'] = '0'
		cntList = [0,0,0,0,0,0,0,0]
		tmppath = os.path.join(filedir, conf['Savedir']+str(dataDate)+"/CP")
		for i in range(len(conf['CountryList'])):
			filepath = os.path.join(tmppath, conf['CountryList'][i]+".csv")
			with open(filepath,encoding="utf-8") as f:
				c = csv.reader(f)
				CPList = set()
				for line in c:
					tmpsite = parseurl(''.join(line[2:-1]))
					if tmpsite not in dependent and line[0] not in CPList and line[-1].strip() != CountryList[i]:
						CPList.add(line[0])
				cntList[i] = 100 - len(CPList)
		context['data'] = cntList
		return JsonResponse(context,safe=False)

	else:
		context["Country"] = conf["CountryList"][country-1]
		context['filetype'] = '1'
		filepath = os.path.join(filedir, conf['Savedir']+str(dataDate)+"/CP")
		filepath = os.path.join(filepath, conf['CountryList'][country-1]+".csv")
		with open(filepath,encoding="utf-8") as f:
			c = csv.reader(f)
			CPList = set()
			for line in c:
				tmpsite = parseurl(''.join(line[2:-1]))	# parse resource url to domain
				if tmpsite not in dependent and line[0] not in CPList and line[-1].strip() != CountryList[country-1]:
					CPList.add(line[0])
			context['data'] = len(CPList)
		return JsonResponse(context,safe=False)

def CPDetail(request, *args, **kwargs):
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
		return render(request,"CPAnalysis/CPHomepage.html",context)
	if country < 0 or country > 8:
		context['message'] = 'countrycode invalid'
		return render(request,"CPAnalysis/CPHomepage.html",context)
	context['message'] = 'OK'
	######################
	# read dependentsite #
	######################
	dependent = set()
	dependentpath = os.path.join(filedir, conf['Savedir']+"dependentList.csv")
	with open(dependentpath) as f:
		for row in f:
			dependent.add(row.split('\t')[0])
	###############################################
	# Get external resource, remove dependentsite #
	###############################################
	filepath = os.path.join(filedir, conf['Savedir']+str(dataDate)+"/CP")
	filepath = os.path.join(filepath, conf['CountryList'][country-1]+".csv")
	CurSite = ""
	Total = []
	
	with open(filepath,'r', encoding='utf-8') as f:
		c = csv.reader(f)
		cnt_list = [0,0,0]
		for line in c:
			tmpsite = parseurl(''.join(line[2:-1]))	# parse resource url to domain
			if tmpsite.strip() not in dependent:
				if line[0].strip() != CurSite:
					if CurSite != "":
						Total.append([CurSite]+cnt_list)
					cnt_list = [0,0,0]
					CurSite = line[0].strip()
				if "image" in line[1]:
					cnt_list[0] += 1
				if "javascript" in line[1]:
					cnt_list[1] += 1
				if "json" in line[1]:
					cnt_list[2] += 1
		Total.append([CurSite]+cnt_list)
	context['data'] = Total
	return JsonResponse(context,safe=False)
