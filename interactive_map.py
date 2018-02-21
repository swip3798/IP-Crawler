import folium
import re
import json



def createInteractiveMap(data, filename, tiles):
	folium_map = folium.Map(location=[25, 0],
	                        zoom_start=3,
	                        tiles=tiles)

	popup_text = """{}<br>
                AS: {}<br> 
                ISP: {}<br>
                Country: {}<br>
                City: {}<br>
                Org: {}<br>
                Region: {}<br>
                Timezone: {}<br>
                ZIP-Code: {}<br>
                Time-To-Response: {}"""

	for i in data:
		popup_text = i["query"] + "<br>AS: " + i["as"] + "<br>ISP: " + i["isp"] + "<br>Country: " + i["country"] + "<br>City: " + i["city"] + "<br>Org: " + i["org"] + "<br>Region: " + i["regionName"] + "<br>Timezone: " + i["timezone"] + "<br>ZIP-Code: " + i["zip"] + "<br>Time-To-Response: " + i["restime"] + "ms"
		popup_text = re.escape(popup_text)
		marker = folium.CircleMarker(location=[i["lat"], i["lon"]], popup=popup_text, fill=True, radius = 5)
		marker.add_to(folium_map)
	

	folium_map.save(filename)


if __name__ == '__main__':
	
	with open("json/database.json", "r") as f:
		ip_infos = json.loads(f.read())
		generateInteractiveMap(ip_infos, "my_map.html", "CartoDB Positron")