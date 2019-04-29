# add a column-Resistance_cnt to csv

import csv
CountryList = ["US","Canada","France","Germany","Italy","Japan","Uk","Taiwan"]

for country in CountryList:
	file = 'thoroughscan/201904_'+country+'scan_result_stat_final.csv'
	d = []
	with open(file, newline='') as csvfile:
		rows = csv.reader(csvfile)
		for row in rows:
			d.append(row)
	d[0].append('Resistance_cnt')
	file = '201904_'+country+'scan_result_stat_final.csv'
	fw = open(file,"w")
	csvCursor = csv.writer(fw)
	csvCursor.writerow(d[0])
	for i in range(1,len(d)):
		cnt = 0
		writefile = d[i]
		if "Ready" in writefile[2]:
			for j in range(4,15):
				if "False" in writefile[j]:
					cnt += 1
		writefile.append(cnt)
		csvCursor.writerow(writefile)