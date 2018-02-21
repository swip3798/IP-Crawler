'''
A crawling script to ping random IPs and if it responses gathering informations about it and do some graphical visualizations
'''

import subprocess
import multiprocessing
import os
from multiprocessing import Pool
from random import *
import time
import requests
import json
from map_geoplotlib import showMapWithIPs, showMapWithoutIPs, saveMapWithoutIPs, saveMapWithIPs
from create_bar_chart import createChartBar, createTimeBarMax, createTimeBarMin
import create_result_pdf
import tqdm
import csv
import re
from numpy import genfromtxt
from interactive_map import createInteractiveMap

###Functions###

def takeFirst(elem):
	'''
	Function to get the first element for sorting
	'''
	return elem[0]

def gen_ip():
	'''
	Generates a random public IP Adress
	'''
	while True:
		firstElement = randint(1,255)
		secondElement = randint(0,255)
		thirdElement = randint(0,255)
		fourthElement = randint(1,254)
		if(firstElement==10):
			pass
		elif(firstElement==127):
			pass
		elif(firstElement==172 and secondElement>=16 and secondElement<=31):
			pass
		elif(firstElement==192 and secondElement==168):
			pass
		else:
			return str(firstElement) + "." + str(secondElement) + "." + str(thirdElement) +  "." + str(fourthElement)

def removeDupDicts(l):
	seen = set()
	new_l = []
	for d in l:
	    t = tuple(d.items())
	    if t not in seen:
	        seen.add(t)
	        new_l.append(d)
	return new_l

def gen_ips(num, current_list=None):
	'''
	Generates a list of unique IP Adresses, num is the length of the returned list
	'''
	if(current_list==None):
		ips=[]
	else:
		ips = current_list
	while len(ips) < num:
		new_ip=gen_ip()
		if new_ip not in ips:
			ips.append(new_ip)
	return ips



def ping(host):
	'''
	Sends a ping to the host with a timeout of 500ms
	'''
	res = 0
	out = subprocess.Popen(["ping", "-n", "1", "-w", "500", host],stderr=subprocess.STDOUT,stdout=subprocess.PIPE, shell=True)
	t = out.communicate()[0],out.returncode
	res = t[1]
	output=t[0]
	output = output.decode("utf-8", "ignore")
	try:
		if(res==0):
			time = re.findall(r"([0-9]{1,3})ms", output)[0]
		else:
			time = ""
	except Exception as e:
		time = "ris"
	return [res==0, host, time]


def cleanCSV(filename):
	csv_data = readcsv(filename)
	data = csv_data[1:]
	new_data = []
	for i in data:
		if i not in new_data:
			new_data.append(i)
	with open(filename, "w") as f:
		f.write(",".join(csv_data[0]) + "\n")
		for i in new_data:
			f.write(",".join(i) + "\n")
	return True

def readcsv(filename):	
	ifile = open(filename, "rU")
	reader = csv.reader(ifile, delimiter=";")

	rownum = 0	
	a = []

	for row in reader:
	    a.append (row)
	    rownum += 1

	ifile.close()
	return a


###Functions END###

###MAIN FUNCTION###

