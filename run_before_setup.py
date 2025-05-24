import json,os,codecs

def convert_to_ascii():
	language_files = {}
	for filename in os.listdir("localization"):
		if filename[0] != ".":
			with open(os.path.join("localization",filename)) as file:
				language_files[filename] = json.loads(file.read())

	os.mkdir("tmp")
	path = os.path.join("tmp","localization")
	os.mkdir(path)
	for file in language_files:
		print(file)
		with open(os.path.join(path,file),"w",encoding="us-ascii") as new_file:
			json.dump(language_files[file],new_file)

if not os.path.exists("tmp"):
	convert_to_ascii()
else:
	print("Delete the tmp folder to proceed")