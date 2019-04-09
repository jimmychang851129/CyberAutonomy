from urllib.parse import urlparse
import csv
site_country = {}
dependentsite = set()
dependentList = {}  # key => [possible countrylist]
output = {}

def parseurl(longurl):
	uri = urlparse(longurl)
	result = '{uri.scheme}://{uri.netloc}/'.format(uri=uri)
	return result

Files = ["Canada","France","Germany","Italy","Japan","Uk","US","Taiwan"]
for file in Files:
	with open("output_v4/"+file+".csv") as f:
		for row in f:
			tmp = row.split(',')[2:-2]
			country =  row.split(',')[-1].strip()
			tmp_site = parseurl(''.join(tmp))
			# print("country = ",country)
			if tmp_site not in site_country:
				site_country[tmp_site] = country
				dependentList[tmp_site] =set()
				dependentList[tmp_site].add(country)
				output[tmp_site] = [country]
			elif site_country[tmp_site] != country:
				print("file4 = ",file)
				print("wrong site ",tmp_site,site_country[tmp_site],country)
				dependentsite.add(tmp_site)
				if country not in dependentList[tmp_site]:
					dependentList[tmp_site].add(country)
					output[tmp_site].append(country)

for file in Files:
	with open("output_v3/"+file+".csv") as f:
		for row in f:
			tmp = row.split(',')[2:-1]
			country = row.split(',')[-1].strip()
			tmp_site = parseurl(''.join(tmp))
			if tmp_site not in site_country:
				site_country[tmp_site] = country
				dependentList[tmp_site] = set()
				dependentList[tmp_site].add(country)
				output[tmp_site] = [country]
			elif site_country[tmp_site] != country:
				print("file3 = ",file)
				print("wrong site ",tmp_site,site_country[tmp_site],country)
				dependentsite.add(tmp_site)
				if country not in dependentList[tmp_site]:
					dependentList[tmp_site].add(country)
					output[tmp_site].append(country)

with open("cdnsite/dependentList.csv",'a') as fw:
	csvCursor = csv.writer(fw)
	for k,v in output.items():
		if(len(v)> 1):
			fw.write(k+"\t"+','.join(v)+"\n")