import json

def removeDupDicts(l):
	seen = set()
	new_l = []
	for d in l:
	    t = tuple(d.items())
	    if t not in seen:
	        seen.add(t)
	        new_l.append(d)
	return new_l

if __name__ == '__main__':
	data = []
	with open("database.json", "r") as j:
		data = json.loads(j.read())
	print(len(data))
	data = removeDupDicts(data)
	with open("database.json", "w") as f:
		f.write(json.dumps(data, indent = 4, sort_keys = True))
	print(len(data))
	input()
