from multiprocessing import Pool
import subprocess
import tqdm


def ping(host):
	'''
	Sends a ping to the host with a timeout of 500ms
	'''
	res = 0
	out = subprocess.Popen(["echo", host],stderr=subprocess.STDOUT,stdout=subprocess.PIPE, shell=True)
	t = out.communicate()[0],out.returncode
	res = t[1]
	output=t[0]	
	return [res==0, host, output.decode("utf-8")]



if __name__ == '__main__':
	print(ping("hallo"))