import numpy as np
import matplotlib.pyplot as plt
import operator
import json


def createChartBar(data):
	countryChart = {}
	for i in data:
		
		if i["countryCode"] in countryChart.keys():
			countryChart[i["countryCode"]]+=1
		else:
			countryChart[i["countryCode"]]=1
	
	means_countrys = []
	sorted_x = sorted(countryChart.items(), key=operator.itemgetter(1))
	sorted_x.reverse()
	sorted_x = sorted_x[:21]
	for i in sorted_x:
		means_countrys.append(i[1])
	n_groups = len(sorted_x[:21])
	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width = 0.35
	opacity = 0.4
	error_config = {'ecolor': '0.3'}
	groups = []
	for i in sorted_x:
		groups.append(i[0])
	rects1 = plt.bar(index, means_countrys, bar_width,
	                 alpha=opacity,
	                 color='b',
	                 error_kw=error_config)
	plt.xlabel('Country')
	plt.ylabel('Count of IP-Adresses')
	plt.title('IPs per country')
	plt.xticks(index + bar_width / 2, groups)
	plt.legend()

	plt.tight_layout()
	return plt

def createTimeBarMax(data):
	countryChart = {}
	for i in data:
		if i["countryCode"] in countryChart.keys():
			if i["restime"] != "ris":
				countryChart[i["countryCode"]][0] += int(i["restime"])
				countryChart[i["countryCode"]][1] += 1
		else:
			if i["restime"] != "ris":
				countryChart[i["countryCode"]]=[int(i["restime"]), 1]
	for i in countryChart:
		countryChart[i] = countryChart[i][0]/countryChart[i][1]
	
	means_countrys = []
	sorted_x = sorted(countryChart.items(), key=operator.itemgetter(1))
	sorted_x.reverse()
	sorted_x = sorted_x[:21]
	for i in sorted_x:
		means_countrys.append(i[1])
	n_groups = len(sorted_x[:21])
	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width = 0.35
	opacity = 0.4
	error_config = {'ecolor': '0.3'}
	groups = []
	for i in sorted_x:
		groups.append(i[0])
	rects1 = plt.bar(index, means_countrys, bar_width,
	                 alpha=opacity,
	                 color='b',
	                 error_kw=error_config)
	plt.xlabel('Country')
	plt.ylabel('Response time per country')
	plt.title('Response time')
	plt.xticks(index + bar_width / 2, groups)
	plt.legend()

	plt.tight_layout()
	return plt

def createTimeBarMin(data):
	countryChart = {}
	for i in data:
		if i["countryCode"] in countryChart.keys():
			if i["restime"] != "ris":
				countryChart[i["countryCode"]][0] += int(i["restime"])
				countryChart[i["countryCode"]][1] += 1
		else:
			if i["restime"] != "ris":
				countryChart[i["countryCode"]]=[int(i["restime"]), 1]
	for i in countryChart:
		countryChart[i] = countryChart[i][0]/countryChart[i][1]
	
	means_countrys = []
	sorted_x = sorted(countryChart.items(), key=operator.itemgetter(1))
	sorted_x = sorted_x[:21]
	for i in sorted_x:
		means_countrys.append(i[1])
	n_groups = len(sorted_x[:21])
	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width = 0.35
	opacity = 0.4
	error_config = {'ecolor': '0.3'}
	groups = []
	for i in sorted_x:
		groups.append(i[0])
	rects1 = plt.bar(index, means_countrys, bar_width,
	                 alpha=opacity,
	                 color='b',
	                 error_kw=error_config)
	plt.xlabel('Country')
	plt.ylabel('Response time per country')
	plt.title('Response time')
	plt.xticks(index + bar_width / 2, groups)
	plt.legend()

	plt.tight_layout()
	return plt

if __name__ == '__main__':
	with open("json/database.json", "r") as f:
		data = json.loads(f.read())
		createTimeBarMax(data).savefig("images/fig_max")
		createTimeBarMin(data).savefig("images/fig_min")