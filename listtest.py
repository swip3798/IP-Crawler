from multiprocessing import Pool
import subprocess
import tqdm
import re


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
	for i in range(50):
		ping("8.8.8.8")