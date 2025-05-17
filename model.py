from datetime import time as dtime,date as ddate
from itertools import repeat
from os import mkdir, environ, path, listdir
from typing import Any, Self, Callable,Optional
import json
from string import ascii_letters,digits
from secrets import choice

CURRENT_FORMAT_VERSION = "1.2"

def format_1_0(data:dict) -> dict:
	data["isImportant"] = False
	data["version"] = CURRENT_FORMAT_VERSION
	return data

FORMATTERS:dict[str,Callable[[dict],dict]] = {
	"1.0":format_1_0
}


class EventDecoderError(Exception):...

def UUID() -> str:
	ids = get_uuids()
	result = "".join([
		choice(ascii_letters+digits)
		for _ in repeat(None,40)
	])
	while result in ids:
		result = "".join([
			choice(ascii_letters+digits)
			for _ in repeat(None, 12)
		])
	with open(path.join(app_path,"local_uuids.txt"),"a") as file:
		file.write(f"\n{result}")
	return result

class Event:
	"""
	The class for managing calendar events
	"""
	def __init__(self,
				 name:str,
				 time:dtime,
				 isImportant:bool,
				 uuid:str,
				 completed:bool=False):
		"""
		Create an event
		"""
		self.name = name
		self.time = time
		self.isImportant = isImportant
		self.completed = completed
		self.version = CURRENT_FORMAT_VERSION
		self.id = uuid

	def __hash__(self):
		return self.id

	@classmethod
	def decode(cls,data:dict[str,Any],uuid:str) -> Optional[Self]:
		event_version = data["version"]
		if event_version == CURRENT_FORMAT_VERSION:
			try:
				result = cls(data["name"],
							 dtime.fromisoformat(data["time"]),
							 data["isImportant"],
							 uuid,
							 data["completed"]
							 )
				print(result.__dict__)
				return result
			except KeyError as e:
				raise EventDecoderError(f"\nevent version is alright, but the contents are corrupted\n{e}!")
		else:
			if event_version in FORMATTERS:
				return cls.decode(FORMATTERS[event_version](data),UUID())
			else:
				raise EventDecoderError(f"\nCannot decode event of version {event_version}!")

	def save(self) -> dict:
		return {"name":self.name,
				"time":self.time.isoformat(),
				"version":self.version,"isImportant":self.isImportant,
				"completed":self.completed,
				}

app_path = f"{environ.get("HOME")}/Library/Application Support/live-smarter"


dir_path = path.join(app_path,"db")


def get_uuids() -> list[str]:
	with open(path.join(app_path,"local_uuids.txt")) as file:
		ids = file.readlines()
	return ids


def setup_directory():
	if not path.exists(dir_path):
		print("Setting up the directory!")
		mkdir(app_path)
		mkdir(dir_path)
		with open(path.join(app_path,"local_uuids.txt"),"w") as file:
			file.write("")


def create_date_path(date:ddate):
	return path.join(str(date.year),str(date.month),str(date.day))


def load_all(date:ddate) -> list[Event]:
	load_dir_path = create_date_path(date)
	try:
		all_item_names = listdir(path.join(dir_path,load_dir_path))
	except FileNotFoundError:
		all_item_names = []
		pass
	print(all_item_names)
	all_items = []
	for name in all_item_names:
		try:
			with open(path.join(dir_path,load_dir_path,name)) as file:
				all_items.append(
					Event.decode(json.load(file),name)
				)
		except FileNotFoundError as e:
			print(f"Nothing planned, {e}")
	return sorted(all_items,key=lambda x:x.time)


def save_item(date:ddate,item:Event):
	if not path.exists(p1:=path.join(dir_path,str(date.year))):
		mkdir(p1)
	if not path.exists(p2:=path.join(dir_path,p1,str(date.month))):
		mkdir(p2)
	if not path.exists(p3:=path.join(dir_path,p1,p2,str(date.day))):
		mkdir(p3)
	with open(path.join(p3,item.id),"w") as file:
		json.dump(item.save(),file)


def get_active_dates(year:int,month:int):
	all_days:dict[str:int] = {}
	all_years = listdir(dir_path)
	if str(year) in all_years:
		all_months = listdir(path.join(dir_path,str(year)))
		if str(month) in all_months:
			all_days = {i:len(listdir(
				path.join(dir_path,str(year),str(month),str(i))
			)) for i in listdir(path.join(dir_path,str(year),str(month))) if i[0] != "."}
	keys = list(all_days.keys())
	keys.sort()
	results = {i: all_days[i] for i in keys}
	return results


setup_directory()