"""
Example of dot density map
"""
import geoplotlib
from geoplotlib.utils import read_csv,epoch_to_str, BoundingBox
from geoplotlib.colors import ColorMap
import json

def showMapWithIPs():
	data = read_csv('bus2.csv')
	geoplotlib.dot(data)
	geoplotlib.labels(data, 'ip', color=[0,0,255,255], font_size=7, anchor_x='center')
	geoplotlib.show()

def showMapWithoutIPs():
	data = read_csv('bus2.csv')
	geoplotlib.dot(data)
	geoplotlib.show()

def saveMapWithoutIPs(input_name, filename):
	data = read_csv(input_name)
	geoplotlib.dot(data)
	geoplotlib.savefig(filename)

def saveMapWithIPs(input_name, filename):
	data = read_csv(input_name)
	geoplotlib.dot(data)
	geoplotlib.labels(data, 'ip', color=[0,0,255,255], font_size=7, anchor_x='center')
	geoplotlib.savefig(filename)