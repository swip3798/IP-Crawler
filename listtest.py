from multiprocessing import Pool
import subprocess
import tqdm
import csv
import re

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

def removeDupDicts(l):
	seen = set()
	new_l = []
	for d in l:
	    t = tuple(d.items())
	    if t not in seen:
	        seen.add(t)
	        new_l.append(d)
	return new_l


def cleanCSV(filename):
	data = readcsv(filename)
	data = data[1:]
	new_data = []
	for i in data:
		if i not in new_data:
			new_data.append(i)
	with open(filename, "w") as f:
		f.write(",".join(data[0]) + "\n")
		for i in new_data:
			f.write(",".join(i) + "\n")
	return True




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
	if(res==0):
		time = re.findall(r"([0-9]{1,3})ms", output)[0]
	else:
		time = ""
	return [res==0, host, time]



if __name__ == '__main__':
	l = [{'a': 123, 'b': 1234},
	        {'a': 3222, 'b': 1234},
	        {'a': 123, 'b': 1234}]

	new_l = removeDupDicts(l)

	print(new_l)
	print(cleanCSV("csv/bus_stats.csv"))