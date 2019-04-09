from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
import sys
import csv
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from pprint import pprint # parse json
import json
import pygeoip
from urllib.parse import urlparse
import time,os


class CPCrawler:
	def __init__(self):
		f = open("config.json",'r')
		conf = json.loads(f.read())
		f.close()
		caps = DesiredCapabilities.CHROME
		caps['loggingPrefs'] = {'performance': 'ALL'}
		chrome_options = Options()  
		chrome_options.add_argument("--headless")  
		driver = webdriver.Chrome("/Users/jimmy/Desktop/CA/crawl/chromedriver",desired_capabilities=caps,chrome_options=chrome_options)
		driver.set_page_load_timeout(conf['WebpageTimeout'])
		self.driver = driver
		self.conf = conf
	def terminate(self):
		self.conf['nowDate'] = nowTime
		with open('config.json', 'w') as outfile:
			json.dump(self.conf, outfile)
		self.driver.quit()


# Files = ["Italy","Japan","Uk","US","Taiwan"]
# TimeoutFile = ["Canada_timeoutsite","France_timeoutsite","Germany_timeoutsite","Italy_timeoutsite","UK_timeoutsite","US_timeoutsite","Taiwan_timeoutsite"]

def parseurl(longurl):
	uri = urlparse(longurl)
	result = '{uri.scheme}://{uri.netloc}/'.format(uri=uri)
	return result

def IPLocationLookup(ip,gi):
	return gi.country_name_by_addr(ip)

#################
# write to file #
#################
def writeFile(file,results,nowDate):
	fw = open(conf['Savedir']+nowDate+"/"+file+'.csv',"a")
	csvCursor = csv.writer(fw)
	for result in results:
		csvCursor.writerow(result)


##################
# 爬下來資訊看url #
##################
def getSitesSource(file,driver,site,conf,nowDate):
	gi = pygeoip.GeoIP('GeoIP.dat')
	site_baseurl = parseurl(site)
	print("url = ",site_baseurl)
	try:
		resp = driver.get(site)
		logs = []
		for log in driver.get_log('performance'):
			if json.loads(log['message'])['message']['method'] == 'Network.responseReceived':
				logs.append(json.loads(log['message'])['message']['params'])
		Js = []
		for log in logs:
			try:
				contenttype = log['response']['headers']['Content-Type']
				picurl = log['response']['url']
				picurl_baseurl = parseurl(picurl)
				if 'javascript' in contenttype or 'json' in contenttype or 'image/' in contenttype:
					if picurl_baseurl != site_baseurl:
						Js.append([site,log['response']['headers']['Content-Type'],log['response']['url'],IPLocationLookup(log['response']['remoteIPAddress'],gi)])
			except KeyError:
				try:
					contenttype = log['response']['headers']['content-type']
					picurl = log['response']['url']
					picurl_baseurl = parseurl(picurl)
					if 'javascript' in contenttype or 'json' in contenttype or 'image/' in contenttype:
						if picurl_baseurl != site_baseurl:
							Js.append([site,log['response']['headers']['Content-Type'],log['response']['url'],IPLocationLookup(log['response']['remoteIPAddress'],gi)])
				except KeyError:
					continue
		writeFile(file,Js,nowDate)
	except TimeoutException:
		print("Timeout Exception : ",site)
		with open(conf['Savedir']+nowDate+"/"+file+"_"+"timeoutsite.txt","a") as fw:
			fw.write(site+"\n")
		return 1
	return 1

#############
# read file #
#############
def readFile(file,conf):
	l = []
	with open(conf['Loaddir']+file+'.txt') as f:
		for row in f:
			l.append(row.strip('\n'))
	return l

def initDriver(conf) :
	caps = DesiredCapabilities.CHROME
	caps['loggingPrefs'] = {'performance': 'ALL'}
	chrome_options = Options()  
	chrome_options.add_argument("--headless")  
	driver = webdriver.Chrome(conf["driverPath"],desired_capabilities=caps,chrome_options=chrome_options)
	driver.set_page_load_timeout(conf['WebpageTimeout'])
	return driver

def readConf():
	f = open("config.json",'r')
	conf = json.loads(f.read())
	print("conf = ",conf)
	return conf

if __name__ == '__main__':
	conf = readConf()
	Files = conf['Files']
	Files = ["test"]
	driver = initDriver(conf)
	a = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	nowTime = a[:4]+a[5:7]
	if os.path.isdir(conf['Savedir']+nowTime+"/") == True:
		print("Exception : "+conf['Savedir']+nowTime+"/"+" already exist")
	else:
		os.mkdir(conf['Savedir']+nowTime+"/")
	for file in Files:
		data = readFile(file,conf)
		for site in data:
			getSitesSource(file,driver,site,conf,nowTime)	# jimmy

	conf['nowDate'] = nowTime
	with open('config.json', 'w') as outfile:
		json.dump(self.conf, outfile,indent=2)
	driver.quit()