def main():
	number_of_ips = int(input("How many IPs should be checked: "))
	threads = int(input("Number of threads: "))
	#Save time for time measurement
	now = time.time()
	print("Generating IPs...")
	ip_list = gen_ips(num = number_of_ips)
	print("Creating Pool...")
	pool = Pool(threads)
	print("Start pinging...")
	results=[]
	for _ in tqdm.tqdm(pool.imap_unordered(ping, ip_list), total=len(ip_list)):
	    results.append(_)
	pool.close()
	#Open all relevant files for saving
	logs = open("logs/results.log", "w")
	info_file = open("logs/informations.log", "w")
	csv_map = open("csv/bus.csv", "w")
	csv_stats = open("csv/bus_stats.csv", "a")
	csv_map.write("ip,lat,lon\n")
	print("Analysing responses...")
	results.sort(key=takeFirst, reverse=True)
	reached = 0
	unreached = 0
	ip_infos = []
	#Wait if the last requests were too soon, to avoid a ban from the API
	with open("control/lastRequest", "r") as f:
		last = int(f.read())
		if (time.time()-last<70):
			print("Please wait until API is ready for new requests", "(" +str(time.time()-last) + ")")
			time.sleep(70-(time.time()-last))
			time.sleep(5)
	analyseRequests = 0
	for n,i in enumerate(results):
		if(i[0]==True):
			#If the IP was reached
			reached+=1
			#Prevent API Ban
			if analyseRequests>145:
				print("Wait until API allows new requests")
				time.sleep(60)
				analyseRequests = 0
			#Call the API
			s = requests.Session()
			s.headers.update({	"Content-Type": "application/x-www-form-urlencoded",
    							"Accept": "application/json"})
			r = s.get("http://ip-api.com/json/" + i[1])
			analyseRequests +=1
			#Save time for the last Request to prevent ban
			lastRequestTime = time.time()
			#Load answer from API in dictionary r
			r = json.loads(r.text)
			r["restime"] = i[2]
			print("#"  + str(n), "on", i[1])
			try:
				if r["status"]=="success":
					info_file.write("-------------------------------------------\n")
					info_file.write("IP-Adress: " + str(i[1]) + "\n")
					info_file.write("AS: " + str(r["as"]) + "\n")
					info_file.write("Region: " + str(r["regionName"]) + "\n")
					info_file.write("Zip: " + str(r["zip"]) + "\n")
					info_file.write("Longitude: " + str(r["lon"]) + "\n")
					info_file.write("Latitude: " + str(r["lat"]) + "\n")
					info_file.write("Country-Code: " + str(r["countryCode"]) + "\n")
					info_file.write("City: " + str(r["city"]) + "\n")
					info_file.write("Country: " + str(r["country"]) + "\n")
					info_file.write("-------------------------------------------\n\n")
					csv_map.write(str(i[1]) + "," + str(r["lat"]) + "," + str(r["lon"]) + "\n")
					csv_stats.write(str(i[1]) + "," + str(r["lat"]) + "," + str(r["lon"]) + "\n")
					ip_infos.append(r)
			except Exception as e:
				#If there was an Error on reading API response
				info_file.write("Failed to gather information, here's the answer of the server:\n" + json.dumps(r) + "\n\n")
				info_file.write("Error: " + str(e) + "\n\n")
				info_file.write("-------------------------------------------\n\n")
		else:
			#If the IP was not reached
			unreached+=1
	percentage = (reached/unreached)*100
	#Creates a chartbar and save it as figure.png
	createChartBar(ip_infos).savefig("images/figure")
	createTimeBarMax(ip_infos).savefig("images/fig_max")
	createTimeBarMin(ip_infos).savefig("images/fig_min")
	#Write the lastRequestTime in file for next script execution
	with open("control/lastRequest", "w") as f:
		f.write(str(int(lastRequestTime)))
	print("Writing logs...")
	logs.write("Ip crawling response: \nReached: " + str(reached) + ";\tNot reached: " + str(unreached) + ";\t (" + str(percentage)  + "% reached)\n")
	logs.write("-------------------------------------------------------------------------------------\n")
	for i in results:
		if(i[0]==True):
			logs.write(i[1] + "\t is reachable\n")
		else:
			logs.write(i[1] + "\t is unreachable\n")
	#Close all files to prevent data loss
	logs.close()
	info_file.close()
	csv_map.close()
	csv_stats.close()
	#Save all maps
	saveMapWithIPs("csv/bus.csv","images/ip_map_w")
	saveMapWithoutIPs("csv/bus.csv","images/ip_map_o")
	saveMapWithoutIPs("csv/bus_stats.csv","images/total_ip_map")
	print("Writing report...")
	filename = "reports/report_" + time.strftime("%Y%m%d-%H%M%S") + ".pdf"
	create_result_pdf.createNewReport(reached, unreached, ip_infos, filename)
	#Save the IP Infos in JSON for later reading
	print("Add to json...")
	with open("json/database.json", "r") as f:
		ip_infos = ip_infos + json.loads(f.read())
	json_ip_infos = json.dumps(removeDupDicts(ip_infos))
	with open("json/database.json", "w") as f:
		f.write(json_ip_infos)
	print("Clean stats CSV-File")
	cleanCSV("csv/bus_stats.csv")
	print("Creating interactive map...")
	htmlname = "html/map_" + time.strftime("%Y%m%d-%H%M%S") + ".html"
	createInteractiveMap(ip_infos, htmlname, "CartoDB dark_matter")
	print("[Finished in " + str(time.time()-now) + "s]")
	print("Open report...")
	os.system("reports\\" + filename[8:])
	print("Open interactive map...")
	os.system("html\\" + htmlname[5:])



###MAIN END###

if __name__ == '__main__':
	main()